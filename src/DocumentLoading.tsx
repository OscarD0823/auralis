import type { ReactNode } from 'react';
import './document-loading.css';

/** Shared by web, installed PWA, Android and desktop. No artificial delay. */
export function DocumentLoading({label='Preparando tu espacio…',overlay=false,compact=false,preview,children}:{label?:string;overlay?:boolean;compact?:boolean;preview?:ReactNode;children?:ReactNode}) {
  return <div className={`auralis-loading ${overlay?'auralis-loading--overlay':''} ${compact?'auralis-loading--compact':''} ${preview?'auralis-loading--with-preview':''}`} aria-busy="true">
    <div className="auralis-loading__card" role="status" aria-live="polite">
      <img className="auralis-loading__sky" src={new URL('./assets/constellation.svg',import.meta.url).href} alt="" aria-hidden="true" width="400" height="220"/>
      <span className="auralis-loading__brand">AURALIS</span>
      <strong>{label}</strong>
      <span className="auralis-loading__detail">Tu trabajo permanece en este dispositivo</span>
      {children}
    </div>
    {preview}
  </div>;
}
