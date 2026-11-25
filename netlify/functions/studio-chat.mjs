import { getStore } from '@netlify/blobs';
import { handleChat } from '../lib/studio-chat.mjs';

async function dispatch(token, chatId, text, link) {
  const res = await fetch('https://api.telegram.org/bot'+token+'/sendMessage', {
    method:'POST', headers:{'Content-Type':'application/json'}, signal:AbortSignal.timeout(8000),
    body:JSON.stringify({chat_id:chatId,text,disable_web_page_preview:true,
      reply_markup:{inline_keyboard:[[{text:'Открыть чат',url:link}]]}})
  });
  const result = await res.json();
  if (result.ok === true) return result.result?.message_id;
  return res.status >= 400 && res.status < 500 && result.ok === false ? false : null;
}

export default (req, context) => handleChat(req,context,{
  store:getStore({name:'studio-chat',consistency:'strong'}),
  token:process.env.TELEGRAM_BOT_TOKEN, targets:(process.env.TELEGRAM_CHAT_ID || '').split(',').map(s=>s.trim()).filter(Boolean),
  dispatch
});
