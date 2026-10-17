import type {CSSProperties,ReactNode} from 'react';
import type {FlowDocument,RichNode} from '@prisma/writer/flow';
import {pageSize} from '@prisma/writer/flow';
import type {Source} from '@prisma/pdf/pdf';
import {PageCanvas} from './components';

export type OpeningPreview={name:string;flow:FlowDocument}|{name:string;source:Source};
function nodeView(node:RichNode,key:number):ReactNode {
  const a=node.attrs??{},content=node.content?.map(nodeView);
  const style:CSSProperties={fontFamily:String(a.fontFamily??'Arial, sans-serif'),fontSize:a.fontSize?Number(a.fontSize)+'pt':undefined,textAlign:a.textAlign as CSSProperties['textAlign'],lineHeight:Number(a.lineHeight)||1.45,marginTop:Number(a.spaceBefore)||0,marginBottom:Number(a.spaceAfter??7),textIndent:Number(a.firstLineIndent)||0};
  if(node.type==='text'){
    const marks=node.marks??[];
    return <span key={key} style={{fontWeight:marks.some(m=>m.type==='bold')?700:undefined,fontStyle:marks.some(m=>m.type==='italic')?'italic':undefined,textDecoration:marks.some(m=>m.type==='underline')?'underline':undefined}}>{node.text}</span>;
  }
  if(node.type==='image'){
    const src=String(a.src??'');if(!/^data:image\/(png|jpeg|gif|webp);base64,/i.test(src))return null;
    return <img key={key} src={src} alt={String(a.alt??'')} style={{maxWidth:'100%',width:a.width?Number(a.width)+'pt':undefined,height:a.height?Number(a.height)+'pt':undefined,objectFit:'contain'}}/>;
  }
  if(node.type==='hardBreak')return <br key={key}/>;
  if(node.type==='table')return <table key={key}><tbody>{content}</tbody></table>;
  if(node.type==='tableRow')return <tr key={key}>{content}</tr>;
  if(node.type==='tableCell'||node.type==='tableHeader')return <td key={key}>{content}</td>;
  if(node.type==='bulletList')return <ul key={key}>{content}</ul>;
  if(node.type==='orderedList')return <ol key={key}>{content}</ol>;
  if(node.type==='listItem')return <li key={key}>{content}</li>;
  return <div key={key} style={{...style,fontWeight:node.type==='heading'?700:undefined}}>{content||node.text}</div>;
}
export function InitialPagePreview({preview}:{preview:OpeningPreview}){
  const flow='flow'in preview?preview.flow:undefined;
  const [w,h]=flow?pageSize(flow.layout):[595,842],scale=280/(w*4/3);
  return <figure className="auralis-loading__preview" aria-label="Vista previa de la primera página" aria-live="off">
    <figcaption><span>PRIMERA PÁGINA</span><strong>{preview.name}</strong></figcaption>
    <div className="auralis-loading__paper" style={{width:280,height:Math.min(400,h/w*280)}}>
      {flow?<div className="auralis-loading__page-content" style={{width:w*4/3,height:h*4/3,transform:`scale(${scale})`,padding:`${flow.layout.top*72/25.4}pt ${flow.layout.right*72/25.4}pt ${flow.layout.bottom*72/25.4}pt ${flow.layout.left*72/25.4}pt`}}>{flow.content.content?.map(nodeView)}</div>:'source'in preview&&<PageCanvas source={preview.source} page={{id:'preview',sourceId:preview.source.id,index:0,rotation:0,marks:[]}} width={280}/>}
    </div>
    <small>{flow?'Vista previa provisional mientras se prepara la edición':'Vista del documento original'}</small>
  </figure>;
}
