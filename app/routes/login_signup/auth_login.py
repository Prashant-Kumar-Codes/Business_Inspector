from contextlib import closing
from datetime import datetime, timedelta
import secrets

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from werkzeug.security import check_password_hash, generate_password_hash

from app.database.db_con import get_db_connection
from app.logger.logger import logger
from .signup_otp import send_otp_email
from app.routes.helper.request_type_and_respond import _request_data, _respond


login_route = APIRouter()
login_template = Jinja2Templates(directory='app/templates')


def _save_otp(cursor, email: str, hashed_otp: str) -> None:
    cursor.execute('SELECT email FROM otp_data WHERE email = %s', (email,))
    if cursor.fetchone():
        cursor.execute(
            'UPDATE otp_data SET otp = %s, otp_created_at = NOW() WHERE email = %s',
            (hashed_otp, email),
        )
    else:
        cursor.execute(
            'INSERT INTO otp_data(email, otp, otp_created_at) VALUES(%s, %s, NOW())',
            (email, hashed_otp),
        )


@login_route.get('/login')
async def login(request: Request):
    flash_messages = request.session.pop('flash_messages', [])
    return login_template.TemplateResponse(
        request=request,
        name='login.html',
        context={'flash_messages': flash_messages},
    )


@login_route.get('/login/submit')
async def login_submit_get():
    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)


@login_route.post('/signup/verify_otp')
async def verify(request: Request):
    try:
        data = await _request_data(request)
        otp = str(data.get('otp') or '').strip()
        email = str(data.get('email') or request.session.get('verify_email') or '').strip()
        logger.info('OTP verification attempt for email: %s', email)

        if not email:
            return _respond(request, {
                'success': False,
                'message': 'Session expired or email missing. Please sign up again.',
            }, status.HTTP_400_BAD_REQUEST, flash_category='error')

        if len(otp) != 6 or not otp.isdigit():
            return _respond(request, {
                'success': False,
                'message': 'Please enter a valid 6-digit OTP.',
            }, status.HTTP_400_BAD_REQUEST, flash_category='error')

        with closing(get_db_connection()) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT otp, otp_created_at FROM otp_data WHERE email = %s',
                    (email,),
                )
                otp_record = cursor.fetchone()
                if not otp_record:
                    return _respond(request, {
                        'success': False,
                        'message': 'OTP details not found. Please sign up again.',
                    }, status.HTTP_404_NOT_FOUND, flash_category='error')

                hashed_otp, otp_created_at = otp_record
                if not hashed_otp:
                    return _respond(request, {
                        'success': False,
                        'message': 'OTP already used or invalid. Please request a new code.',
                    }, status.HTTP_400_BAD_REQUEST, flash_category='error')

                current_time = datetime.now(otp_created_at.tzinfo) if otp_created_at.tzinfo else datetime.utcnow()
                if current_time - otp_created_at > timedelta(minutes=10):
                    return _respond(request, {
                        'success': False,
                        'message': 'OTP has expired. Please click resend to get a new code.',
                    }, status.HTTP_400_BAD_REQUEST, flash_category='error')

                if not check_password_hash(hashed_otp, otp):
                    return _respond(request, {
                        'success': False,
                        'message': 'Invalid OTP code. Please check and try again.',
                    }, status.HTTP_400_BAD_REQUEST, flash_category='error')

                cursor.execute('UPDATE login_data SET is_verified = true WHERE email = %s', (email,))
                cursor.execute('UPDATE otp_data SET otp = NULL WHERE email = %s', (email,))
                connection.commit()
                cursor.execute(
                    'SELECT username, organization FROM login_data WHERE email = %s',
                    (email,),
                )
                user_info = cursor.fetchone()

        logger.info('Email verified successfully: %s', email)
        if user_info:
            request.session.update({
                'username': user_info[0],
                'user_email': email,
                'organization': user_info[1],
            })

        for key in ('verify_email', 'verify_user', 'verify_username'):
            request.session.pop(key, None)

        message = 'Email verified successfully! Welcome to Business Inspector.'
        return _respond(request, {
            'success': True,
            'message': message,
            'redirect_url': '/inspect',
        }, redirect_url='/inspect', flash_category='success')

    except Exception:
        logger.exception('OTP verification failed')
        return _respond(request, {
            'success': False,
            'message': 'Verification failed due to a server error. Please try again.',
        }, status.HTTP_500_INTERNAL_SERVER_ERROR, flash_category='error')


