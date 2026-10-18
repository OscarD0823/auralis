from pathlib import Path
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import json, csv, hashlib, math, argparse
from lxml import etree as E
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.enum.text import WD_BREAK, WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont
from openpyxl import Workbook

parser=argparse.ArgumentParser(description='Crea una batería sintética de compatibilidad DOCX, no una certificación de todas las funciones de Word.')
parser.add_argument('--output',type=Path,required=True,help='Carpeta nueva para los archivos de prueba')
parser.add_argument('--diagram-font',help='Ruta opcional a una fuente TrueType para el diagrama')
args=parser.parse_args()
OUT=args.output.resolve()
OUT.mkdir(parents=True,exist_ok=False)
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','m':'http://schemas.openxmlformats.org/officeDocument/2006/math','c':'http://schemas.openxmlformats.org/drawingml/2006/chart','a':'http://schemas.openxmlformats.org/drawingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing','v':'urn:schemas-microsoft-com:vml','w14':'http://schemas.microsoft.com/office/word/2010/wordml'}
bookmark_id=1
def xml(s):return E.fromstring(s.encode())
def tag(qualified_name,**attrs):
 el=OxmlElement(qualified_name)
 for k,v in attrs.items():el.set(qn('w:'+k),str(v))
 return el
def field(p,code,result=''):
 for kind in ['begin','code','separate','text','end']:
  r=OxmlElement('w:r')
  if kind=='code':e=OxmlElement('w:instrText');e.set('{http://www.w3.org/XML/1998/namespace}space','preserve');e.text=' '+code+' '
  elif kind=='text':e=OxmlElement('w:t');e.text=str(result)
  else:e=tag('w:fldChar',fldCharType=kind)
  r.append(e);p._p.append(r)
def bookmark(p,name):
 global bookmark_id
 p._p.insert(1 if p._p.find(qn('w:pPr')) is not None else 0,tag('w:bookmarkStart',id=bookmark_id,name=name));p._p.append(tag('w:bookmarkEnd',id=bookmark_id));bookmark_id+=1
def link(p,text,target):
 h=tag('w:hyperlink',anchor=target);r=OxmlElement('w:r');rp=OxmlElement('w:rPr');rp.append(tag('w:u',val='single'));r.append(rp);t=OxmlElement('w:t');t.text=text;r.append(t);h.append(r);p._p.append(h)
def base(title):
 d=Document();d.core_properties.title=title;d.core_properties.author='OscarD0823';d.core_properties.subject='Prueba original de compatibilidad Auralis y Word';d.core_properties.keywords='Auralis, batería, compatibilidad, MO-110, MO-111'
 for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','Caption']:
  s=d.styles[name];s.font.name='Arial';s.font.color.rgb=RGBColor(0,0,0);s.font.size=Pt(11 if name in ['Normal','Caption'] else 22 if name=='Title' else 16 if name=='Heading 1' else 13)
  for borders in s.element.findall('.//'+qn('w:pBdr')):borders.getparent().remove(borders)
  for fonts in s.element.findall('.//'+qn('w:rFonts')):
   for key in list(fonts.attrib):
    if E.QName(key).localname.lower().endswith('theme'):del fonts.attrib[key]
  s.paragraph_format.space_after=Pt(7);s.paragraph_format.line_spacing=1.12
 d.styles['Normal'].paragraph_format.widow_control=True
 for s in d.sections:setup(s)
 setting=tag('w:updateFields',val='true');settings=d.settings.element;compat=settings.find(qn('w:compat'));settings.insert(list(settings).index(compat) if compat is not None else 0,setting)
 return d
def setup(s,landscape=False,columns=1):
 s.page_width=Inches(11 if landscape else 8.5);s.page_height=Inches(8.5 if landscape else 11);s.orientation=WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT
 s.top_margin=s.bottom_margin=s.left_margin=s.right_margin=Inches(.85);s.header_distance=s.footer_distance=Inches(.35)
 cols=s._sectPr.find(qn('w:cols'));cols.set(qn('w:num'),str(columns));cols.set(qn('w:space'),'400')
 s.header.is_linked_to_previous=False;s.footer.is_linked_to_previous=False
 p=s.header.paragraphs[0];p.text='Auralis   Laboratorio de documentos';p.runs[0].font.size=Pt(9)
 p=s.footer.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.RIGHT;p.add_run('Página ');field(p,'PAGE','1')
def section(d,landscape=False,columns=1,kind=WD_SECTION_START.NEW_PAGE):
 s=d.add_section(kind);setup(s,landscape,columns);return s
def page(d,title,token):
 d.add_page_break();h=d.add_heading(title,1);bookmark(h,token);d.add_paragraph('Identificador de control '+token+'. Comprueba contenido, estructura y edición tras importar y exportar.')
