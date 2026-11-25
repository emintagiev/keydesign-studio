import { getStore } from '@netlify/blobs';
import { pruneChat } from '../lib/studio-chat.mjs';

export const config = {schedule:'@hourly'};
export default async () => {
  await pruneChat(getStore({name:'studio-chat',consistency:'strong'}), Date.now());
};
