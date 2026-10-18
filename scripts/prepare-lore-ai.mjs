import fs from 'node:fs';import path from 'node:path';
if(['stories','prisma'].includes(process.env.VITE_PRODUCT??'pdf')){
 const out='public/lore-ai';fs.mkdirSync(out+'/licenses',{recursive:true});
 fs.copyFileSync('node_modules/@wllama/wllama/esm/single-thread/wllama.wasm',out+'/wllama.wasm');
 for(const file of ['compat.wasm','compat.js'])fs.rmSync(out+'/'+file,{force:true});
 fs.copyFileSync('node_modules/@wllama/wllama/LICENCE',out+'/licenses/wllama-MIT.txt');
 fs.copyFileSync('vendor/lore-ai/Qwen-Apache-2.0.txt',out+'/licenses/Qwen-Apache-2.0.txt');
 fs.copyFileSync('vendor/lore-ai/Creative-model-card.md',out+'/licenses/Creative-model-card.md');
 console.log('Lore: motor de IA local opcional preparado, sin descargar pesos.');
}else{
 const out=path.resolve('public/lore-ai');if(!out.startsWith(path.resolve('public')+path.sep))throw Error('Ruta no válida.');fs.rmSync(out,{recursive:true,force:true});
}