def caption(d,label,title,bm):
 p=d.add_paragraph(style='Caption');p.add_run(label+' ');field(p,'SEQ '+label+' \\* ARABIC','1');p.add_run('  '+title);bookmark(p,bm);return p
def table(d,rows,headers=1):
 t=d.add_table(rows=0,cols=len(rows[0]));t.style='Table Grid'
 for i,row in enumerate(rows):
  cells=t.add_row().cells
  if i<headers:t.rows[-1]._tr.get_or_add_trPr().append(tag('w:tblHeader'))
  t.rows[-1]._tr.get_or_add_trPr().append(tag('w:cantSplit'))
  for c,text in zip(cells,row):
   c.text=str(text);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   if i<headers:
    c._tc.get_or_add_tcPr().append(tag('w:shd',val='clear',fill='EAEAEA'))
    for r in c.paragraphs[0].runs:r.bold=True
 return t
def sdt(p,alias,kind,content,options=None):
 n=OxmlElement('w:sdt');pr=OxmlElement('w:sdtPr');pr.append(tag('w:alias',val=alias));pr.append(tag('w:tag',val=alias));pr.append(tag('w:id',val=10000+len(alias)));n.append(pr)
 if kind=='checkBox':
  prop=E.Element('{'+NS['w14']+'}checkbox');checked=E.SubElement(prop,'{'+NS['w14']+'}checked');checked.set('{'+NS['w14']+'}val','0');pr.append(prop)
 else:
  prop=OxmlElement('w:'+kind);pr.append(prop)
  if kind=='dropDownList':
   for text in options or []:prop.append(tag('w:listItem',displayText=text,value=text))
  if kind=='date':prop.append(tag('w:dateFormat',val='dd/MM/yyyy'));prop.append(tag('w:lid',val='es-CO'))
 body=OxmlElement('w:sdtContent');r=OxmlElement('w:r');t=OxmlElement('w:t');t.text=content;r.append(t);body.append(r);n.append(body);p._p.append(n)
def equation(p):
 p._p.append(xml(f'''<m:oMathPara xmlns:m="{NS['m']}"><m:oMath><m:f><m:num><m:sSup><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup><m:r><m:t> + </m:t></m:r><m:sSup><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup></m:num><m:den><m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e><m:r><m:t>n</m:t></m:r></m:e></m:rad></m:den></m:f><m:r><m:t> = α</m:t></m:r></m:oMath></m:oMathPara>'''))
def textbox(p):
 p._p.append(xml(f'''<w:r xmlns:w="{NS['w']}" xmlns:v="{NS['v']}"><w:pict><v:rect id="AuralisTextBox" style="width:360pt;height:65pt" filled="f" stroked="t"><v:textbox inset="8pt,8pt,8pt,8pt"><w:txbxContent><w:p><w:r><w:t>CUADRO_EDITABLE_01 Texto dentro de una forma nativa de Word</w:t></w:r></w:p></w:txbxContent></v:textbox></v:rect></w:pict></w:r>'''))
def native_chart(p):
 p._p.append(xml(f'''<w:r xmlns:w="{NS['w']}" xmlns:wp="{NS['wp']}" xmlns:a="{NS['a']}" xmlns:c="{NS['c']}" xmlns:r="{NS['r']}"><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="5486400" cy="2743200"/><wp:docPr id="900" name="Grafico editable de resultados" descr="Gráfico de columnas con tres series de resultados sintéticos"/><wp:cNvGraphicFramePr/><a:graphic><a:graphicData uri="{NS['c']}"><c:chart r:id="rIdAuralisChart"/></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'''))
