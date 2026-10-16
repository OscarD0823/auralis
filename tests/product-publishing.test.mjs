import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
test('la publicación de cada aplicación toma sus fuentes del catálogo Auralis actual',()=>{
 const products=JSON.parse(fs.readFileSync('products.json','utf8'));
 const workflow=fs.readFileSync('.github/workflows/product-pages.yml','utf8');
 const declaration=workflow.match(/const slugs=(\{[^;]+\});/);
 assert.ok(declaration,'La fase de detección debe declarar todos los repositorios que comprueba.');
 const repositories=JSON.parse(declaration[1]);
 assert.deepEqual(repositories,Object.fromEntries(Object.entries(products).map(([kind,product])=>[kind,product.siteSlug])));
 assert.match(workflow,/repository: OscarD0823\/auralis\s/);
});
