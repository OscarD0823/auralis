import test from 'node:test';import assert from 'node:assert/strict';import 'fake-indexeddb/auto';
import {saveOfficeFile,loadOfficeFile,listOfficeFiles} from '@prisma/core/office-storage';
import {recoverDataDraft,type DataDraft} from '@prisma/data/data-draft';
test('Nexus recovers unexecuted SQL and a pending record separately from database bytes',async()=>{
 const draft:DataDraft={sql:'INSERT INTO "Personas" (nombre) VALUES (',newTable:'Ideas',definition:'nombre TEXT',createOpen:true,tab:'Consulta SQL',table:'Personas',record:{nombre:'Ana'},newRecord:true,rowKey:undefined};
 const file={id:'recovery-database',product:'data',name:'Prueba',bytes:new Uint8Array([83,81,76]),updated:Date.now(),draft};
 await saveOfficeFile(file);const restored=await loadOfficeFile(file.id);assert.deepEqual(restored?.bytes,file.bytes);assert.deepEqual(recoverDataDraft(restored?.draft),draft);
 assert.equal('draft' in (await listOfficeFiles('data')).find(card=>card.id===file.id)!,false);
 assert.equal(recoverDataDraft({sql:42}),undefined);assert.equal(recoverDataDraft(undefined),undefined);
});
test('Nexus restores typed query parameters and the page of an unfinished record without executing SQL',()=>{
 const base={sql:'DELETE FROM Pedidos;',newTable:'Tabla',definition:'id INTEGER',createOpen:false,tab:'Salud',table:'Pedidos',record:{importe:'42'},rowKey:{rowid:1507},newRecord:false,params:{':minimo':'15'},paramTypes:{':minimo':'number'},queryName:'Importes',queryId:'q1',nullFields:['nota'],browse:{offset:1500,pageSize:100,search:'',sort:'importe',direction:'desc'}};
 const recovered=recoverDataDraft(base)!;assert.equal(recovered.sql,'DELETE FROM Pedidos;');assert.equal(recovered.browse?.offset,1500);assert.equal(recovered.paramTypes?.[':minimo'],'number');assert.deepEqual(recovered.nullFields,['nota']);assert.equal(recovered.tab,'Salud');
 const invalid=recoverDataDraft({...base,paramTypes:{':minimo':'unsupported'},browse:{offset:-2,pageSize:42,direction:'arbitrary'}})!;assert.equal(invalid.paramTypes,undefined);assert.equal(invalid.browse?.offset,0);assert.equal(invalid.browse?.pageSize,100);assert.equal(invalid.browse?.direction,'asc');
});
