/** Yield between CPU batches, including in hidden tabs where RAF can stop. */
export async function yieldToDevice():Promise<void> {
  const scheduler=(globalThis as typeof globalThis & {scheduler?:{yield?:()=>Promise<void>}}).scheduler;
  if(scheduler?.yield)await scheduler.yield();
  else await new Promise<void>(resolve=>setTimeout(resolve,0));
}