def package_patch(path,extras=None,relationships=None):
 with ZipFile(path) as z:parts={n:z.read(n) for n in z.namelist()}
 body=E.fromstring(parts['word/document.xml']);order=['cnfStyle','tcW','gridSpan','hMerge','vMerge','tcBorders','shd','noWrap','tcMar','textDirection','tcFitText','vAlign','hideMark','headers','cellIns','cellDel','cellMerge','tcPrChange']
 for prop in body.findall('.//w:tcPr',NS):
  for child in sorted(list(prop),key=lambda e:order.index(E.QName(e).localname) if E.QName(e).localname in order else 100):prop.append(child)
 parts['word/document.xml']=E.tostring(body,xml_declaration=True,encoding='UTF-8',standalone=True)
 relroot=E.fromstring(parts['word/_rels/document.xml.rels']);ct=E.fromstring(parts['[Content_Types].xml']);rns='http://schemas.openxmlformats.org/package/2006/relationships';cns='http://schemas.openxmlformats.org/package/2006/content-types'
 for rid,typ,target in relationships or []:E.SubElement(relroot,'{'+rns+'}Relationship',Id=rid,Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/'+typ,Target=target)
 for name,blob,mime in extras or []:
  parts[name]=blob.encode() if isinstance(blob,str) else blob
  if mime:E.SubElement(ct,'{'+cns+'}Override',PartName='/'+name,ContentType=mime)
 parts['word/_rels/document.xml.rels']=E.tostring(relroot,xml_declaration=True,encoding='UTF-8',standalone=True);parts['[Content_Types].xml']=E.tostring(ct,xml_declaration=True,encoding='UTF-8',standalone=True)
 with ZipFile(path,'w',ZIP_DEFLATED) as z:
  for n,b in parts.items():z.writestr(n,b)

try:
 diagram_font=ImageFont.truetype(args.diagram_font or 'Arial.ttf',28)
except OSError:
 diagram_font=ImageFont.load_default(size=28)
img=Image.new('RGB',(1000,420),'white');draw=ImageDraw.Draw(img)
for x,label in [(60,'1 CAPTURA'),(370,'2 PROCESO'),(680,'3 RESULTADO')]:draw.rounded_rectangle((x,120,x+260,280),radius=20,fill='#eceaf8',outline='#343145',width=4);draw.text((x+20,182),label,fill='black',font=diagram_font)
draw.line((320,200,370,200),fill='black',width=5);draw.line((630,200,680,200),fill='black',width=5);img.save(OUT/'Diagrama-original.png')

d=base('Libro maestro de compatibilidad entre Word y Auralis')
d.add_heading('Libro maestro de compatibilidad entre Word y Auralis',0)
d.add_paragraph('Batería original de documentos y tareas avanzadas',style='Subtitle')
d.add_paragraph('Autor OscarD0823\nFecha 17 de octubre de 2026\nDatos sintéticos sin información personal')
d.add_paragraph('Este libro reúne pruebas de estructura, edición, referencias, revisión y objetos. Se abre primero en Word para fijar la referencia y después en Auralis Scribe. Cada identificador permite localizar una pérdida, una transformación o una función pendiente. La matriz adjunta distingue presencia en el archivo, representación, edición y conservación al volver a guardar.')
d.add_paragraph('Los temarios oficiales MO 110 y MO 111 y una evaluación avanzada de Washburn Tech orientan la cobertura. Los textos, datos, diseños y actividades de esta batería son propios. No se presenta como una prueba de todas las versiones, servicios o complementos de Word.')
s=d.sections[0];s.different_first_page_header_footer=True;s.first_page_header.paragraphs[0].text='';s.first_page_footer.paragraphs[0].text=''
page(d,'Contenido y navegación','NAV_CONTENIDO')
p=d.add_paragraph();field(p,'TOC \\o "1-3" \\h \\z \\u','Actualiza la tabla completa en Word con F9')
d.add_paragraph('Después de actualizar, cada entrada debe navegar al título. Cambia un título y actualiza de nuevo para comprobar el campo, no solo su apariencia.')
p=d.add_paragraph();link(p,'Ir al apéndice B','APENDICE_B');p.add_run('   ');link(p,'Ir a la tabla de resultados','TABLA_RESULTADOS')
page(d,'Texto y tipografía','TXT_TIPOGRAFIA')
p=d.add_paragraph('TEXTO_BASE_01 ')
for name,attr in [('negrita','bold'),('cursiva','italic'),('subrayado','underline'),('tachado','strike')]:
 r=p.add_run(name+'  ')
 if attr=='strike':r.font.strike=True
 else:setattr(r,attr,True)
r=p.add_run('H2O ');r.font.subscript=True;r=p.add_run('x2 ');r.font.superscript=True
for family in ['Arial','Times New Roman','Calibri','Cambria','Consolas','Georgia']:
 p=d.add_paragraph('FUENTE_'+family.replace(' ','_')+'  Árbol, información, 1.234,56; 10 %; €; ¿pregunta?');p.runs[0].font.name=family
d.add_paragraph('UNICODE_01 café cafe\u0301 — – «comillas» “dobles” … ½ ¼ ± × ÷ ∞ ≤ ≥ → • § ¶ Ω Ж Ελληνικά 日本語 العربية हिन्दी')
p=d.add_paragraph('Visible ');r=p.add_run('OCULTO_01');r.font.hidden=True;p.add_run(' y texto tras el contenido oculto.')
for lang,text in [('es-CO','ES_IDIOMA La edición debe conservar tildes y signos.'),('en-US','EN_LANGUAGE The document preserves the original spelling.'),('fr-FR','FR_LANGUE Une référence et une équation restent modifiables.')]:
 p=d.add_paragraph(text);p.runs[0]._r.get_or_add_rPr().append(tag('w:lang',val=lang))
page(d,'Párrafos listas y búsqueda','PAR_PAGINACION')
p=d.add_paragraph('PARRAFO_SANGRIA_01 Este párrafo usa primera línea, separación posterior e interlineado. Debe conservarse al editar una palabra sin afectar al bloque siguiente.');p.paragraph_format.first_line_indent=Inches(.35);p.paragraph_format.space_after=Pt(12);p.paragraph_format.keep_together=True
p=d.add_paragraph('PARRAFO_FRANCES_01 Referencia con sangría francesa para comprobar alineación de las líneas que continúan. '*3);p.paragraph_format.left_indent=Inches(.35);p.paragraph_format.first_line_indent=Inches(-.35)
p=d.add_paragraph('TABULACION_01\tImporte\t1.234,56');p.paragraph_format.tab_stops.add_tab_stop(Inches(2.5));p.paragraph_format.tab_stops.add_tab_stop(Inches(5))
for style,items in [('List Number',['Elemento inicial','Elemento que continúa','Elemento final']),('List Bullet',['Viñeta principal','Otra viñeta']),('List Bullet 2',['Viñeta anidada'])]:
 for text in items:d.add_paragraph(text,style=style)
d.add_paragraph('BUSCAR_01 gato GATO gatos; código A 001; código B 002; espacios  dobles; salto de línea manual aquí\ny continuación dentro del mismo párrafo.')
s=section(d,columns=2);d.add_heading('Sección en dos columnas',1)
for i in range(5):d.add_paragraph('COLUMNA_A_'+str(i)+' Este bloque comprueba la anchura y el orden de lectura entre columnas. La estructura debe conservar el salto explícito y el cambio de sección.')
d.add_paragraph().add_run().add_break(WD_BREAK.COLUMN)
for i in range(5):d.add_paragraph('COLUMNA_B_'+str(i)+' El segundo bloque comienza después del salto de columna. La lectura y el copiado deben seguir el orden lógico del texto.')
s=section(d,landscape=True);d.add_heading('Sección horizontal y tabla combinada',1);bookmark(d.paragraphs[-1],'SECCION_HORIZONTAL')
caption(d,'Tabla','Resultados sintéticos con celdas combinadas','TABLA_RESULTADOS')
t=table(d,[['Grupo','Caso','Entrada','Salida','Estado'],['A','CASO_001','Texto','Documento','Esperado'],['A','CASO_002','Tabla','Tabla editable','Esperado'],['B','CASO_003','Referencia','Destino válido','Esperado']]);t.cell(1,0).merge(t.cell(2,0));t.cell(0,3).merge(t.cell(0,4))
d.add_paragraph('Nota. Elaboración propia. Cambia CASO_002 sin modificar la combinación vertical ni la cabecera.')
p=d.add_paragraph('Referencia cruzada al número de tabla ');field(p,'REF TABLA_RESULTADOS \\h','Tabla 1');p.add_run(' y a su página ');field(p,'PAGEREF TABLA_RESULTADOS \\h','6')
s=section(d);d.add_heading('Tabla extensa con dos cabeceras',1);bookmark(d.paragraphs[-1],'TABLA_EXTENSA')
rows=[['Código','Cantidad','Importe'],['Cabecera secundaria','Unidades','COP']]+[[f'REGISTRO_{i:03}',str(i),f'{i*1250:,}'.replace(',','.')] for i in range(1,43)]
table(d,rows,2)
d.add_paragraph('FIN_TABLA_EXTENSA Los 42 registros deben aparecer una vez. Las dos primeras filas se repiten en las continuaciones.')
page(d,'Ilustraciones y ajuste del texto','OBJ_IMAGEN')
caption(d,'Figura','Diagrama propio de tres etapas','FIGURA_ETAPAS')
p=d.add_paragraph();shape=p.add_run().add_picture(str(OUT/'Diagrama-original.png'),width=Inches(5.8));shape._inline.docPr.set('descr','DIAGRAMA_ALT_01 Tres etapas conectadas de izquierda a derecha')
d.add_paragraph('Nota. Diagrama de elaboración propia. La imagen debe conservar proporción, texto alternativo y relación con su título.')
p=d.add_paragraph('La figura anterior se cita mediante ');field(p,'REF FIGURA_ETAPAS \\h','Figura 1')
p=d.add_paragraph();p.add_run('IMAGEN_FLOTANTE_01 Un dibujo anclado acompaña este texto. '*8)
inline=d.add_paragraph().add_run().add_picture(str(OUT/'Diagrama-original.png'),width=Inches(2.4))._inline
anchor=xml(f'<wp:anchor xmlns:wp="{NS["wp"]}" distT="0" distB="0" distL="114300" distR="114300" simplePos="0" relativeHeight="1" behindDoc="0" locked="0" layoutInCell="1" allowOverlap="0"><wp:simplePos x="0" y="0"/><wp:positionH relativeFrom="column"><wp:align>right</wp:align></wp:positionH><wp:positionV relativeFrom="paragraph"><wp:posOffset>0</wp:posOffset></wp:positionV></wp:anchor>')
for child in list(inline):anchor.append(child)
anchor.insert(4,xml(f'<wp:wrapSquare xmlns:wp="{NS["wp"]}" wrapText="bothSides"/>'));inline.getparent().replace(inline,anchor)
page(d,'Gráfico editable y forma con texto','OBJ_GRAFICO')
caption(d,'Figura','Resultados del laboratorio','FIGURA_GRAFICO');native_chart(d.add_paragraph())
d.add_paragraph('GRAFICO_EDITABLE_01 El gráfico tiene categorías A, B y C y valores 12, 18 y 9. Debe poder abrir sus datos; una captura no demuestra edición del gráfico.')
textbox(d.add_paragraph())
page(d,'Ecuaciones símbolos y notas','OBJ_ECUACION')
d.add_paragraph('ECUACION_NATIVA_01 Fracción con exponentes y radical en formato matemático editable de Word.')
equation(d.add_paragraph())
p=d.add_paragraph('NOTA_PIE_01 Esta frase lleva una nota al pie');r=OxmlElement('w:r');r.append(tag('w:footnoteReference',id=1));p._p.append(r)
p=d.add_paragraph('NOTA_FINAL_01 Esta frase lleva una nota final');r=OxmlElement('w:r');r.append(tag('w:endnoteReference',id=1));p._p.append(r)
d.add_paragraph('Comprueba el texto de la nota, el salto al destino y el regreso al punto de llamada. La referencia no debe desaparecer al cambiar una palabra cercana.')
page(d,'Campos índices y fuentes','REF_CAMPOS')
p=d.add_paragraph('Campo de autor ');field(p,'AUTHOR','OscarD0823');p=d.add_paragraph('Propiedad de título ');field(p,'DOCPROPERTY Title','Libro maestro de compatibilidad entre Word y Auralis')
p=d.add_paragraph('Campo de cálculo ');field(p,'= (1250 * 4) + 350 \\# "0"','5350')
p=d.add_paragraph('Cita de referencia técnica ');field(p,'CITATION MicrosoftWord2026 \\l 3082','(Microsoft, 2026)')
d.add_heading('Lista de figuras',2);field(d.add_paragraph(),'TOC \\h \\z \\c "Figura"','Actualiza las figuras con F9')
d.add_heading('Lista de tablas',2);field(d.add_paragraph(),'TOC \\h \\z \\c "Tabla"','Actualiza las tablas con F9')
d.add_heading('Índice analítico',2);field(d.add_paragraph(),'XE "Compatibilidad:Documentos"','');field(d.add_paragraph(),'XE "Pruebas:Referencias"','');field(d.add_paragraph(),'INDEX \\e ", " \\h "A" \\c "2"','Actualiza el índice con F9')
d.add_heading('Bibliografía',2);field(d.add_paragraph(),'BIBLIOGRAPHY \\l 3082','Microsoft. (2026). Listen to your Word documents. Microsoft Support.')
page(d,'Revisión y cambios registrados','REV_CONTROL')
p=d.add_paragraph('REVISION_01 El plazo acordado es ');p._p.append(tag('w:commentRangeStart',id=0));p.add_run('quince días');p._p.append(tag('w:commentRangeEnd',id=0));r=OxmlElement('w:r');r.append(tag('w:commentReference',id=0));p._p.append(r)
p=d.add_paragraph('CAMBIO_01 La versión revisada utiliza ')
for name,text in [('del','el texto anterior'),('ins','el texto nuevo')]:
 n=tag('w:'+name,id=1 if name=='del' else 2,author='Revisor de prueba',date='2026-10-17T12:00:00Z');r=OxmlElement('w:r');t=OxmlElement('w:delText' if name=='del' else 'w:t');t.text=text;r.append(t);n.append(r);p._p.append(n)
d.add_paragraph('Acepta una inserción y rechaza una eliminación en una copia. Cambiar la visualización de marcas no debe aceptar cambios ni borrar comentarios.')
page(d,'Apéndice A Instrumentos','APENDICE_A')
d.add_paragraph('APENDICE_A_TEXTO_01 Instrumento sintético para comprobar el índice de apéndices y el esquema de títulos.')
p=d.add_paragraph(style='Caption');p.add_run('Apéndice ');field(p,'SEQ Apéndice \\* ALPHABETIC','A');p.add_run('  Instrumentos');bookmark(p,'CAP_AP_A')
d.add_heading('A 1 Criterios de evaluación',2);d.add_heading('A 1 1 Escala de resultados',3)
table(d,[['Resultado','Criterio'],['Conservado','Se representa y sigue siendo editable'],['Parcial','Se conserva con una transformación documentada'],['Ausente','No aparece en el modelo o pierde su estructura'],['Sin comprobar','No se ejecutó la operación']])
page(d,'Apéndice B Protocolo de intercambio','APENDICE_B')
p=d.add_paragraph(style='Caption');p.add_run('Apéndice ');field(p,'SEQ Apéndice \\* ALPHABETIC','B');p.add_run('  Protocolo');bookmark(p,'CAP_AP_B')
d.add_paragraph('APENDICE_B_TEXTO_01 Guarda una copia en Auralis, cambia una palabra del texto principal y vuelve a abrirla en Word. Después repite con un cambio estructural para distinguir la conservación del original de la reconstrucción del documento.')
d.add_heading('Índice de apéndices',2);field(d.add_paragraph(),'TOC \\h \\z \\c "Apéndice"','Actualiza los apéndices con F9')
d.add_paragraph('FIN_MAESTRO_01 Último marcador del cuerpo principal. Las notas finales pueden aparecer después de él.')
master=OUT/'01_Libro_maestro_Word.docx';d.save(master)
chart=f'''<c:chartSpace xmlns:c="{NS['c']}" xmlns:a="{NS['a']}" xmlns:r="{NS['r']}"><c:lang val="es-CO"/><c:chart><c:autoTitleDeleted val="1"/><c:plotArea><c:layout/><c:barChart><c:barDir val="col"/><c:grouping val="clustered"/><c:ser><c:idx val="0"/><c:order val="0"/><c:tx><c:v>Resultados</c:v></c:tx><c:cat><c:strLit><c:ptCount val="3"/><c:pt idx="0"><c:v>A</c:v></c:pt><c:pt idx="1"><c:v>B</c:v></c:pt><c:pt idx="2"><c:v>C</c:v></c:pt></c:strLit></c:cat><c:val><c:numLit><c:formatCode>General</c:formatCode><c:ptCount val="3"/><c:pt idx="0"><c:v>12</c:v></c:pt><c:pt idx="1"><c:v>18</c:v></c:pt><c:pt idx="2"><c:v>9</c:v></c:pt></c:numLit></c:val></c:ser><c:axId val="10"/><c:axId val="20"/></c:barChart><c:catAx><c:axId val="10"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:axPos val="b"/><c:tickLblPos val="nextTo"/><c:crossAx val="20"/><c:crosses val="autoZero"/><c:auto val="1"/><c:lblAlgn val="ctr"/><c:lblOffset val="100"/></c:catAx><c:valAx><c:axId val="20"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:axPos val="l"/><c:majorGridlines/><c:numFmt formatCode="0" sourceLinked="0"/><c:tickLblPos val="nextTo"/><c:crossAx val="10"/><c:crosses val="autoZero"/><c:crossBetween val="between"/></c:valAx></c:plotArea><c:plotVisOnly val="1"/></c:chart></c:chartSpace>'''
comments=f'<w:comments xmlns:w="{NS["w"]}"><w:comment w:id="0" w:author="Revisor de prueba" w:date="2026-10-17T12:00:00Z"><w:p><w:r><w:t>COMENTARIO_01 Comprueba este plazo y conserva el comentario.</w:t></w:r></w:p></w:comment></w:comments>'
foot=f'<w:footnotes xmlns:w="{NS["w"]}"><w:footnote w:type="separator" w:id="-1"><w:p><w:r><w:separator/></w:r></w:p></w:footnote><w:footnote w:id="1"><w:p><w:r><w:footnoteRef/></w:r><w:r><w:t> NOTA_PIE_CONTENIDO_01 Texto de elaboración propia al pie.</w:t></w:r></w:p></w:footnote></w:footnotes>'
end=f'<w:endnotes xmlns:w="{NS["w"]}"><w:endnote w:type="separator" w:id="-1"><w:p><w:r><w:separator/></w:r></w:p></w:endnote><w:endnote w:id="1"><w:p><w:r><w:endnoteRef/></w:r><w:r><w:t> NOTA_FINAL_CONTENIDO_01 Nota final de elaboración propia.</w:t></w:r></w:p></w:endnote></w:endnotes>'
sources='<b:Sources xmlns:b="http://schemas.openxmlformats.org/officeDocument/2006/bibliography" SelectedStyle="/APA.XSL" StyleName="APA"><b:Source><b:Tag>MicrosoftWord2026</b:Tag><b:SourceType>InternetSite</b:SourceType><b:Guid>{6F27DF0F-4057-4B0D-A034-000000000001}</b:Guid><b:Author><b:Author><b:Corporate>Microsoft</b:Corporate></b:Author></b:Author><b:Title>Listen to your Word documents</b:Title><b:InternetSiteTitle>Microsoft Support</b:InternetSiteTitle><b:Year>2026</b:Year><b:URL>https://support.microsoft.com/en-us/word/listen-to-your-word-documents</b:URL></b:Source></b:Sources>'
chartroot=xml(chart)
for name,column,cache in [('strLit','A','strCache'),('numLit','B','numCache')]:
 node=chartroot.find('.//c:'+name,NS);parent=node.getparent();ref=E.Element('{'+NS['c']+'}'+('strRef' if name=='strLit' else 'numRef'));f=E.SubElement(ref,'{'+NS['c']+'}f');f.text=f"Datos!${column}$2:${column}$4";node.tag='{'+NS['c']+'}'+cache;ref.append(node);parent.append(ref)
external=E.SubElement(chartroot,'{'+NS['c']+'}externalData');external.set('{'+NS['r']+'}id','rIdData');E.SubElement(external,'{'+NS['c']+'}autoUpdate',val='0')
wb=Workbook();sheet=wb.active;sheet.title='Datos';sheet.append(['Categoría','Resultados']);sheet.append(['A',12]);sheet.append(['B',18]);sheet.append(['C',9]);xlsx=BytesIO();wb.save(xlsx)
chartrels='<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdData" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/package" Target="../embeddings/DatosGrafico.xlsx"/></Relationships>'
package_patch(master,[('word/charts/chart1.xml',E.tostring(chartroot),'application/vnd.openxmlformats-officedocument.drawingml.chart+xml'),('word/charts/_rels/chart1.xml.rels',chartrels,None),('word/embeddings/DatosGrafico.xlsx',xlsx.getvalue(),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),('word/comments.xml',comments,'application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml'),('word/footnotes.xml',foot,'application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml'),('word/endnotes.xml',end,'application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml'),('customXml/item1.xml',sources,None)],[('rIdAuralisChart','chart','charts/chart1.xml'),('rIdAuralisComments','comments','comments.xml'),('rIdAuralisFootnotes','footnotes','footnotes.xml'),('rIdAuralisEndnotes','endnotes','endnotes.xml')])

d=base('Formularios y límites de paginación')
d.add_heading('Formularios y límites de paginación',0)
d.add_paragraph('Prueba sintética de controles editables, tablas anidadas, filas mayores que una hoja y texto de varias lenguas. Cada control debe conservar su valor y su tipo. Un rótulo que solo parezca un control se registra como conservación parcial.')
for alias,kind,text,opts in [('CONTROL_TEXTO_01','text','Nombre de prueba',None),('CONTROL_LISTA_01','dropDownList','Pendiente',['Pendiente','En revisión','Aprobado']),('CONTROL_FECHA_01','date','17/10/2026',None),('CONTROL_CASILLA_01','checkBox','☐',None)]:
 p=d.add_paragraph(alias+'   ');sdt(p,alias,kind,text,opts)
d.add_heading('Tabla anidada y combinaciones',1)
t=table(d,[['Celda contenedora','Detalle'],['TABLA_ANIDADA_01','Contenido exterior']]);inner=t.cell(1,1).add_table(rows=2,cols=2);inner.cell(0,0).text='INTERIOR_A';inner.cell(0,1).text='INTERIOR_B';inner.cell(1,0).text='INTERIOR_C';inner.cell(1,1).text='INTERIOR_D'
page(d,'Fila mayor que una página','LIMITE_FILA_ALTA')
d.add_paragraph('Se permite dividir la fila para comprobar continuidad. Cada marcador debe aparecer una vez y mantener el orden.')
t=d.add_table(rows=1,cols=1);t.style='Table Grid';c=t.cell(0,0);c.text='FILA_ALTA_INICIO'
for i in range(1,86):c.add_paragraph(f'FILA_ALTA_{i:03} Texto de control para una fila que continúa entre páginas.')
page(d,'Tareas de edición y accesibilidad','INTERACTIVO_01')
for title,text in [('Dictado','Dicta durante un minuto en español e inglés. Comprueba puntuación, salto de párrafo, cursor, deshacer y estado del micrófono. Repite sin conexión y registra el motor utilizado.'),('Lectura en voz alta','Lee selección y documento completo. Comprueba pausa, reanudar, velocidad, cambio de idioma, posición y cancelación al cerrar. Repite sin conexión y observa las solicitudes de red.'),('Macros','En una copia, graba una macro que inserte MARCA_MACRO_01 y aplique negrita. Ejecútala por nombre y guárdala como DOCM. La prueba no requiere modificar el Centro de confianza.'),('Copiar y pegar','Copia dos celdas, una ecuación y un fragmento con comentario. Prueba conservar formato y solo texto. Comprueba que no se acepten cambios ni se dupliquen encabezados.'),('Revisión','Introduce errores deliberados en español, inglés y francés. Comprueba idioma, sugerencias, ignorar, deshacer y conservación de la variante original.'),('Accesibilidad','Revisa títulos, navegación por teclado, texto alternativo, orden de lectura, ampliación y contraste. Prueba la tabla con cabeceras y los controles sin ratón.')]:d.add_heading(title,2);d.add_paragraph(text)
d.save(OUT/'02_Formularios_y_limites.docx')

d=base('Correspondencia y campos condicionales')
d.add_heading('Correspondencia y campos condicionales',0)
d.add_paragraph('Plantilla de prueba con datos ficticios. Selecciona Destinatarios.csv como origen de datos y genera documentos de combinación. No se envía correo ni se imprime físicamente.')
p=d.add_paragraph('Destinatario ');field(p,'MERGEFIELD Nombre','«Nombre»');p.add_run(' ');field(p,'MERGEFIELD Apellido','«Apellido»')
p=d.add_paragraph('Ciudad ');field(p,'MERGEFIELD Ciudad','«Ciudad»')
p=d.add_paragraph('Código ');field(p,'MERGEFIELD Codigo','«Codigo»')
p=d.add_paragraph('Categoría ');field(p,'IF 1 = 1 "Confirmado" "Pendiente"','Confirmado')
d.add_paragraph('MENSAJE_COMBINACION_01 Esta comunicación pertenece al conjunto sintético. Cada salida debe conservar el destinatario, el código y el encabezado. Comprueba vista previa, selección de registros y salida en un documento nuevo.')
d.save(OUT/'03_Correspondencia.docx')
with (OUT/'Destinatarios.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Nombre','Apellido','Ciudad','Codigo']);w.writerows([[f'Persona{i:02}','De Prueba',['Pamplona','Bogotá','Cúcuta'][i%3],f'REG-{i:03}'] for i in range(1,21)])
(OUT/'Macro_de_prueba.bas').write_text('Attribute VB_Name = "AuralisPrueba"\nOption Explicit\nPublic Sub MarcaDePrueba()\n    Selection.TypeText Text:="MARCA_MACRO_01"\n    Selection.Font.Bold = True\nEnd Sub\n',encoding='utf-8')

