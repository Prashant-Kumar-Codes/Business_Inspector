from fastapi import Request, APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
import secrets
from .signup_otp import send_otp_email
from .delete_unverified import delete_unverified_users

login_route = APIRouter()
login_template = Jinja2Templates(directory='app/templates')


# ======= RENDER LOGIN PAGE =======
@path.get('/login')
def login(request: Response):
    return login_template.TemplateResponse(
        'login.html',
        {request:request}
    )

# ======= OTP - VERIFY =======
@path.post('/signup/verify_otp')
def verify(request: request):
    try:
        if request.is_json:
            data = request.get_json() or {}
            otp = str(data.get('otp', '')).strip()
            email = data.get('email', '').strip() or session.get('verify_email')
        else:
            email = session.get('verify_email')
            otp = str(request.form.get('otp', '')).strip()

        print(f"OTP verification attempt for email: {email} | OTP: {otp}")
        
        if not email:
            msg = 'Session expired or email missing. Please sign up again.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 400
            flash(msg, 'error')
            return redirect(url_for('login'))

        if not otp or len(otp) != 6:
            msg = 'Please enter a valid 6-digit OTP.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 400
            flash(msg, 'error')
            return redirect(url_for('login'))

        mycon  = dbConn()
        cursor = mycon.cursor()

        cursor.execute("SELECT otp, otp_created_at FROM otp_data WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result:
            cursor.close(); mycon.close()
            print(f"❌ No DB record in otp_data for email: {email}")
            msg = 'OTP details not found. Please sign up again.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 404
            flash(msg, 'error')
            return redirect(url_for('login'))

        hash_otp, otp_created_at = result
        print(f"🗄 Stored OTP hash found | Created: {otp_created_at}")

        if not hash_otp:
            cursor.close(); mycon.close()
            msg = 'OTP already used or invalid. Please request a new code.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 400
            flash(msg, 'error')
            return redirect(url_for('login'))

        if datetime.utcnow() - otp_created_at > timedelta(minutes=10):
            cursor.close(); mycon.close()
            print(f"⌛ OTP expired for {email}")
            msg = 'OTP has expired. Please click resend to get a new code.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 400
            flash(msg, 'error')
            return redirect(url_for('login'))

        if not check_password_hash(hash_otp, otp):
            cursor.close(); mycon.close()
            print(f"❌ OTP mismatch for {email}: got '{otp}'")
            msg = 'Invalid OTP code. Please check and try again.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 400
            flash(msg, 'error')
            return redirect(url_for('login'))

        cursor.execute("UPDATE login_data SET is_verified = true WHERE email = %s", (email,))
        cursor.execute("UPDATE otp_data SET otp = NULL WHERE email = %s", (email,))
        mycon.commit()
        
        cursor.execute("SELECT username, organization FROM login_data WHERE email = %s", (email,))
        user_info = cursor.fetchone()
        cursor.close(); mycon.close()

        print(f"[OK] Email verified successfully: {email}")
        if user_info:
            session.permanent = True
            session['username'] = user_info[0]
            session['user_email'] = email
            session['organization'] = user_info[1]

        session.pop('verify_email', None)
        session.pop('verify_user', None)
        session.pop('verify_username', None)

        msg = 'Email verified successfully! Welcome to Business Inspector.'
        redirect_url = url_for('inspect_auth.inspect')
        
        if request.is_json:
            return jsonify({
                'success': True,
                'message': msg,
                'redirect_url': redirect_url
            }), 200

        flash(msg, 'success')
        return redirect(redirect_url)

    except Exception as e:
        print(f"❌ Verify error: {e}")
        import traceback; traceback.print_exc()
        msg = 'Verification failed due to a server error. Please try again.'
        if request.is_json:
            return jsonify({'success': False, 'message': msg}), 500
        flash(msg, 'error')
        return redirect(url_for('login'))


# ======= LOGIN SUBMIT =======
@path.route('/login/submit', methods=['GET', 'POST'])
def login_submit():
    if request.method == 'GET':
        return redirect(url_for('login'))

    try: 
        data = request.get_json() if request.is_json else request.form
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        print(f'Attempting login for email: {email}')
            
        if not email or not password:
            msg = 'Email and Password are required.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 400
            flash(msg, 'error')
            return redirect(url_for('login'))

        mycon  = dbConn()
        cursor = mycon.cursor()

        # Query strictly by email (Primary Key)
        cursor.execute(
            "SELECT username, email, organization, password, is_verified FROM login_data WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()

        if not user:
            cursor.close(); mycon.close()
            print(f"❌ No user found for email: {email}")
            msg = 'No account found with this email. Please Sign Up first.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 401
            flash(msg, 'error')
            return redirect(url_for('login'))

        username, user_email, user_organization, hashed_password, is_verified = user

        if not is_verified:
            print(f"[WARNING] Account not verified: {user_email}")
            session['verify_email'] = user_email
            session['verify_user']  = username
            cursor.close(); mycon.close()
            msg = 'Your account is not verified yet. Please enter the OTP sent to your email.'
            if request.is_json:
                return jsonify({
                    'success': False,
                    'message': msg,
                    'redirect_to_verify': True,
                    'email': user_email
                }), 403
            flash(msg, 'warning')
            return redirect(url_for('login'))

        if not check_password_hash(hashed_password, password):
            cursor.close(); mycon.close()
            print(f"❌ Wrong password for: {email}")
            msg = 'Invalid credentials. Please check your password.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 401
            flash(msg, 'error')
            return redirect(url_for('login'))

        # Increment login_count if column exists
        try:
            cursor.execute(
                "UPDATE login_data SET login_count = COALESCE(login_count, 0) + 1 WHERE email = %s",
                (user_email,)
            )
            mycon.commit()
        except Exception as count_err:
            print(f"[NOTE] login_count update skipped/not present: {count_err}")
            mycon.rollback()

        cursor.close(); mycon.close()

        # Set session details on successful authentication
        session.permanent  = True
        session['username']     = username
        session['user_email']   = user_email
        session['organization'] = user_organization

        print(f"[OK] Login successful: {username} ({user_email})")

        redirect_url = url_for('inspect_auth.inspect')
        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Login successful!',
                'redirect_url': redirect_url
            }), 200

        flash('Login successful!', 'success')
        return redirect(redirect_url)

    except Exception as e:
        print(f"❌ Login error: {e}")
        import traceback; traceback.print_exc()
        msg = 'Login failed due to a server error. Please try again.'
        if request.is_json:
            return jsonify({'success': False, 'message': msg}), 500
        flash(msg, 'error')
        return redirect(url_for('login'))


