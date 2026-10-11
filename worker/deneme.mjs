import { EmailMessage } from 'cloudflare:email';

const origins = new Set(['https://www.terrafitnessclub.com', 'https://terrafitnessclub.com']);
const recipient = 'terrafitnessclub1@gmail.com';
const reply = (status, message, origin) => new Response(JSON.stringify({ ok: status === 200, message }), {
  status,
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    ...(origins.has(origin) ? { 'Access-Control-Allow-Origin': origin, Vary: 'Origin' } : {}),
  },
});
const encode = (text) => btoa(String.fromCharCode(...new TextEncoder().encode(text)));

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin');
    if (new URL(request.url).pathname !== '/api/deneme') return reply(404, 'Sayfa bulunamadı.', origin);
    if (!origins.has(origin)) return reply(403, 'Lütfen Terra web sitesindeki formu kullan.', origin);
    if (request.method === 'OPTIONS') return new Response(null, {
      status: 204,
      headers: { 'Access-Control-Allow-Origin': origin, 'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type', Vary: 'Origin' },
    });
    if (request.method !== 'POST') return reply(405, 'Bu işlem desteklenmiyor.', origin);
    if (!env.EMAIL || !env.TURNSTILE_SECRET || !env.SENDER_EMAIL) {
      return reply(503, 'Başvuru gönderimi şu anda kullanılamıyor. Lütfen daha sonra tekrar dene.', origin);
    }
    if (!request.headers.get('Content-Type')?.startsWith('application/json')) {
      return reply(415, 'Başvuru biçimi geçersiz.', origin);
    }
    let data;
    try {
      // Read a bounded body even if Content-Length is absent or incorrect.
      const reader = request.body?.getReader();
      if (!reader) return reply(400, 'Başvuru bilgileri eksik.', origin);
      let size = 0;
      const chunks = [];
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        size += value.byteLength;
        if (size > 8192) { await reader.cancel(); return reply(413, 'Başvuru çok uzun.', origin); }
        chunks.push(value);
      }
      const bytes = new Uint8Array(size);
      let offset = 0;
      for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
      data = JSON.parse(new TextDecoder().decode(bytes));
    } catch { return reply(400, 'Başvuru bilgileri okunamadı.', origin); }
    if (!data || typeof data !== 'object' || Array.isArray(data)) return reply(400, 'Başvuru bilgileri geçersiz.', origin);
    const clean = (key, max) => typeof data[key] === 'string' && data[key].length <= max
      && !/[\u0000-\u001f\u007f]/.test(data[key]) ? data[key].trim() : '';
    const firstName = clean('firstName', 60);
    const lastName = clean('lastName', 60);
    const phone = clean('phone', 24);
    const email = clean('email', 254);
    const token = clean('token', 2048);
    if (data.website || !firstName || !lastName || !/^[+\d ().-]+$/.test(phone)
      || phone.replace(/\D/g, '').length < 10 || phone.replace(/\D/g, '').length > 15
      || !/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(email) || !token) {
      return reply(400, 'Lütfen bilgilerini ve güvenlik kontrolünü tamamla.', origin);
    }
    let verification;
    try {
      const result = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
        method: 'POST',
        body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: token,
          remoteip: request.headers.get('CF-Connecting-IP') || '' }),
        signal: AbortSignal.timeout(10000),
      });
      if (!result.ok) throw new Error('Verification unavailable');
      verification = await result.json();
    } catch { return reply(503, 'Güvenlik kontrolü tamamlanamadı. Lütfen tekrar dene.', origin); }
    if (!verification.success || !['www.terrafitnessclub.com', 'terrafitnessclub.com'].includes(verification.hostname)
      || verification.action !== 'trial') return reply(400, 'Güvenlik kontrolünü yenileyip tekrar dene.', origin);
    const timestamp = new Date().toLocaleString('tr-TR', { timeZone: 'Europe/Istanbul' });
    const text = `Yeni 1 günlük deneme üyeliği başvurusu\n\nİsim: ${firstName}\nSoyisim: ${lastName}\nTelefon: ${phone}\nE-posta: ${email}\nBaşvuru zamanı: ${timestamp} (Türkiye)\n\nBu bir başvurudur; üyelik veya randevu onayı değildir.`;
    const sender = env.SENDER_EMAIL;
    if (!/^[a-z0-9._+-]+@(?:[a-z0-9-]+\.)*terrafitnessclub\.com$/i.test(sender)) {
      return reply(503, 'Başvuru gönderimi şu anda kullanılamıyor.', origin);
    }
    const raw = [`From: Terra Fitness Club <${sender}>`, `To: ${recipient}`, `Reply-To: ${email}`,
      `Subject: =?UTF-8?B?${encode(`Yeni deneme üyeliği — ${firstName} ${lastName}`)}?=`,
      'MIME-Version: 1.0', 'Content-Type: text/plain; charset=UTF-8', 'Content-Transfer-Encoding: base64',
      '', encode(text).match(/.{1,76}/g).join('\r\n')].join('\r\n');
    try {
      await env.EMAIL.send(new EmailMessage(sender, recipient, raw));
    } catch {
      // Never log applicant details or return provider diagnostics to the browser.
      return reply(502, 'Başvurun gönderilemedi. Lütfen daha sonra tekrar dene.', origin);
    }
    return reply(200, 'Başvurun iletildi. Terra ekibi deneme üyeliğin için seninle iletişime geçecek.', origin);
  },
};
