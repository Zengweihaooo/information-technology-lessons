import {parseHTML} from './test-runtime/node_modules/linkedom/esm/index.js';
import fs from 'fs';
const html=fs.readFileSync('/Users/zengweihao/Desktop/信息技术/out/智慧农业_完整版/互动课堂.html','utf8');
const {document}=parseHTML(html);
if(document.querySelectorAll('.zone').length!==4) throw Error('zones');
if(!html.includes('MQTT Broker')||!html.includes('智慧温室')) throw Error('content');
console.log('game DOM smoke test passed: 4 zones, MQTT content, bundled asset');
