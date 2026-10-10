const trialForm = document.querySelector('.trial-form');
const trialStatus = document.querySelector('#trial-status');
const trialPhone = document.querySelector('#phone');
const trialNames = [...trialForm.querySelectorAll('.trial-name-row input')];
const trialButton = trialForm.querySelector('button[type="submit"]');
const trialLabel = trialButton.querySelector('span');
const trialSitekey = document.querySelector('meta[name="turnstile-sitekey"]').content;
let trialToken = '';
let trialWidget;
let trialSending = false;
let trialComplete = false;

document.querySelector('[data-trial-year]').textContent = new Date().getFullYear();
const showTrialStatus = (message) => {
  trialStatus.textContent = message;
  trialStatus.hidden = false;
  trialStatus.focus();
};
const updateTrialButton = () => {
  trialButton.disabled = !trialToken || trialSending || trialComplete;
};
const validateTrialField = (input) => {
  if (input === trialPhone) {
    const digits = input.value.replace(/\D/g, '');
    const allowedCharacters = /^[+\d\s().-]+$/.test(input.value);
    input.setCustomValidity(allowedCharacters && digits.length >= 10 && digits.length <= 15
      ? '' : 'Lütfen geçerli bir telefon numarası gir.');
  } else if (trialNames.includes(input)) {
    input.setCustomValidity(input.value.trim() ? '' : 'Lütfen bu alanı doldur.');
  }
};
trialForm.addEventListener('input', (event) => {
  validateTrialField(event.target);
  if (!trialSending && !trialComplete) trialStatus.hidden = true;
});

// No configured key means no live submissions; local previews remain safe.
if (trialSitekey) {
  const script = document.createElement('script');
  script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
  script.async = true;
  script.addEventListener('load', () => {
    const compact = window.matchMedia('(max-width: 399px)');
    const renderSecurity = () => {
      if (trialComplete) return;
      if (trialWidget !== undefined) window.turnstile.remove(trialWidget);
      trialToken = '';
      updateTrialButton();
      trialWidget = window.turnstile.render('#trial-security', {
      sitekey: trialSitekey,
      action: 'trial',
      language: 'tr',
      size: compact.matches ? 'compact' : 'flexible',
      theme: 'light',
      callback: (token) => { trialToken = token; updateTrialButton(); },
      'expired-callback': () => { trialToken = ''; updateTrialButton(); },
      'error-callback': () => {
        trialToken = '';
        updateTrialButton();
        showTrialStatus('Güvenlik kontrolü yüklenemedi. Lütfen sayfayı yenile.');
      },
      });
    };
    renderSecurity();
    compact.addEventListener('change', renderSecurity);
    document.querySelector('#trial-preview').hidden = true;
  });
  script.addEventListener('error', () => showTrialStatus('Güvenlik kontrolü yüklenemedi. Lütfen sayfayı yenile.'));
  document.head.append(script);
}

trialForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (trialSending || trialComplete) return;
  [...trialNames, trialPhone].forEach(validateTrialField);
  if (!trialForm.reportValidity()) return;
  if (!trialToken) {
    showTrialStatus('Başvurmak için güvenlik kontrolünün tamamlanmasını bekle.');
    return;
  }
  const payload = Object.fromEntries(new FormData(trialForm));
  payload.token = trialToken;
  trialSending = true;
  updateTrialButton();
  trialForm.setAttribute('aria-busy', 'true');
  trialLabel.textContent = 'Gönderiliyor…';
  try {
    const response = await fetch(trialForm.action, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(25000),
    });
    const result = await response.json();
    if (!response.ok || result.ok !== true) {
      throw new Error(result.message || 'Başvurun gönderilemedi. Lütfen tekrar dene.');
    }
    trialComplete = true;
    trialForm.reset();
    showTrialStatus('Başvurun iletildi. Terra ekibi deneme üyeliğin için seninle iletişime geçecek.');
  } catch (error) {
    const message = error.name === 'TimeoutError' || error.name === 'TypeError' || error.name === 'SyntaxError'
      ? 'Gönderim sonucu doğrulanamadı. Tekrar başvurmadan önce lütfen Terra ile iletişime geç.'
      : error.message;
    showTrialStatus(message);
  } finally {
    trialSending = false;
    trialToken = '';
    trialForm.removeAttribute('aria-busy');
    trialLabel.textContent = trialComplete ? 'Başvurun iletildi' : 'Deneme üyeliğine başvur';
    if (trialWidget !== undefined) {
      if (trialComplete) {
        window.turnstile.remove(trialWidget);
        trialWidget = undefined;
        document.querySelector('#trial-security').hidden = true;
      } else {
        window.turnstile.reset(trialWidget);
      }
    }
    updateTrialButton();
  }
});
