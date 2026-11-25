import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { handleChat, pruneChat } from '../netlify/lib/studio-chat.mjs';

// The fixture never contacts Telegram or Netlify.
const entries = new Map();
let version = 0;
const store = {
  async get(key) { return entries.get(key)?.data ?? null; },
  async getWithMetadata(key) { return entries.get(key) ?? null; },
  async getMetadata(key) { return entries.get(key) ?? null; },
  async set(key,data) { entries.set(key,{data}); },
  async setJSON(key,data,{onlyIfNew,onlyIfMatch,metadata}={}) {
    if (onlyIfNew && entries.has(key) || onlyIfMatch && onlyIfMatch !== entries.get(key)?.etag) return {modified:false};
    entries.set(key,{data,metadata,etag:String(++version)}); return {modified:true};
  },
  async delete(key) {entries.delete(key);},
  list({prefix,paginate}) {
    const page = {blobs:[...entries.keys()].filter(key=>key.startsWith(prefix)).map(key=>({key}))};
    return paginate ? [page] : page;
  }
};
const token='1234:fixture', targets=['52'], notices=[];
const deps={store,token,targets,dispatch:async (_token,_dest,text)=>{notices.push(text);return true;}};
const origin='https://www.keydesign.studio', url='https://example.test/chat';
const sig=createHmac('sha256',token).update('studio-chat-webhook-v1').digest('hex');
const call=(payload,hook=false,signature=sig)=>handleChat(new Request(url+(hook?'?webhook=1':''),{
  method:'POST',headers:{'Content-Type':'application/json','Origin':origin,'X-Telegram-Bot-Api-Secret-Token':signature},
  body:JSON.stringify(payload)
}),{ip:'test'},deps);
const input={action:'send',name:'Test',text:'Question',consent:true,session:'1'.repeat(64),id:'a'.repeat(32)};
assert.equal((await call({...input,consent:false})).status,422);
await Promise.all([call(input),call(input)]);
assert.equal((await call(input)).status,200); assert.equal(notices.length,1);
const update={message:{message_id:2,chat:{id:52},from:{is_bot:false},text:'Reply',
  reply_to_message:{date:Math.floor(Date.now()/1000),from:{is_bot:true,id:1234},text:notices[0]}}};
const read=async (session=input.session)=>(await (await call({action:'read',session})).json()).messages;
assert.equal((await call(update,true,'wrong')).status,403);
await call({message:{...update.message,chat:{id:51}}},true);
assert.equal((await read()).length,1);
await call(update,true); await call(update,true);
assert.deepEqual((await read()).map(e=>e.text),['Question','Reply']);
assert.deepEqual(await read('2'.repeat(64)),[]);
await pruneChat(store,Date.now()+8*86400000);
assert.equal(entries.size,0);
console.log('Visitor delivery, concurrent retry, authorized reply, isolation and expiry passed.');
