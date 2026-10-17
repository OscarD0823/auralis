import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
test('Windows installer metadata uses the same product versions as web and Android',()=>{
 const products=JSON.parse(fs.readFileSync('products.json','utf8'));
 const covered=new Set();
 for(const file of fs.readdirSync('.').filter(file=>/^electron-builder.*\.yml$/.test(file))){
  let config=fs.readFileSync(file,'utf8');
  if(file==='electron-builder-arquitectura.yml'){
   assert.equal(config.match(/^extends:\s*(.+)$/m)?.[1],'./electron-builder-architecture.yml');
   config=fs.readFileSync('electron-builder-architecture.yml','utf8');
  }
  const kind=config.match(/prismaProduct:\s*(\w+)/)?.[1];
  assert(kind&&products[kind],file+' needs a product');covered.add(kind);
  assert.equal(config.match(/\n  version:\s*([^\s]+)/)?.[1],products[kind].version,file+' would publish an outdated Windows installer');
  assert.equal(config.match(/^productName:\s*(.+)$/m)?.[1].trim(),products[kind].name);
 }
 assert.deepEqual([...covered].sort(),Object.keys(products).sort());
});
