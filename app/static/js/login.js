/**
 * Login & Signup Unified Single Webpage JavaScript — Business Inspector
 * Handles mode switching, password visibility, OTP flow, dynamic validation, and backend fetch requests.
 */

document.addEventListener('DOMContentLoaded', () => {
    initAuthModeSwitcher();
    initPasswordToggles();
    initLoginForm();
    initSignupForm();
    initAmbientCanvas();
    initSocialButtons();
});

/**
 * Helper error handling and flash alerts
 */
const showError = (group, errorElem, message) => {
    if (group) group.classList.add('has-error');
    if (errorElem) errorElem.textContent = message;
};

const clearError = (group, errorElem) => {
    if (group) group.classList.remove('has-error');
    if (errorElem) errorElem.textContent = '';
};

function showFlashMessage(message, category = 'error') {
    const container = document.getElementById('flash-container');
    if (!container) return;

    let iconSvg = '';
    if (category === 'error' || category === 'danger') {
        iconSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`;
    } else if (category === 'success') {
        iconSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>`;
    } else {
        iconSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`;
    }

    container.innerHTML = `
        <div class="flash-alert flash-${category}">
            <span class="flash-icon">${iconSvg}</span>
            <span class="flash-text">${message}</span>
        </div>
    `;
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Tab Mode Switcher (Sign In vs Create Account)
 */
function initAuthModeSwitcher() {
    const tabLogin = document.getElementById('tab-login');
    const tabSignup = document.getElementById('tab-signup');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const authTitle = document.getElementById('auth-title');
    const authSubtitle = document.getElementById('auth-subtitle');
    const headerBadgeText = document.getElementById('header-badge-text');
    const socialDividerText = document.getElementById('social-divider-text');
    const footerTextLogin = document.getElementById('footer-text-login');
    const footerTextSignup = document.getElementById('footer-text-signup');
    const gotoSignup = document.getElementById('goto-signup');
    const gotoLogin = document.getElementById('goto-login');

    if (!tabLogin || !tabSignup || !loginForm || !signupForm) return;

    const switchMode = (mode) => {
        if (mode === 'signup') {
            tabLogin.classList.remove('active');
            tabLogin.setAttribute('aria-selected', 'false');
            tabSignup.classList.add('active');
            tabSignup.setAttribute('aria-selected', 'true');

            loginForm.style.display = 'none';
            signupForm.style.display = 'flex';

            authTitle.textContent = 'Create Your Account';
            authSubtitle.textContent = 'Start inspecting data & predicting customer intelligence with AI';
            headerBadgeText.textContent = 'Free Account Registration';
            socialDividerText.textContent = 'OR SIGN UP WITH';

            footerTextLogin.style.display = 'none';
            footerTextSignup.style.display = 'block';
            document.title = 'Create Account — Business Inspector';
        } else {
            tabSignup.classList.remove('active');
            tabSignup.setAttribute('aria-selected', 'false');
            tabLogin.classList.add('active');
            tabLogin.setAttribute('aria-selected', 'true');

            signupForm.style.display = 'none';
            loginForm.style.display = 'flex';

            authTitle.textContent = 'Welcome Back';
            authSubtitle.textContent = 'Log in to view customer analytics, churn risk, and AI insights';
            headerBadgeText.textContent = 'Secure Access Portal';
            socialDividerText.textContent = 'OR SIGN IN WITH';

            footerTextSignup.style.display = 'none';
            footerTextLogin.style.display = 'block';
            document.title = 'Sign In — Business Inspector';
        }
    };

    tabLogin.addEventListener('click', () => switchMode('login'));
    tabSignup.addEventListener('click', () => switchMode('signup'));

    if (gotoSignup) gotoSignup.addEventListener('click', () => switchMode('signup'));
    if (gotoLogin) gotoLogin.addEventListener('click', () => switchMode('login'));
}

/**
 * Password Visibility Toggles
 */
function initPasswordToggles() {
    const setupToggle = (inputId, btnId) => {
        const input = document.getElementById(inputId);
        const btn = document.getElementById(btnId);
        if (!input || !btn) return;

        const eyeShow = btn.querySelector('.eye-show');
        const eyeHide = btn.querySelector('.eye-hide');

        btn.addEventListener('click', () => {
            const isPassword = input.getAttribute('type') === 'password';
            input.setAttribute('type', isPassword ? 'text' : 'password');

            if (isPassword) {
                if (eyeShow) eyeShow.style.display = 'none';
                if (eyeHide) eyeHide.style.display = 'block';
                btn.setAttribute('aria-label', 'Hide password');
            } else {
                if (eyeShow) eyeShow.style.display = 'block';
                if (eyeHide) eyeHide.style.display = 'none';
                btn.setAttribute('aria-label', 'Show password');
            }
        });
    };

    setupToggle('password', 'toggle-password');
    setupToggle('signup-password', 'toggle-signup-password');
}

/**
 * Login Form Handling & Client/Server Integration
 */
function initLoginForm() {
    const form = document.getElementById('login-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const emailGroup = document.getElementById('group-email');
    const passwordGroup = document.getElementById('group-password');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');
    const submitBtn = document.getElementById('submit-btn');
    const btnLabel = submitBtn ? submitBtn.querySelector('.btn-label') : null;
    const btnSpinner = document.getElementById('btn-spinner');
    const btnArrow = submitBtn ? submitBtn.querySelector('.btn-arrow') : null;

    if (!form) return;

    emailInput?.addEventListener('input', () => clearError(emailGroup, emailError));
    passwordInput?.addEventListener('input', () => clearError(passwordGroup, passwordError));

    const resetSubmitBtn = () => {
        if (submitBtn) submitBtn.disabled = false;
        if (btnLabel) btnLabel.textContent = 'Sign In';
        if (btnSpinner) btnSpinner.hidden = true;
        if (btnArrow) btnArrow.style.display = 'inline-block';
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        let isValid = true;
        const emailValue = emailInput.value.trim();
        const passwordValue = passwordInput.value.trim();

        if (!emailValue) {
            showError(emailGroup, emailError, 'Please enter your email or username');
            isValid = false;
        } else {
            clearError(emailGroup, emailError);
        }

        if (!passwordValue) {
            showError(passwordGroup, passwordError, 'Please enter your password');
            isValid = false;
        } else {
            clearError(passwordGroup, passwordError);
        }

        if (!isValid) {
            triggerShake();
            return;
        }

        if (submitBtn && btnLabel && btnSpinner) {
            submitBtn.disabled = true;
            btnLabel.textContent = 'Signing in...';
            btnSpinner.hidden = false;
            if (btnArrow) btnArrow.style.display = 'none';
        }

        try {
            const response = await fetch('/login/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    email: emailValue,
                    password: passwordValue
                })
            });

            const data = await response.json();

            if (data.success) {
                showFlashMessage(data.message || 'Login successful!', 'success');
                setTimeout(() => {
                    window.location.href = data.redirect_url || '/inspect';
                }, 500);
            } else {
                resetSubmitBtn();
                triggerShake();
                showFlashMessage(data.message || 'Invalid email or password.', 'error');
                
                if (data.redirect_to_verify) {
                    const tabSignup = document.getElementById('tab-signup');
                    const signupEmail = document.getElementById('signup-email');
                    if (signupEmail) signupEmail.value = data.email || emailValue;
                    if (tabSignup) tabSignup.click();

                    const btnGetOtp = document.getElementById('btn-get-otp');
                    const otpSection = document.getElementById('otp-section');
                    const signupSubmitBtn = document.getElementById('signup-submit-btn');

                    if (btnGetOtp) btnGetOtp.style.display = 'none';
                    if (otpSection) otpSection.style.display = 'flex';
                    if (signupSubmitBtn) signupSubmitBtn.style.display = 'flex';

                    showFlashMessage(data.message || 'Please enter the OTP sent to your email.', 'warning');
                }
            }
        } catch (err) {
            console.error('Login submit error:', err);
            resetSubmitBtn();
            triggerShake();
            showFlashMessage('A network or server error occurred. Please try again.', 'error');
        }
    });
}

/**
 * Signup Form & Get OTP Flow Handling
 */
function initSignupForm() {
    const form = document.getElementById('signup-form');
    const usernameInput = document.getElementById('signup-username');
    const emailInput = document.getElementById('signup-email');
    const orgInput = document.getElementById('signup-org');
    const passwordInput = document.getElementById('signup-password');
    const otpInput = document.getElementById('signup-otp');

    const usernameGroup = document.getElementById('group-signup-username');
    const emailGroup = document.getElementById('group-signup-email');
    const orgGroup = document.getElementById('group-signup-org');
    const passwordGroup = document.getElementById('group-signup-password');
    const otpGroup = document.getElementById('group-signup-otp');

    const usernameError = document.getElementById('signup-username-error');
    const emailError = document.getElementById('signup-email-error');
    const orgError = document.getElementById('signup-org-error');
    const passwordError = document.getElementById('signup-password-error');
    const otpError = document.getElementById('signup-otp-error');

    const btnGetOtp = document.getElementById('btn-get-otp');
    const btnOtpSpinner = document.getElementById('btn-otp-spinner');
    const btnOtpText = btnGetOtp ? btnGetOtp.querySelector('.btn-otp-text') : null;

    const otpSection = document.getElementById('otp-section');
    const signupSubmitBtn = document.getElementById('signup-submit-btn');
    const btnResendOtp = document.getElementById('btn-resend-otp');

    if (!form) return;

    usernameInput?.addEventListener('input', () => clearError(usernameGroup, usernameError));
    emailInput?.addEventListener('input', () => clearError(emailGroup, emailError));
    orgInput?.addEventListener('input', () => clearError(orgGroup, orgError));
    passwordInput?.addEventListener('input', () => clearError(passwordGroup, passwordError));
    otpInput?.addEventListener('input', () => clearError(otpGroup, otpError));

    let timerInterval = null;

    const formatTime = (totalSeconds) => {
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    };

    const startResendTimer = () => {
        let count = 300; // 5 minutes countdown
        if (btnResendOtp) {
            btnResendOtp.disabled = true;
            btnResendOtp.innerHTML = `Resend OTP (<span id="resend-timer">${formatTime(count)}</span>)`;
        }

        clearInterval(timerInterval);
        timerInterval = setInterval(() => {
            count--;
            const timerSpan = document.getElementById('resend-timer');
            if (timerSpan) timerSpan.textContent = formatTime(count);
            if (count <= 0) {
                clearInterval(timerInterval);
                if (btnResendOtp) {
                    btnResendOtp.disabled = false;
                    btnResendOtp.textContent = 'Resend OTP';
                }
            }
        }, 1000);
    };

    const resetGetOtpBtn = () => {
        if (btnGetOtp) btnGetOtp.disabled = false;
        if (btnOtpText) btnOtpText.textContent = 'Get OTP Verification Code';
        if (btnOtpSpinner) btnOtpSpinner.hidden = true;
    };

    // Step 1: Click "Get OTP"
    btnGetOtp?.addEventListener('click', async () => {
        let isValid = true;
        const usernameVal = usernameInput.value.trim();
        const emailVal = emailInput.value.trim();
        const orgVal = orgInput.value.trim();
        const passVal = passwordInput.value.trim();

        if (!usernameVal) {
            showError(usernameGroup, usernameError, 'Please enter a username');
            isValid = false;
        } else {
            clearError(usernameGroup, usernameError);
        }

        if (!emailVal || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailVal)) {
            showError(emailGroup, emailError, 'Please enter a valid email address');
            isValid = false;
        } else {
            clearError(emailGroup, emailError);
        }

        if (!orgVal) {
            showError(orgGroup, orgError, 'Please enter your organization name');
            isValid = false;
        } else {
            clearError(orgGroup, orgError);
        }

        if (!passVal || passVal.length < 6) {
            showError(passwordGroup, passwordError, 'Password must be at least 6 characters');
            isValid = false;
        } else {
            clearError(passwordGroup, passwordError);
        }

        if (!isValid) {
            triggerShake();
            return;
        }

        btnGetOtp.disabled = true;
        if (btnOtpText) btnOtpText.textContent = 'Sending OTP...';
        if (btnOtpSpinner) btnOtpSpinner.hidden = false;

        try {
            const response = await fetch('/signup/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    username: usernameVal,
                    email: emailVal,
                    organization: orgVal,
                    password: passVal
                })
            });

            const data = await response.json();

            if (data.success) {
                if (btnOtpSpinner) btnOtpSpinner.hidden = true;
                btnGetOtp.style.display = 'none';

                if (otpSection) otpSection.style.display = 'flex';
                if (signupSubmitBtn) signupSubmitBtn.style.display = 'flex';
                otpInput?.focus();

                showFlashMessage(data.message || 'OTP sent to your email address!', 'success');
                startResendTimer();
            } else {
                resetGetOtpBtn();
                triggerShake();
                showFlashMessage(data.message || 'Signup failed. Please try again.', 'error');
            }
        } catch (err) {
            console.error('Signup OTP request error:', err);
            resetGetOtpBtn();
            triggerShake();
            showFlashMessage('A network or server error occurred while sending OTP.', 'error');
        }
    });

    // Step 2: Resend OTP Click
    btnResendOtp?.addEventListener('click', async () => {
        if (btnResendOtp.disabled) return;
        btnResendOtp.disabled = true;
        btnResendOtp.textContent = 'Sending...';

        const emailVal = emailInput.value.trim();

        try {
            const response = await fetch('/resend_otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ email: emailVal })
            });

            const data = await response.json();

            if (data.success) {
                showFlashMessage(data.message || 'New OTP sent to your email!', 'success');
                startResendTimer();
            } else {
                btnResendOtp.disabled = false;
                btnResendOtp.textContent = 'Resend OTP';
                triggerShake();
                showFlashMessage(data.message || 'Failed to resend OTP.', 'error');
            }
        } catch (err) {
            console.error('Resend OTP error:', err);
            btnResendOtp.disabled = false;
            btnResendOtp.textContent = 'Resend OTP';
            triggerShake();
            showFlashMessage('Network error while resending OTP.', 'error');
        }
    });

    // Step 3: Final Form Submit (Verify OTP)
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const otpVal = otpInput.value.trim();
        const emailVal = emailInput.value.trim();

        if (!otpVal || otpVal.length !== 6) {
            showError(otpGroup, otpError, 'Please enter the 6-digit OTP sent to your email');
            triggerShake();
            return;
        }

        clearError(otpGroup, otpError);

        const submitBtn = document.getElementById('signup-submit-btn');
        const btnLabel = submitBtn ? submitBtn.querySelector('.btn-label') : null;
        const btnSpinner = document.getElementById('signup-btn-spinner');

        const resetSignupSubmitBtn = () => {
            if (submitBtn) submitBtn.disabled = false;
            if (btnLabel) btnLabel.textContent = 'Create Account & Complete Registration';
            if (btnSpinner) btnSpinner.hidden = true;
        };

        if (submitBtn && btnLabel && btnSpinner) {
            submitBtn.disabled = true;
            btnLabel.textContent = 'Verifying OTP...';
            btnSpinner.hidden = false;
        }

        try {
            const response = await fetch('/signup/verify_otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    otp: otpVal,
                    email: emailVal
                })
            });

            const data = await response.json();

            if (data.success) {
                showFlashMessage(data.message || 'Account verified successfully!', 'success');
                setTimeout(() => {
                    window.location.href = data.redirect_url || '/inspect';
                }, 600);
            } else {
                resetSignupSubmitBtn();
                showError(otpGroup, otpError, data.message || 'Invalid or expired OTP code');
                triggerShake();
                showFlashMessage(data.message || 'Verification failed.', 'error');
            }
        } catch (err) {
            console.error('Verify OTP error:', err);
            resetSignupSubmitBtn();
            triggerShake();
            showFlashMessage('Network error while verifying OTP.', 'error');
        }
    });
}

/**
 * Trigger Card Shake Animation on Error
 */
function triggerShake() {
    const card = document.querySelector('.auth-card');
    if (card) {
        card.style.animation = 'none';
        card.offsetHeight;
        card.style.animation = 'shake 0.4s ease';
    }
}

/**
 * Ambient Background Particles Canvas Animation
 */
function initAmbientCanvas() {
    const canvas = document.getElementById('login-bg-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const particleCount = Math.floor((width * height) / 25000) + 15;

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            radius: Math.random() * 2 + 1,
            vx: (Math.random() - 0.5) * 0.4,
            vy: (Math.random() - 0.5) * 0.4,
            alpha: Math.random() * 0.5 + 0.1,
            color: Math.random() > 0.3 ? '#00c853' : '#36B4B6'
        });
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        particles.forEach((p) => {
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0) p.x = width;
            if (p.x > width) p.x = 0;
            if (p.y < 0) p.y = height;
            if (p.y > height) p.y = 0;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = p.alpha;
            ctx.shadowBlur = 8;
            ctx.shadowColor = p.color;
            ctx.fill();
        });

        requestAnimationFrame(animate);
    }

    animate();
}

/**
 * Social Buttons Interaction
 */
function initSocialButtons() {
    const googleBtn = document.getElementById('social-google');
    const githubBtn = document.getElementById('social-github');

    if (googleBtn) googleBtn.addEventListener('click', () => console.log('Google Auth click'));
    if (githubBtn) githubBtn.addEventListener('click', () => console.log('GitHub Auth click'));
}

// Add Shake Animation dynamically
const styleSheet = document.createElement('style');
styleSheet.textContent = `
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    20%, 60% { transform: translateX(-8px); }
    40%, 80% { transform: translateX(8px); }
}
`;
document.head.appendChild(styleSheet);