@login_route.post('/login/submit')
async def login_submit(request: Request):
    try:
        data = await _request_data(request)
        email = str(data.get('email') or '').strip()
        password = str(data.get('password') or '').strip()

        if not email or not password:
            return _respond(request, {
                'success': False,
                'message': 'Email and Password are required.',
            }, status.HTTP_400_BAD_REQUEST, flash_category='error')

        with closing(get_db_connection()) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT username, email, organization, password, is_verified '
                    'FROM login_data WHERE email = %s',
                    (email,),
                )
                user = cursor.fetchone()
                if not user:
                    logger.warning('Login attempt for unknown email: %s', email)
                    return _respond(request, {
                        'success': False,
                        'message': 'No account found with this email. Please Sign Up first.',
                    }, status.HTTP_401_UNAUTHORIZED, flash_category='error')

                username, user_email, organization, hashed_password, is_verified = user
                if not is_verified:
                    request.session['verify_email'] = user_email
                    request.session['verify_user'] = username
                    return _respond(request, {
                        'success': False,
                        'message': 'Your account is not verified yet. Please enter the OTP sent to your email.',
                        'redirect_to_verify': True,
                        'email': user_email,
                    }, status.HTTP_403_FORBIDDEN, flash_category='warning')

                if not check_password_hash(hashed_password, password):
                    logger.warning('Invalid password for email: %s', email)
                    return _respond(request, {
                        'success': False,
                        'message': 'Invalid credentials. Please check your password.',
                    }, status.HTTP_401_UNAUTHORIZED, flash_category='error')

                try:
                    cursor.execute(
                        'UPDATE login_data SET login_count = COALESCE(login_count, 0) + 1 '
                        'WHERE email = %s',
                        (user_email,),
                    )
                    connection.commit()
                except Exception:
                    logger.warning('login_count update skipped or unavailable', exc_info=True)
                    connection.rollback()

        request.session.update({
            'username': username,
            'user_email': user_email,
            'organization': organization,
        })
        logger.info('Login successful: %s (%s)', username, user_email)
        return _respond(request, {
            'success': True,
            'message': 'Login successful!',
            'redirect_url': '/inspect',
        }, redirect_url='/inspect', flash_category='success')

    except Exception:
        logger.exception('Login failed')
        return _respond(request, {
            'success': False,
            'message': 'Login failed due to a server error. Please try again.',
        }, status.HTTP_500_INTERNAL_SERVER_ERROR, flash_category='error')


@login_route.get('/signup/submit')
async def signup_submit_get():
    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)


@login_route.post('/signup/submit')
async def signup_submit(request: Request):
    try:
        data = await _request_data(request)
        email = str(data.get('email') or '').strip()
        username = str(data.get('username') or '').strip()
        organization = str(data.get('organization') or '').strip()
        password = str(data.get('password') or '').strip()

        if not all((email, username, password)):
            return _respond(request, {
                'success': False,
                'message': 'Username, Email and Password are required.',
            }, status.HTTP_400_BAD_REQUEST, flash_category='error')

        if len(password) < 6:
            return _respond(request, {
                'success': False,
                'message': 'Password length must be at least 6 characters.',
            }, status.HTTP_400_BAD_REQUEST, flash_category='error')

        otp = f'{secrets.randbelow(1_000_000):06d}'
        hashed_otp = generate_password_hash(otp)
        hashed_password = generate_password_hash(password)

        with closing(get_db_connection()) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT username, email, is_verified FROM login_data WHERE email = %s',
                    (email,),
                )
                existing = cursor.fetchone()

                if existing and existing[2]:
                    return _respond(request, {
                        'success': False,
                        'message': 'This email is already registered. Please log in instead.',
                    }, status.HTTP_409_CONFLICT, flash_category='error')

                if existing:
                    stored_email = existing[1]
                    cursor.execute(
                        'UPDATE login_data SET username = %s, organization = %s, '
                        'password = %s, created_at = NOW() WHERE email = %s',
                        (username, organization, hashed_password, stored_email),
                    )
                    email = stored_email
                else:
                    cursor.execute(
                        'INSERT INTO login_data '
                        '(email, username, organization, password, is_verified, created_at) '
                        'VALUES(%s, %s, %s, %s, false, NOW())',
                        (email, username, organization, hashed_password),
                    )

                _save_otp(cursor, email, hashed_otp)
                connection.commit()

        request.session['verify_user'] = username
        request.session['verify_email'] = email
        try:
            await send_otp_email(email, otp, username)
        except Exception:
            logger.exception('OTP email delivery failed for %s', email)

        logger.info('Signup OTP created for %s', email)
        message = 'Account registered! Check your email for the 6-digit OTP code.'
        return _respond(request, {
            'success': True,
            'message': message,
            'requires_otp': True,
        }, status.HTTP_201_CREATED, flash_category='success')

    except Exception:
        logger.exception('Signup failed')
        return _respond(request, {
            'success': False,
            'message': 'Signup failed due to a server error. Please try again later.',
        }, status.HTTP_500_INTERNAL_SERVER_ERROR, flash_category='error')


@login_route.post('/logout')
async def logout(request: Request):
    logger.info('Logout: %s', request.session.get('username', 'Unknown'))
    request.session.clear()
    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)


@login_route.post('/resend_otp')
async def resend_otp(request: Request):
    try:
        data = await _request_data(request)
        email = str(data.get('email') or request.session.get('verify_email') or '').strip()
        username = str(request.session.get('verify_user') or 'User')

        if not email:
            return _respond(request, {
                'success': False,
                'message': 'Session expired or email missing. Please sign up again.',
            }, status.HTTP_400_BAD_REQUEST, flash_category='error')

        otp = f'{secrets.randbelow(1_000_000):06d}'
        hashed_otp = generate_password_hash(otp)
        with closing(get_db_connection()) as connection:
            with connection.cursor() as cursor:
                _save_otp(cursor, email, hashed_otp)
                connection.commit()

        await send_otp_email(email, otp, username)
        logger.info('New OTP sent to %s', email)
        return _respond(request, {
            'success': True,
            'message': 'New OTP code sent to your email address!',
        }, flash_category='success')

    except Exception:
        logger.exception('Resend OTP failed')
        return _respond(request, {
            'success': False,
            'message': 'An error occurred while resending OTP. Please try again.',
        }, status.HTTP_500_INTERNAL_SERVER_ERROR, flash_category='error')
