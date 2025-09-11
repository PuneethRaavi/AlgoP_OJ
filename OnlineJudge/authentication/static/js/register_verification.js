// OTP resend & timer script (clean version)
// Handles: toast notifications, countdown timer, resend action, OTP input formatting & auto-submit.

document.addEventListener('DOMContentLoaded', () => {
  const resendBtn = document.getElementById('resend-otp-btn');
  if (!resendBtn) return;

  const verifyUrl = resendBtn.getAttribute('data-verify-url');
  const emailValue = resendBtn.getAttribute('data-email') || '';
  const resendLabel = document.getElementById('resend-label');
  const otpInput = document.getElementById('id_otp');
  let countdown = 30;
  let intervalId = null;
  let toastTimer = null;

  // Toast helpers
  function hideToast() {
    const toast = document.getElementById('otp-toast');
    if (toast) {
      toast.classList.remove('translate-x-0');
      toast.classList.add('translate-x-full');
    }
  }
  function showToast(title, msg, type = 'success') {
    const toast = document.getElementById('otp-toast');
    if (!toast) return;
    document.getElementById('toast-title').textContent = title;
    document.getElementById('toast-message').textContent = msg;
    const successIcon = document.getElementById('success-icon');
    const errorIcon = document.getElementById('error-icon');
    if (type === 'success') { successIcon.classList.remove('hidden'); errorIcon.classList.add('hidden'); }
    else { errorIcon.classList.remove('hidden'); successIcon.classList.add('hidden'); }
    toast.classList.remove('translate-x-full');
    toast.classList.add('translate-x-0');
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(hideToast, 4000);
  }
  const closeBtn = document.getElementById('toast-close');
  if (closeBtn) closeBtn.addEventListener('click', () => { hideToast(); if (toastTimer) clearTimeout(toastTimer); });

  function startTimer() {
    if (intervalId) clearInterval(intervalId);
    countdown = 30;
    resendBtn.disabled = true;
    const timerEl = document.getElementById('timer');
    if (timerEl) timerEl.textContent = ` (${countdown}s)`;
    intervalId = setInterval(() => {
      countdown--;
      if (countdown > 0) {
        if (timerEl) timerEl.textContent = ` (${countdown}s)`;
      } else {
        clearInterval(intervalId);
        intervalId = null;
        if (timerEl) timerEl.textContent = '';
        resendBtn.disabled = false;
      }
    }, 1000);
  }

  // OTP input formatting & auto-submit at 6 digits
  if (otpInput) {
    otpInput.addEventListener('input', e => {
      let v = e.target.value.replace(/\D/g, '').slice(0, 6);
      e.target.value = v;
      if (v.length === 6) e.target.form.submit();
    });
    otpInput.focus();
  }

  // Start timer if no server error messages are present
  const hasErrors = document.querySelector('.bg-red-100, .text-red-600, .text-red-400');
  if (!hasErrors) startTimer(); else resendBtn.disabled = false;

  // Resend action
  resendBtn.addEventListener('click', e => {
    e.preventDefault();
    if (!verifyUrl) { showToast('Config Error', 'Missing verification URL.', 'error'); return; }
    if (resendLabel) resendLabel.textContent = 'Sending...';
    resendBtn.disabled = true;
    const timerEl = document.getElementById('timer');
    if (timerEl) timerEl.textContent = '';

    fetch(verifyUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: new URLSearchParams({ action: 'resend', email: emailValue, purpose: 'registration' })
    })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          showToast('OTP Sent', data.message || 'Verification code sent.', 'success');
          setTimeout(() => { if (resendLabel) resendLabel.textContent = 'Resend Code'; startTimer(); }, 900);
        } else {
          if (resendLabel) resendLabel.textContent = 'Resend Code';
          resendBtn.disabled = false;
          showToast('Send Failed', data.message || 'Could not send code.', 'error');
        }
      })
      .catch(() => {
        if (resendLabel) resendLabel.textContent = 'Resend Code';
        resendBtn.disabled = false;
        showToast('Network Error', 'Please try again.', 'error');
      });
  });
});