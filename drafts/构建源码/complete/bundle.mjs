import fs from 'node:fs/promises';
import sharp from 'sharp';
const base=new URL('.',import.meta.url);
let html=await fs.readFile(new URL('index.template.html',base),'utf8');
const css=await fs.readFile(new URL('style.css',base),'utf8'),app=await fs.readFile(new URL('app.js',base),'utf8');
html=html.replace('/*STYLE*/',()=>css).replace('/*APP*/',()=>app);
for(const n of ['park','greenhouse','room']){
 const bytes=await sharp(await fs.readFile(new URL('assets/'+n+'.png',base))).resize({width:1500,withoutEnlargement:true}).jpeg({quality:88}).toBuffer();
 await fs.writeFile(new URL('assets/'+n+'.jpg',base),bytes);
 html=html.replace('{{'+n+'}}','data:image/jpeg;base64,'+bytes.toString('base64'));
}
await fs.writeFile(new URL('../../out/智慧农业_完整版/互动课堂.html',base),html);
console.log('Standalone HTML written:',html.length);
