import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import products from "./products.json";
import {resolve} from 'node:path';
import {realpathSync,readFileSync} from 'node:fs';
import {activeEntry,moduleAliases} from './scripts/workspace-core.mjs';
import {provenancePlugin} from './scripts/build-provenance.mjs';
const architectureStandalone = process.env.VITE_ARCHITECTURE_STANDALONE === '1';
// Older Hunspell bindings call nanoid's CommonJS export. Make that import
// explicit for Rollup, including the separately compiled spelling worker.
const proofingInterop = () => ({
  name: 'prisma-proofing-interop',
  transform(code:string,id:string){
    if(/(?:hunspell-asm|emscripten-wasm-loader)/.test(id)){
      const fixed=code.replace("import * as nanoid from 'nanoid';","import nanoid from 'nanoid';").replace("import * as runtime from './lib/node/hunspell';","import runtime from './lib/node/hunspell';").replace("import * as unixify from 'unixify';","import unixify from 'unixify';");
      if(fixed!==code)return {code:fixed,map:null};
    }
  },
});
// Wllama 2.4's URL helper assumes a DOM. Our outer worker owns the model so
// cancellation also stops loading. Adapt only URL resolution; keep its runtime
// and model weights unchanged. The exact SDK version is pinned in pnpm-lock.
const editorialWorkerCompat = () => ({
  name: 'auralis-editorial-worker-compat',
  transform(code:string,id:string){
    if(!id.replaceAll('\\','/').includes('/@wllama/wllama/')||!id.endsWith('/esm/index.js'))return;
    const original='new URL(relativePath, document.baseURI)',replacement="new URL(relativePath, typeof document === 'undefined' ? self.location.href : document.baseURI)";
    if(!code.includes(original))throw Error('Revisa el adaptador de URL del motor editorial antes de cambiar su versión.');
    return {code:code.replace(original,replacement),map:null};
  },
});
export default defineConfig({
  cacheDir: 'node_modules/.vite-auralis-'+(process.env.VITE_PRODUCT??'pdf'),
  publicDir: architectureStandalone ? false : 'public',
  resolve: {alias: {'@prisma/active-app':activeEntry(process.cwd(),process.env.VITE_PRODUCT??'pdf'),...moduleAliases(process.cwd())}},
  plugins: [
    react(),
    proofingInterop(),
    editorialWorkerCompat(),
    provenancePlugin(process.env.VITE_PRODUCT??'pdf'),
    {
      name: "prisma-product",
      transformIndexHtml(html) {
        if (architectureStandalone) return html;
        const kind=process.env.VITE_PRODUCT as keyof typeof products;
        const canonical='https://oscard0823.github.io/'+(products[kind]??products.pdf).siteSlug+'/';
        html=html.replace('<head>','<head>\n    <link rel="canonical" href="'+canonical+'" />');
        html=html.replace(/<title>[\s\S]*?<\/title>/,'<title>'+(products[kind]??products.pdf).name+' · BETA · Una nueva luz para tus ideas</title>');
        html=html.replaceAll('Auralis Folio',(products[kind]??products.pdf).name).replaceAll('Auralis Folio',(products[kind]??products.pdf).name);
        return html;
      },
    },
  ],
  base: "./",
  server: {fs:{allow:[process.cwd(),...Object.values(moduleAliases(process.cwd())).map(dir=>realpathSync(dir)),realpathSync('node_modules')]},watch: {ignored: ["**/dist/**", "**/dist-*/**", "**/release*/**", "**/qa/**", "**/android/**", "**/.prisma/architecture-source/**"]}},
  optimizeDeps: { entries: ["index.html"],include:['hunspell-asm'],exclude:['@wllama/wllama/esm/index.js'],esbuildOptions:{plugins:[{name:'prisma-proofing-development-interop',setup(build){build.onLoad({filter:/(?:hunspell-asm|emscripten-wasm-loader)[/\\].*\.js$/},args=>{const code=readFileSync(args.path,'utf8'),contents=code.replace("import * as nanoid from 'nanoid';","import nanoid from 'nanoid';").replace("import * as runtime from './lib/node/hunspell';","import runtime from './lib/node/hunspell';").replace("import * as unixify from 'unixify';","import unixify from 'unixify';");return{contents,loader:'js'};});}}]} },
  worker: { format: "es", plugins:()=>[proofingInterop(),editorialWorkerCompat()] },
  build: { chunkSizeWarningLimit: 1800, ...(architectureStandalone ? {rollupOptions:{input:resolve('arquitectura.html')}} : {}) },
});
