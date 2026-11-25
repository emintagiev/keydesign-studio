(() => {
  'use strict';
  const panel = document.querySelector('#question-panel');
  const button = document.querySelector('.contact-chat');
  const form = document.querySelector('#question-form');
  if (!panel || !button || !form || typeof panel.showModal !== 'function') return;
  const thread = document.querySelector('#chat-thread');
  const status = document.querySelector('#chat-status');
  const submit = form.querySelector('[type=submit]');
  const strings = {
    open: ['Задать вопрос','Ask a question'], title: ['Вопрос дизайнеру','Ask the designer'],
    hint: ['Ответ появится здесь. Вернитесь в этот чат с того же браузера.','Your reply will appear here. Return using the same browser.'],
    name: ['Имя и фамилия','Full name'], message: ['Ваш вопрос','Your message'],
    agree: ['Соглашаюсь на обработку данных в Netlify и передачу вопроса в рабочий Telegram студии.','I consent to processing my details on Netlify and sending my question to the studio’s work Telegram.'],
    policy: ['Политика конфиденциальности','Privacy policy'], send: ['Отправить','Send'], close: ['Закрыть','Close'],
    visitor: ['Вы','You'], studio: ['Студия','Studio'], sending: ['Отправляем…','Sending…'],
    sent: ['Вопрос доставлен.','Your message was delivered.'],
    error: ['Не удалось отправить. Попробуйте ещё раз.','Could not send. Please try again.'],
    readError: ['Не удалось обновить чат. Проверим снова автоматически.','Could not refresh the chat. We’ll try again automatically.'],
    offline: ['Нет связи с чатом. Ваш текст остался в форме. Попробуйте ещё раз или напишите Кристине напрямую.','Cannot connect to the chat. Your draft is still here. Try again or contact Kristina directly.'],
    wait: ['Пока не получили подтверждение. Можно повторить отправку этого сообщения.','Delivery hasn’t been confirmed yet. You can retry this message.'],
    rate: ['Много сообщений подряд. Попробуйте позже.','Too many messages. Please try again later.'],
    fallback: ['Написать Кристине в Telegram','Message Kristina on Telegram'],
    temporary: ['Чтобы увидеть ответ, оставьте эту вкладку открытой.','Keep this tab open to receive your reply.']
  };
  const t = k => strings[k][document.documentElement.lang === 'en' ? 1 : 0];
  const storageKey = 'kds.studio-chat.v1';
  const hex = bytes => Array.from(crypto.getRandomValues(new Uint8Array(bytes)), n => n.toString(16).padStart(2,'0')).join('');
  let saved = {};
  try {
    const data = JSON.parse(localStorage.getItem(storageKey));
    if (data && /^[0-9a-f]{64}$/.test(data.token) && data.expires > Date.now()) saved = data;
    else localStorage.removeItem(storageKey);
  } catch (_) {}
  let persistent = true;
  function persist() {
    saved.expires = Date.now() + 7 * 86400000;
    try { localStorage.setItem(storageKey, JSON.stringify(saved)); } catch (_) { persistent = false; }
  }
  const goal = name => {
    if (window.KDS_METRIKA_ID && typeof window.ym === 'function') {
      try { window.ym(window.KDS_METRIKA_ID,'reachGoal',name,{entry:'home_chat'}); } catch (_) {}
    }
  };
  let rows = [], busy = false, reading = false, statusKey = '', timer;
  function render() {
    document.querySelectorAll('[data-chat-copy]').forEach(el => { el.textContent = t(el.dataset.chatCopy); });
    panel.querySelector('.close-panel').setAttribute('aria-label',t('close'));
    if (!persistent) panel.querySelector('[data-chat-copy="hint"]').textContent = t('temporary');
    status.textContent = statusKey ? t(statusKey) : '';
    thread.replaceChildren(...rows.map(row => {
      const line = document.createElement('p'), author = document.createElement('strong');
      author.textContent = t(row.side) + ' · ';
      line.append(author, document.createTextNode(row.text));
      return line;
    }));
  }
  function say(key) {
    statusKey = key;
    status.textContent = key ? t(key) : '';
    document.querySelector('#chat-fallback').hidden = !['error','rate','wait','readError','offline'].includes(key);
  }
  async function api(action, extra={}) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), action === 'read' ? 8000 : 16000);
    try {
      const response = await fetch(window.KDS_BRIEF.chatEndpoint, {
        method:'POST', headers:{'Content-Type':'application/json'}, credentials:'omit', cache:'no-store',
        body:JSON.stringify({action, session:saved.token, ...extra}), signal:controller.signal
      });
      const body = await response.json();
      if (!response.ok || body.ok !== true) throw Object.assign(new Error('chat'), {status:response.status});
      return body;
    } finally { clearTimeout(timeout); }
  }
  async function refresh() {
    if (!panel.open || document.hidden || !saved.token || reading) return;
    reading = true;
    try {
      const result = await api('read');
      if (!Array.isArray(result.messages)) throw new Error('format');
      if (!panel.open || document.hidden) return;
      if (statusKey === 'readError') say('');
      if (JSON.stringify(result.messages) !== JSON.stringify(rows)) {
        rows = result.messages; render(); thread.scrollTop = thread.scrollHeight;
      }
      if (!busy && saved.pending && rows.some(row => row.request_id === saved.pending)) {
        delete saved.pending; delete saved.digest; persist(); say('sent');
      }
      if (rows.some(r=>r.side === 'visitor') && !saved.sent) { saved.sent=true; persist(); goal('home_chat_sent'); }
      if (rows.some(r=>r.side === 'studio') && !saved.seen) { saved.seen=true; persist(); goal('chat_reply_seen'); }
    } catch (_) { if (!busy && !statusKey) say('readError'); }
    finally { reading = false; }
  }
  button.addEventListener('click', () => {
    panel.showModal(); goal('home_chat_open'); render();
    refresh();
    clearInterval(timer); timer = setInterval(refresh, 12000);
  });
  panel.querySelector('.close-panel').addEventListener('click',()=>panel.close());
  panel.addEventListener('close',()=>{ clearInterval(timer); button.focus(); });
  document.addEventListener('visibilitychange',refresh);
  new MutationObserver(render).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy || !form.reportValidity()) return;
    const name = form.elements.fullname.value.trim(), text = form.elements.message.value.trim();
    if (!name || !text) { say('error'); return; }
    if (!saved.token) { saved.token = hex(32); persist(); }
    // Reuse the same ID after a lost response, also across a page refresh. Keep form values out of storage.
    const hash = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(name+'\n'+text))),n=>n.toString(16).padStart(2,'0')).join('');
    if (busy) return;
    if (saved.digest !== hash || !saved.pending) { saved.digest=hash; saved.pending=hex(16); persist(); }
    busy = true; submit.disabled = true; say('sending');
    try {
      await api('send',{id:saved.pending,name,text,consent:form.elements.consent.checked,company:form.elements.company.value});
      delete saved.pending; delete saved.digest;
      if (!saved.sent) { saved.sent = true; goal('home_chat_sent'); }
      persist(); form.elements.message.value=''; say('sent'); await refresh();
    } catch (err) { say(!navigator.onLine ? 'offline' : !err.status || err.status===409 || err.status===503 ? 'wait' : err.status===429 ? 'rate' : 'error'); }
    finally { busy=false; submit.disabled=false; }
  });
  render(); button.hidden=false;
})();
