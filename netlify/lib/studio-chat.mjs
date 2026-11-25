import { createHmac, randomBytes, timingSafeEqual } from 'node:crypto';

const HOUR = 3600000;
const WEEK = 168 * HOUR;
const hexSession = /^[a-f0-9]{64}$/;
const hexEvent = /^[a-f0-9]{32}$/;
const origins = new Set(['https://www.keydesign.studio', 'https://keydesign.studio',
  'https://keydesign-studio-xxxxx.web.app', 'https://keydesign-studio-xxxxx.firebaseapp.com']);

const digest = (token, value) => createHmac('sha256', token).update(value).digest('hex');
const headers = { 'Cache-Control': 'no-store', 'Vary': 'Origin', 'X-Robots-Tag': 'noindex' };

function json(status, data, origin) {
  return Response.json({ok:status === 200, ...data}, {status, headers:{
    ...headers, ...(origin && origins.has(origin) ? {'Access-Control-Allow-Origin':origin} : {})
  }});
}

async function addEvent(store, key, event) {
  const expires = event.created + WEEK;
  // Publish the cleanup marker first so a partially failed write cannot leave data without an expiry.
  await store.set('expiry/' + Math.ceil(expires / HOUR) + '/' + key, '');
  return store.setJSON(key, event, {onlyIfNew:true, metadata:{expires}});
}

async function allow(store, scope, period, limit, now) {
  const end = (Math.floor(now / period) + 1) * period;
  const key = 'limit/' + end + '/' + scope;
  for (let attempt = 0; attempt < 8; attempt++) {
    const prev = await store.getWithMetadata(key, {type:'json'});
    const count = prev?.data ?? 0;
    if (count >= limit) return false;
    const written = await store.setJSON(key, count + 1, prev ? {onlyIfMatch:prev.etag} : {onlyIfNew:true});
    if (written.modified) return true;
  }
  return false;
}

function existing(event) {
  return event?.state === 'sent' ? [200,{delivery:'sent'}] : [409,{delivery:'pending'}];
}

async function readRoom(store, room, now) {
  const {blobs} = await store.list({prefix:'room/' + room + '/'});
  const events = [];
  for (let i = 0; i < blobs.length; i += 20) {
    const batch = await Promise.all(blobs.slice(i,i+20).map(({key}) => store.get(key,{type:'json'})));
    for (const e of batch) if (e?.state === 'sent' && e.created + WEEK > now) events.push(e);
  }
  return events.sort((a,b) => a.created - b.created).slice(-120).map(e => ({
    side:e.side, text:e.text, created:e.created, request_id:e.side === 'visitor' ? e.id : null
  }));
}

async function visitor(data, ip, {store,token,targets,dispatch}, now) {
  if (typeof data.session !== 'string' || !hexSession.test(data.session)) return [422,{}];
  const room = digest(token,data.session);
  if (data.action === 'read') return [200,{messages:await readRoom(store,room,now)}];
  const text = typeof data.text === 'string' ? data.text.trim() : '';
  if (data.action !== 'send' || typeof data.id !== 'string' || !hexEvent.test(data.id) ||
      !text || text.length > 1500 || data.company || data.consent !== true) return [422,{}];
  const key = 'room/' + room + '/' + data.id;
  const previous = await store.get(key,{type:'json'});
  if (previous) return existing(previous);
  if (!await allow(store,digest(token,'ip:'+ip),600000,12,now) ||
      !await allow(store,'site',HOUR,100,now)) return [429,{}];
  const event = {side:'visitor', id:data.id, state:'pending', text, created:now};
  const claim = await addEvent(store,key,event);
  if (!claim.modified) return existing(await store.get(key,{type:'json'}));
  // A capability is delivered only in the work bot's inline button. Only its digest is stored.
  const ticket = randomBytes(32).toString('hex');
  const reference = {room, id:data.id, created:now};
  await addEvent(store,'ticket/' + digest(token,ticket),reference);
  const link = staffURL + ticket;
  const notice = 'Сообщение с сайта\n\n' + text + '\n\nЧтобы ответить здесь, нажмите «Ответить».';
  const results = await Promise.allSettled(targets.map(async chatId => {
    const messageId = await dispatch(token,chatId,notice,link);
    if (!Number.isSafeInteger(messageId) || messageId <= 0) return messageId === false ? false : null;
    await addEvent(store,telegramKey(token,chatId,messageId),reference);
    return true;
  }));
  if (results.some(r => r.status === 'fulfilled' && r.value === true)) {
    await store.setJSON(key,{...event,state:'sent'},{metadata:{expires:now+WEEK}});
    return [200,{delivery:'sent'}];
  }
  if (results.every(r => r.status === 'fulfilled' && r.value === false)) {
    await store.delete(key);
    return [502,{}];
  }
  return [409,{delivery:'unknown'}];
}

const staffURL = 'https://www.keydesign.studio/studio-chat#';
const telegramKey = (token,chatId,messageId) => 'telegram/' + digest(token,chatId+':'+messageId);

