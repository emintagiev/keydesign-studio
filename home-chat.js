(() => {
  'use strict';
  const panel = document.querySelector('#question-panel');
  const form = document.querySelector('#question-form');
  if (!panel || !form) return;
  const staff = panel.hasAttribute('data-staff');
  const launch = document.querySelector('.contact-chat');
  if (!staff && (!launch || !panel.showModal)) return;
  const thread = panel.querySelector('#chat-thread');
  const scroller = panel.querySelector('.chat-scroll');
  const hint = panel.querySelector('.chat-intro');
  const waiting = panel.querySelector('#chat-waiting');
  const status = panel.querySelector('#chat-status');
  const field = form.elements.message;
  const submit = form.querySelector('[type=submit]');
  const consent = form.elements.consent;
  const fallback = form.querySelector('#chat-fallback');
  const strings = {
    open:['Задать вопрос','Ask a question'],
    title:staff ? ['Диалог с посетителем','Visitor conversation'] : ['Чат с дизайнером','Chat with a designer'],
    hint:staff ? ['Сообщения посетителя появятся здесь.','Visitor messages will appear here.'] :
      ['Что вы хотите узнать о своём проекте? Дизайнер ответит в этом чате.','What would you like to know about your project? A designer will reply here.'],
    agree:['Согласен на обработку сообщений в Netlify и передачу в рабочий Telegram студии.','I consent to processing my messages on Netlify and sending them to the studio’s work Telegram.'],
    policy:['Политика конфиденциальности','Privacy policy'], close:['Закрыть','Close'],
    visitor:staff ? ['Посетитель','Visitor'] : ['Вы','You'], studio:['Студия','Studio'],
    message:['Напишите сообщение…','Write a message…'], send:['Отправить сообщение','Send message'],
    log:['Переписка','Conversation'], waiting:['Доставлено. Ожидаем ответа дизайнера.','Delivered. Waiting for a designer to reply.'],
    sending:['Отправляем…','Sending…'], readError:['Не удалось обновить чат. Пробуем снова.','Could not refresh. Trying again.'],
    error:['Не удалось отправить. Попробуйте ещё раз.','Could not send. Please try again.'],
    wait:['Доставка пока не подтверждена. Можно повторить отправку.','Delivery is unconfirmed. You can try sending again.'],
    rate:['Много сообщений подряд. Попробуйте позже.','Too many messages. Try again later.'],
    denied:['Ссылка недействительна. Откройте чат из свежего сообщения рабочего бота.','This link is invalid or expired. Open a recent notification in the work bot.'],
    fallback:['Написать Кристине в Telegram','Message Kristina on Telegram'],
    temporary:['Чтобы увидеть ответ, оставьте эту вкладку открытой.','Keep this tab open to receive your reply.']
  };
  const lang = () => document.documentElement.lang === 'en' ? 1 : 0;
  const t = key => strings[key][lang()];
  const hex = length => Array.from(crypto.getRandomValues(new Uint8Array(length)), n=>n.toString(16).padStart(2,'0')).join('');
  const key = 'kds.studio-chat.v1';
  let saved = {}, ticket = '', persistent = true;
  if (staff) {
    const fragment = location.hash.slice(1);
    try {
      if (fragment) sessionStorage.setItem('kds.staff.ticket',fragment);
      ticket = fragment || sessionStorage.getItem('kds.staff.ticket') || '';
    } catch { ticket = fragment; }
    if (fragment) history.replaceState(null,'',location.pathname);
  } else {
    try {
      const session = JSON.parse(localStorage.getItem(key));
      if (session?.expires > Date.now() && /^[a-f0-9]{64}$/.test(session.token)) saved = session;
    } catch {}
  }
  function persist() {
    if (staff) return;
    saved.expires = Date.now()+7*86400000;
    try { localStorage.setItem(key,JSON.stringify(saved)); } catch { persistent=false; }
  }
  function goal(name) {
    if (!staff && window.KDS_METRIKA_ID && typeof window.ym === 'function') {
      try { window.ym(window.KDS_METRIKA_ID,'reachGoal',name,{entry:'home_chat'}); } catch {}
    }
  }
  let rows=[], busy=false, locked=false, reading=false, revision=0, timer, statusKey='';
  let staffPending, staffText;
  function say(value) {
    statusKey=value; status.textContent=value ? t(value) : '';
    if (fallback) fallback.hidden=!['wait','error','rate','readError'].includes(value);
  }
  function render() {
    panel.querySelectorAll('[data-chat-copy]').forEach(el=>{el.textContent=t(el.dataset.chatCopy);});
    if (launch) launch.querySelector('[data-chat-copy]').textContent=t('open');
    panel.querySelector('.close-panel')?.setAttribute('aria-label',t('close'));
    submit.setAttribute('aria-label',t('send'));
    field.placeholder=t('message'); field.setAttribute('aria-label',t('message'));
    thread.setAttribute('aria-label',t('log'));
    if (consent) {
      form.querySelector('#chat-consent').hidden=!!saved.agreed;
      consent.required=!saved.agreed;
    }
    hint.hidden=rows.length>0 && persistent;
    if (!persistent) hint.textContent=t('temporary');
    waiting.hidden=staff || rows.at(-1)?.side !== 'visitor';
    say(statusKey);
    thread.replaceChildren(...rows.map(row=>{
      const bubble=document.createElement('div'), meta=document.createElement('small'), text=document.createElement('p');
      bubble.className='chat-bubble '+row.side;
      const time=Number.isFinite(row.created) ? new Date(row.created).toLocaleTimeString(lang()?'en-GB':'ru-RU',{hour:'2-digit',minute:'2-digit'}) : '';
      meta.textContent=t(row.side)+(time?' · '+time:''); text.textContent=row.text;
      bubble.append(meta,text); return bubble;
    }));
  }
  async function api(action, data={}) {
    const controller=new AbortController(), timeout=setTimeout(()=>controller.abort(), action.endsWith('read')?10000:18000);
    try {
      const response=await fetch(window.KDS_BRIEF.chatEndpoint,{
        method:'POST',credentials:'omit',cache:'no-store',signal:controller.signal,
        headers:{'Content-Type':'application/json'},body:JSON.stringify({action,...(staff?{ticket}:{session:saved.token}),...data})
      });
      const body=await response.json();
      if (!response.ok || !body.ok) throw Object.assign(new Error('chat'),{status:response.status});
      return body;
    } finally { clearTimeout(timeout); }
  }
  function deny() {
    locked=true; field.disabled=true; submit.disabled=true; clearInterval(timer); say('denied');
  }
  function setRows(messages,forceScroll=false) {
    if (JSON.stringify(messages)===JSON.stringify(rows)) return;
    const nearBottom=scroller.scrollHeight-scroller.scrollTop-scroller.clientHeight<60;
    rows=messages; render();
    if (nearBottom || forceScroll) scroller.scrollTop=scroller.scrollHeight;
  }
  async function refresh() {
    if ((!staff && (!panel.open || !saved.token)) || document.hidden || locked || reading || busy) return;
    reading=true;
    const version=revision;
    try {
      const {messages}=await api(staff?'staff_read':'read');
      if (version!==revision || !Array.isArray(messages)) return;
      if (statusKey==='readError') say('');
      if (!staff && saved.pending && messages.some(row=>row.request_id===saved.pending)) {
        // The server accepted a message even though its original response was lost.
        const delivered=messages.find(row=>row.request_id===saved.pending);
        if (field.value.trim()===delivered.text) field.value='';
        saved.agreed=true; delete saved.pending; delete saved.digest; persist(); say('');
      }
      if (!staff && messages.some(r=>r.side==='visitor') && !saved.sent) { saved.sent=true; persist(); goal('home_chat_sent'); }
      if (!staff && messages.some(r=>r.side==='studio') && !saved.seen) { saved.seen=true; persist(); goal('chat_reply_seen'); }
      setRows(messages);
    } catch (err) {
      if (staff && err.status===403) deny();
      else if (!busy && !statusKey) say('readError');
    } finally { reading=false; }
  }
  function start() { clearInterval(timer); timer=setInterval(refresh,7500); refresh(); }
  if (staff) {
    if (/^[0-9a-f]{64}$/.test(ticket)) start(); else deny();
  } else {
    launch.hidden=false;
    launch.addEventListener('click',()=>{panel.showModal(); goal('home_chat_open'); start();});
    panel.querySelector('.close-panel').addEventListener('click',()=>panel.close());
    panel.addEventListener('close',()=>{clearInterval(timer);launch.focus();});
  }
  document.addEventListener('visibilitychange',refresh);
  new MutationObserver(render).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
  field.addEventListener('keydown',event=>{
    if (event.key==='Enter' && !event.shiftKey && !event.isComposing && matchMedia('(pointer:fine)').matches) {
      event.preventDefault(); form.requestSubmit();
    }
  });
  form.addEventListener('submit',async event=>{
    event.preventDefault();
    const text=field.value.trim();
    if (busy || locked || !text || !form.reportValidity()) return;
    busy=true; revision++; submit.disabled=true; field.readOnly=true; say('sending');
    try {
      let id;
      if (staff) {
        if (!staffPending || staffText!==text) {staffPending=hex(16);staffText=text;}
        id=staffPending; await api('staff_reply',{id,text});
        staffPending=staffText=undefined;
      } else {
        if (!saved.token) saved.token=hex(32);
        const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text))),n=>n.toString(16).padStart(2,'0')).join('');
        if (!saved.pending || saved.digest!==hash) {saved.pending=hex(16);saved.digest=hash;}
        persist(); id=saved.pending;
        await api('send',{id,text,consent:!!saved.agreed || consent.checked,company:form.elements.company.value});
        delete saved.pending; delete saved.digest; saved.agreed=true;
        if (!saved.sent) {saved.sent=true;goal('home_chat_sent');}
        persist();
      }
      field.value=''; say('');
      setRows([...rows,{side:staff?'studio':'visitor',text,request_id:staff?null:id,created:Date.now()}],true);
    } catch (err) {
      if (staff && err.status===403) deny();
      else say(err.status===429?'rate':!err.status || err.status===409 || err.status===503?'wait':'error');
    } finally {busy=false;submit.disabled=locked;field.readOnly=false;if (!statusKey) refresh();}
  });
  render();
})();