# Internal performance fixture; not a claim that 500 rendered pages were visually certified.
d=base('Carga controlada de quinientas páginas')
for i in range(1,501):
 if i>1:d.add_page_break()
 d.add_heading(f'Página de control {i:03}',1);d.add_paragraph(f'CARGA_PAGINA_{i:03}_INICIO')
 for j in range(7):d.add_paragraph(f'P{i:03}_B{j:02} Datos sintéticos para medir apertura, búsqueda, edición y recuperación. El texto se conserva sin conexión y no contiene información privada.')
 d.add_paragraph(f'CARGA_PAGINA_{i:03}_FIN')
d.save(OUT/'04_Carga_500_paginas.docx')
generated=['01_Libro_maestro_Word.docx','02_Formularios_y_limites.docx','03_Correspondencia.docx','04_Carga_500_paginas.docx']
for name in generated:package_patch(OUT/name)

sources=[{'title':'Word Associate MO 110','url':'https://arch-center.azureedge.net/Learning/Credentials/MO-110_OD_MOS365_Word.pdf'},{'title':'Word Expert MO 111','url':'https://arch-center.azureedge.net/Learning/Credentials/MO-111_OD_MOS365_WordExpert.pdf'},{'title':'Washburn Tech Word Level 3 Assessment','url':'https://www.washburntech.edu/business-community/files/Word-2016-L3-Assessment_Final.pdf'},{'title':'Dictar documentos en Word','url':'https://support.microsoft.com/es-es/word/dictate-your-documents-in-word'},{'title':'Listen to your Word documents','url':'https://support.microsoft.com/en-us/word/listen-to-your-word-documents'}]
(OUT/'Fuentes.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')
files=[{'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [OUT/name for name in generated]]
(OUT/'Procedencia-generacion.json').write_text(json.dumps({'author':'OscarD0823','builder':'bundled python-docx and standard OOXML','wordNormalized':False,'synthetic':True,'sources':sources,'files':files},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(files,ensure_ascii=False))
