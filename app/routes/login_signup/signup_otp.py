from ..extensions import mail, Message

def send_otp_email(email, otp, username):
    print(f"📧 Sending OTP email → {email} (user: {username})")

    msg = Message(
        subject    = "Your OTP for Business Inspector Verification",
        recipients = [email],
        html       = f"""
<html>
<head>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
      background:#f3f4f6; margin:0; padding:0; color:#1f2937;
    }}
    .wrap  {{ max-width:600px; margin:0 auto; background:#fff; }}
    .hdr   {{
      background: linear-gradient(135deg,#667eea,#764ba2);
      color:#fff; padding:40px 30px; text-align:center;
    }}
    .hdr h1 {{ margin:0 0 8px; font-size:26px; }}
    .hdr p  {{ margin:0; opacity:.9; font-size:15px; }}
    .body   {{ padding:36px 30px; }}
    .otp-box {{
      text-align:center; padding:28px;
      background:linear-gradient(135deg,#f0fdf4,#dcfce7);
      border-radius:12px; margin:24px 0;
    }}
    .otp-label {{
      font-size:13px; font-weight:600; color:#6b7280;
      text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;
    }}
    .otp-code  {{ font-size:46px; font-weight:900; color:#667eea; letter-spacing:10px; }}
    .note {{
      background:#f9fafb; border-left:4px solid #667eea;
      padding:16px; border-radius:8px; color:#4b5563; font-size:14px;
    }}
    .warn {{
      background:linear-gradient(135deg,#fef3c7,#fde68a);
      border-left:4px solid #f59e0b;
      padding:16px; border-radius:8px; margin-top:16px;
      color:#78350f; font-size:14px;
    }}
    .ftr {{
      text-align:center; padding:24px;
      background:#f9fafb; color:#6b7280; font-size:13px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hdr">
      <h1>🔐 Email Verification</h1>
      <p>Entrepreneurs and Investors Smart Connect</p>
    </div>
    <div class="body">
      <p>Hello <strong>{username}</strong>,</p>
      <p>Welcome to Business Inspector! Use the code below to verify your email address.</p>
      <div class="otp-box">
        <div class="otp-label">Your One-Time Password</div>
        <div class="otp-code">{otp}</div>
      </div>
      <div class="note">
        This OTP is valid for <strong>10 minutes</strong>.
        Enter it on the verification page to complete registration.
      </div>
      <div class="warn">
        ⚠️ Didn't request this? You can safely ignore this email.
      </div>
    </div>
    <div class="ftr">
      <strong>Business Inspector Team</strong><br>AI-Powered Customer Intelligence
    </div>
  </div>
</body>
</html>"""
    )
    mail.send(msg)
    print(f"[OK] OTP email dispatched -> {email}")