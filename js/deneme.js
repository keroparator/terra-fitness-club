const trialForm = document.querySelector('.trial-form');
const trialStatus = document.querySelector('#trial-status');
const trialPhone = document.querySelector('#phone');
const trialNames = [...trialForm.querySelectorAll('input[type="text"]')];

// Bu sayfa yalnız tasarım önizlemesidir. Backend kurulana kadar veri gönderilmez.
trialForm.querySelector('button[type="submit"]').disabled = false;
document.querySelector('[data-trial-year]').textContent = new Date().getFullYear();

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
  trialStatus.hidden = true;
});

trialForm.addEventListener('submit', (event) => {
  event.preventDefault();
  [...trialNames, trialPhone].forEach(validateTrialField);
  if (!trialForm.reportValidity()) return;
  trialStatus.textContent = 'Form bilgilerin uygun. Bu bir tasarım önizlemesi; başvurun gönderilmedi. Gönderim bağlantısı kurulduğunda başvuru yapabileceksin.';
  trialStatus.hidden = false;
  trialStatus.focus();
});