async function ticketReference(ticket, {store,token}, now) {
  if (typeof ticket !== 'string' || !hexSession.test(ticket)) return null;
  const ref = await store.get('ticket/'+digest(token,ticket),{type:'json'});
  return ref && ref.created + WEEK > now ? ref : null;
}

async function staff(data, deps, now) {
  const ref = await ticketReference(data.ticket,deps,now);
  if (!ref) return [403,{}];
  const {store} = deps;
  if (data.action === 'staff_read') return [200,{messages:await readRoom(store,ref.room,now)}];
  const text = typeof data.text === 'string' ? data.text.trim() : '';
  if (!text || text.length > 1500 || typeof data.id !== 'string' || !hexEvent.test(data.id)) return [422,{}];
  await addEvent(store,'room/'+ref.room+'/staff-'+data.id,{side:'studio',state:'sent',text,created:now});
  return [200,{delivery:'sent'}];
}

async function acceptReply(data, {store,token,targets}, now) {
  const m = data.message;
  const parent = m?.reply_to_message;
  if (!targets.includes(String(m?.chat?.id)) || !m?.message_id || !m.from || m.from.is_bot ||
      !parent?.from?.is_bot || String(parent.from.id) !== token.split(':')[0] ||
      typeof m.text !== 'string' || !m.text.trim()) return;
  if (!Number.isSafeInteger(parent.date) || parent.date*1000 + WEEK <= now) return;
  let ref = await store.get(telegramKey(token,m.chat.id,parent.message_id),{type:'json'});
  if (!ref) {
    const link = parent.reply_markup?.inline_keyboard?.flat().find(button=>button.url?.startsWith(staffURL))?.url;
    if (link) ref = await ticketReference(link.slice(staffURL.length),{store,token},now);
  }
  if (!ref) {
    const legacy = /^Вопрос с сайта #([a-f0-9]{64})(?:\.([a-f0-9]{32}))?\n/.exec(parent.text || '');
    if (!legacy) return;
    ref = {room:legacy[1],id:legacy[2]};
  }
  const {room,id} = ref;
  if (id) {
    const key = 'room/' + room + '/' + id;
    const question = await store.get(key,{type:'json'});
    if (!question || question.created + WEEK <= now) return;
    if (question.state !== 'sent') await store.setJSON(key,{...question,state:'sent'},
      {metadata:{expires:question.created+WEEK}});
  }
  // Signed replies to the previous notification format can still reach the same browser session.
  const key = 'room/' + room + '/reply-' + digest(token,m.chat.id+':'+m.message_id);
  await addEvent(store,key,{side:'studio',state:'sent',text:m.text.trim().slice(0,4096),created:now});
}

export async function handleChat(req, context, deps) {
  const origin = req.headers.get('Origin');
  const webhook = new URL(req.url).searchParams.has('webhook');
  if (!webhook && !origins.has(origin)) return json(403,{},origin);
  if (!webhook && req.method === 'OPTIONS') return new Response(null,{status:204,headers:{
    ...headers,'Access-Control-Allow-Origin':origin,'Access-Control-Allow-Methods':'POST, OPTIONS',
    'Access-Control-Allow-Headers':'Content-Type'
  }});
  if (req.method !== 'POST') return json(405,{},origin);
  if (!req.headers.get('content-type')?.toLowerCase().startsWith('application/json')) return json(415,{},origin);
  if (!deps.token || !deps.targets.length) return json(503,{},origin);
  if (webhook) {
    const signature = req.headers.get('x-telegram-bot-api-secret-token') || '';
    const expected = digest(deps.token,'studio-chat-webhook-v1');
    if (!hexSession.test(signature) || !timingSafeEqual(Buffer.from(signature),Buffer.from(expected))) return json(403,{});
  }
  const raw = await req.text();
  if (raw.length > 65536) return json(413,{},origin);
  let data;
  try { data = JSON.parse(raw); } catch { return json(400,{},origin); }
  if (!data || typeof data !== 'object' || Array.isArray(data)) return json(400,{},origin);
  try {
    if (webhook) { await acceptReply(data,deps,Date.now()); return json(200,{}); }
    const [status,result] = ['staff_read','staff_reply'].includes(data.action)
      ? await staff(data,deps,Date.now()) : await visitor(data,context.ip || 'unknown',deps,Date.now());
    return json(status,result,origin);
  } catch { return json(503,{},origin); }
}

export async function pruneChat(store, now) {
  for (const prefix of ['limit/','expiry/']) {
    for await (const page of store.list({prefix,paginate:true})) {
      const expired = page.blobs.filter(({key})=>{
        const end = Number(key.split('/')[1]);
        return (prefix === 'limit/' ? end : end * HOUR) <= now;
      });
      for (let i = 0; i < expired.length; i += 16) {
        await Promise.all(expired.slice(i,i+16).map(async ({key})=>{
          if (prefix === 'expiry/') {
            const target = key.split('/').slice(2).join('/');
            const entry = await store.getMetadata(target);
            if (entry && entry.metadata.expires <= now) await store.delete(target);
          }
          await store.delete(key);
        }));
      }
    }
  }
}
