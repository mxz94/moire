
import type { PageServerLoad } from './$types';
import { getMemos } from '$lib/server/memos';

export const load: PageServerLoad = async () => {
  const memos = await getMemos();

  return {
    memos
  };
};