# ======= SIGNUP SUBMIT =======
@path.route('/signup/submit', methods=['GET', 'POST'])
def signup_submit():
    if request.method == 'GET':
        return redirect(url_for('login'))

    try: 
        data = request.get_json() if request.is_json else request.form
        email = data.get('email', '').strip()
        username = data.get('username', '').strip()
        organization = data.get('organization', '').strip()
        password = data.get('password', '').strip()
        
        print(f'Attempting signup: email -> {email}, username -> {username}')
        
        if not all([email, username, password]):
            msg = 'Username, Email and Password are required.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 400
            flash(msg, 'error')
            return redirect(url_for('login'))

        if len(password) < 6:
            msg = 'Password length must be at least 6 characters.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 400
            flash(msg, 'error')
            return redirect(url_for('login'))
        
        myconn = dbConn()
        cursor = myconn.cursor()
        
        # Unique check strictly by primary key email (usernames can be identical across different users)
        cursor.execute('SELECT username, email, is_verified FROM login_data WHERE email = %s', (email,))
        existing = cursor.fetchone()
        
        otp = f"{secrets.randbelow(1_000_000):06d}"
        hash_otp = generate_password_hash(otp)
        hash_password = generate_password_hash(password)

        if existing:
            ex_username, ex_email, is_verified = existing
            if is_verified:
                cursor.close(); myconn.close()
                print(f"[WARNING] Email already registered & verified: {email}")
                msg = 'This email is already registered. Please log in instead.'
                if request.is_json:
                    return jsonify({'success': False, 'message': msg}), 409
                flash(msg, 'error')
                return redirect(url_for('login'))
            else:
                print(f"[INFO] Updating unverified existing user record: {email}")
                cursor.execute("""
                    UPDATE login_data
                    SET username = %s, organization = %s, password = %s, created_at = NOW()
                    WHERE email = %s
                """, (username, organization, hash_password, ex_email))

                cursor.execute("SELECT email FROM otp_data WHERE email = %s", (ex_email,))
                if cursor.fetchone():
                    cursor.execute("UPDATE otp_data SET otp = %s, otp_created_at = NOW() WHERE email = %s", (hash_otp, ex_email))
                else:
                    cursor.execute("INSERT INTO otp_data(email, otp, otp_created_at) VALUES(%s, %s, NOW())", (ex_email, hash_otp))
                
                myconn.commit()
                cursor.close(); myconn.close()

                session['verify_user'] = username
                session['verify_email'] = ex_email

                try:
                    send_otp_email(ex_email, otp, username)
                    print(f"[OK] OTP email sent -> {ex_email}")
                except Exception as e:
                    print(f"[WARNING] OTP email failed: {e}")
                    import traceback; traceback.print_exc()

                msg = 'Account pending verification! We sent a 6-digit OTP code to your email.'
                if request.is_json:
                    return jsonify({'success': True, 'message': msg, 'requires_otp': True}), 200
                flash(msg, 'info')
                return redirect(url_for('login'))

        cursor.execute("""INSERT INTO login_data (email, username, organization, password, is_verified, created_at)
                VALUES(%s, %s, %s, %s, false, NOW())""",
                (email, username, organization, hash_password)
        )
        
        cursor.execute("SELECT email FROM otp_data WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.execute("UPDATE otp_data SET otp = %s, otp_created_at = NOW() WHERE email = %s", (hash_otp, email))
        else:
            cursor.execute("""INSERT INTO otp_data(email, otp, otp_created_at)
                    VALUES(%s, %s, NOW())""",
                    (email, hash_otp))
        
        myconn.commit()
        cursor.close(); myconn.close()

        print(f"[OK] User inserted: {email} | OTP generated and inserted")
        
        session['verify_user'] = username
        session['verify_email'] = email

        try:
            send_otp_email(email, otp, username)
            print(f"[OK] OTP email sent -> {email}")
        except Exception as e:
            print(f"[WARNING] OTP email failed: {e}")
            import traceback; traceback.print_exc()

        msg = 'Account registered! Check your email for the 6-digit OTP code.'
        if request.is_json:
            return jsonify({'success': True, 'message': msg, 'requires_otp': True}), 201
            
        flash(msg, 'success')
        return redirect(url_for('login'))

    except Exception as e:
        print(f"❌ Signup error: {e}")
        import traceback; traceback.print_exc()
        msg = 'Signup failed due to a server error. Please try again later.'
        if request.is_json:
            return jsonify({'success': False, 'message': msg}), 500
        flash(msg, 'error')
        return redirect(url_for('login'))


# ======= LOGOUT HANDLE =======
@path.route('/logout', methods=['GET', 'POST'])
def logout():
    print(f"Logout -> {session.get('username', 'Unknown')}")
    session.clear()
    return redirect(url_for('login'))


# ======= OTP RESEND =======
@path.route('/resend_otp', methods=['POST'])
def resend_otp():
    try:
        data = request.get_json() if request.is_json else request.form
        email    = data.get('email', '').strip() or session.get('verify_email')
        username = session.get('verify_user', 'User')
        print(f"📧 Resend OTP request for → {email}")

        if not email:
            msg = 'Session expired or email missing. Please sign up again.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 400
            flash(msg, 'error')
            return redirect(url_for('login'))

        otp = f"{secrets.randbelow(1_000_000):06d}"
        hash_otp = generate_password_hash(otp)
        
        mycon  = dbConn()
        cursor = mycon.cursor()
        
        cursor.execute("SELECT email FROM otp_data WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.execute("UPDATE otp_data SET otp = %s, otp_created_at = NOW() WHERE email = %s", (hash_otp, email))
        else:
            cursor.execute("INSERT INTO otp_data(email, otp, otp_created_at) VALUES(%s, %s, NOW())", (email, hash_otp))
            
        mycon.commit()
        cursor.close(); mycon.close()
        print(f"🗄 New OTP saved in otp_data for {email}")

        try:
            send_otp_email(email, otp, username)
            msg = 'New OTP code sent to your email address!'
            if request.is_json:
                return jsonify({'success': True, 'message': msg}), 200
            flash(msg, 'success')
        except Exception as e:
            print(f"[WARNING] Email send failed: {e}")
            msg = 'Failed to send email. Please try again.'
            if request.is_json:
                return jsonify({'success': False, 'message': msg}), 500
            flash(msg, 'error')

        return redirect(url_for('login'))

    except Exception as e:
        print(f"❌ Resend OTP error: {e}")
        import traceback; traceback.print_exc()
        msg = 'An error occurred while resending OTP. Please try again.'
        if request.is_json:
            return jsonify({'success': False, 'message': msg}), 500
        flash(msg, 'error')
        return redirect(url_for('login'))
