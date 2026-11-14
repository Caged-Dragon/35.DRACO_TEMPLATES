(() => {
  const form = document.querySelector('#authForm');
  const password = document.querySelector('#password');
  const toggle = document.querySelector('.toggle-password');
  const status = document.querySelector('#status');
  toggle.addEventListener('click', () => {
    const reveal = password.type === 'password';
    password.type = reveal ? 'text' : 'password';
    toggle.textContent = reveal ? 'HIDE' : 'SHOW';
    toggle.setAttribute('aria-label', reveal ? 'Hide password' : 'Show password');
    toggle.setAttribute('aria-pressed', String(reveal));
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    const identifier = document.querySelector('#identifier').value.trim();
    const secret = password.value;
    status.className = 'status';
    if (!identifier) { status.textContent = 'Enter your email address or mobile number.'; status.classList.add('error'); document.querySelector('#identifier').focus(); return; }
    if (secret.length < 8) { status.textContent = 'Enter a password with at least 8 characters.'; status.classList.add('error'); password.focus(); return; }
    status.textContent = 'UI preview only — connect this form to your own secure sign-in endpoint.';
    status.classList.add('success');
  });
  document.querySelector('#forgotLink').addEventListener('click', event => {
    event.preventDefault(); status.className = 'status'; status.textContent = 'Password recovery link placeholder — connect your recovery flow.';
  });
  document.querySelector('#createLink').addEventListener('click', event => {
    event.preventDefault(); status.className = 'status'; status.textContent = 'Account creation link placeholder — connect your registration flow.';
  });
})();
