import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const ROOT='/Users/zengweihao/Desktop/信息技术',SKILL='/Users/zengweihao/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.22227/skills/presentations';
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(SKILL+'/container_tools/artifact_tool_utils.mjs'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
const C={paper:'#F6EFDF',sheet:'#FFFAF0',ink:'#263E32',green:'#294A3C',soft:'#637265',orange:'#B55731',line:'#D5CBB5',pale:'#E4E9D7',gold:'#D1AD62'},F='HarmonyOS Sans SC',SER='STSong';
const source='教材：教育科学出版社《信息科技 八年级上册》，第1课第3–7页、第2课第8–13页、第3课第14–18页。';
const mqtt='协议核对：https://mqtt.org/ 和 https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html 。MQTT为本课指定重点。';
let num=0;const allNotes=[];
function text(s,t,x,y,w,h,size=26,color=C.ink,bold=false,font=F){const q=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});q.text=t;q.text.style={typeface:font,fontSize:size,color,bold,autoFit:'none'};return q}
function rect(s,x,y,w,h,fill=C.sheet,line='none'){return s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:line,width:line==='none'?0:1}})}
function rule(s,x,y,w,c=C.line){rect(s,x,y,w,2,c)}
function title(s,t,tag){text(s,tag,64,34,1050,26,15,C.orange,true);text(s,t,64,79,1150,68,44,C.green,true,SER);rule(s,64,159,1152)}
function slide(t,tag,notes){let s=p.slides.add();s.background.fill=C.paper;num++;title(s,t,tag);text(s,'探秘农业物联网云平台',64,678,700,24,14,C.soft);text(s,String(num).padStart(2,'0'),1150,674,64,30,20,C.orange,false,SER);let n=`第${num}页 ${t}\n${notes}\n${source}\n${mqtt}\n数据与阈值：教学模拟，不作为农业生产参数。图像：AI辅助生成的教学概念插画，不是实际基地照片。`;s.speakerNotes.textFrame.setText(n);allNotes.push(n);return s}
async function img(s,n,x,y,w,h,fit='cover'){s.images.add({blob:new Uint8Array(await fs.readFile(ROOT+'/build/complete/assets/'+n+'.jpg')),contentType:'image/jpeg',alt:n==='park'?'示范区参观情境插画':n==='greenhouse'?'温室设备概念插画':'网络中控室概念插画',position:{left:x,top:y,width:w,height:h},fit})}
function note(s,t,y=593){rect(s,64,y,1152,56,C.pale);text(s,t,84,y+11,1110,40,23,C.green)}
function para(s,heading,body,x,y,w=500){text(s,heading,x,y,w,42,29,C.green,true,SER);text(s,body,x,y+54,w,140,25)}
function arrow(s,x,y,w=42,dir='right'){s.shapes.add({geometry:dir==='right'?'rightArrow':'downArrow',position:{left:x,top:y,width:dir==='right'?w:24,height:dir==='right'?24:w},fill:C.orange,line:{fill:'none',width:0}})}
function node(s,name,detail,x,y,w=205,h=130,fill=C.sheet){rect(s,x,y,w,h,fill,C.line);text(s,name,x+16,y+18,w-32,40,28,fill===C.green?C.sheet:C.green,true,SER);text(s,detail,x+16,y+66,w-32,h-72,21,fill===C.green?C.sheet:C.soft)}
function table(s,values,x=64,y=190,w=1152,h=350,widths){const tb=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,values,...(widths?{columnWidths:widths}:{})});tb.borders.assign({style:'solid',fill:C.line,width:1});for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){let cell=tb.getCell(r,c);cell.fill=r===0?C.green:r%2?C.sheet:C.pale;cell.text.style={typeface:F,fontSize:23,color:r===0?C.sheet:C.ink,bold:r===0}}return tb}
function chart(s,values,categories,x=70,y=210,w=760,h=340,thresholds=[35]){const series=[{name:'土壤示数',values,line:{fill:C.green,width:3},marker:{symbol:'circle',size:6}}];thresholds.forEach((v,i)=>series.push({name:i?'停止阈值':'启动阈值',values:values.map(()=>v),line:{fill:i?C.soft:C.orange,width:1.5}}));let c=s.charts.add('line',{position:{left:x,top:y,width:w,height:h},categories,series,hasLegend:true,legend:{position:'bottom'},chartFill:C.paper,plotAreaFill:C.sheet,xAxis:{textStyle:{typeface:F,fontSize:18}},yAxis:{min:0,max:100,majorUnit:25,numberFormatCode:'0',majorGridlines:{fill:C.line,width:1},textStyle:{typeface:F,fontSize:18}},lineOptions:{smooth:false}});applyPresentationChartFont(c,{fontFamily:F});return c}
// 01 Cover, a quiet editorial composition with a full illustration.
let s=p.slides.add();num++;s.background.fill=C.paper;await img(s,'park',0,240,1280,480);text(s,'第一单元 认识物联网 / 第3课',64,37,900,30,18,C.orange,true);text(s,'探秘农业物联网云平台',64,95,1160,76,54,C.green,true,SER);text(s,'一号温室缺水了，远处的水阀怎么知道？',67,180,1100,40,27,C.ink);s.speakerNotes.textFrame.setText('封面：先出示问题，不讲MQTT定义。引导学生猜测系统需要哪些信息。图片为AI辅助教学插画。'+source);allNotes.push('第1页 封面\n导入先问：缺水的证据从哪里来？');
s=slide('参观继续：从展厅走到网络中控室','聚焦 / 3分钟','出示第1课、第2课和本课关系。请学生回顾智慧农业功能与传感器任务，说明本课研究信息怎样传递与处理。');
[['第1课','认识智慧农业','知道它能做什么'],['第2课','探索温室大棚','知道数据从哪里来'],['第3课','探秘云平台','知道消息怎样变成行动']].forEach((a,i)=>{let x=70+i*398;text(s,a[0],x,217,350,35,19,C.orange,true);text(s,a[1],x,275,350,48,33,C.green,true,SER);text(s,a[2],x,350,330,70,26);rule(s,x,454,340,C.green);text(s,['监测、查询、报警、控制','土壤、空气、光照等传感器','网络、MQTT、平台规则'][i],x,480,340,85,22,C.soft)});
s=slide('09:00，管理员留下了一张任务单','聚焦 / 真实问题','读任务单。先让学生口头给出系统方案。预期：采集土壤数据、发给平台、判断、控制灌溉。强调后续要验证每个猜想。');
rect(s,64,200,690,340,C.sheet,C.line);text(s,'“我正在另一处大棚巡查。\n请留意一号温室的土壤变化，\n需要时提醒我，并按规则灌溉。”',94,236,630,190,34,C.green,false,SER);text(s,'参观记录员的责任：用证据解释每一步。',94,460,610,42,23,C.orange);para(s,'先猜一猜','系统要知道什么？\n消息交给谁？\n谁真正打开水阀？',817,212,370);note(s,'网页第0站：保存你的初步猜想，课末回看。');
s=slide('同一项浇水任务，两种工作方式','回顾 / 3分钟','用具体动作比较传统与智慧农业，不贬低人的经验。人的规则设置、现场核查仍然重要。');
para(s,'人到现场，观察判断','巡查大棚，查看土壤与作物。\n凭经验选择时机，再操作水阀。\n大棚越多，巡视耗时越长。',72,205,520);para(s,'设备采集，平台辅助','采集数据，集中显示变化。\n平台按阈值提醒，辅助判断。\n人工远程控制或运行自动规则。',678,205,520);rule(s,640,196,1);note(s,'设备帮助人及时获取信息；人的经验用于设置规则和核查异常。');
s=slide('四项功能，回答四个不同的问题','回顾 / 功能辨析','提问：能看到数字就代表自动灌溉了吗？答案：不代表，自动控制还需要规则、设备、通信等。网页第1站完成判断。');
table(s,[['功能','要回答的问题','可以观察到的证据'],['实时监测','现在怎样？','最新土壤、温度等读数'],['历史查询','之前怎样？','曲线、历史照片、操作记录'],['异常报警','哪里需要注意？','超限提示与时间'],['远程控制','怎样采取行动？','人工或规则发出的设备指令']],64,198,1152,350,[230,325,597]);note(s,'议一议：监测、报警和自动控制之间有什么区别？');
s=slide('温室里，谁感知，谁执行？','探索 / 设备观察 4分钟','使用网页第2站热点逐一观察。插画仅作设备概念辨认。土壤探头采集，空气传感器测空气，网关帮助通信，阀门和风机执行。');
await img(s,'greenhouse',64,190,775,435);text(s,'1  土壤湿度探头',877,215,340,40,25,C.green,true);text(s,'2  灌溉阀与驱动',877,289,340,40,25,C.green,true);text(s,'3  通信网关',877,363,340,40,25,C.green,true);text(s,'4  空气温湿度传感器',877,437,340,40,25,C.green,true);text(s,'5  排风机',877,511,340,40,25,C.green,true);text(s,'网页第2站：点击图中设备，\n记录任务与能力边界。',880,585,315,55,18,C.orange);
s=slide('土壤湿度与空气湿度不能混用','探索 / 测量对象','提醒学生区分空气与土壤测量。此页让学生从测量对象理解传感器选择，不把示例百分比当真实土壤体积含水率标准。');
table(s,[['观察对象','设备与示例','用于判断什么'],['根部土壤','土壤探头：示数 28%','土壤含水情况，辅助灌溉'],['温室空气','温湿度传感器：30°C、65% RH','空气环境，辅助通风等调节'],['光照环境','光照传感器：照度值','光照条件，辅助补光或遮阳']],64,198,1152,295,[250,465,437]);text(s,'本课统一使用土壤湿度教学示数演示灌溉。',82,535,1100,44,29,C.orange,true);text(s,'具体阈值需结合传感器标定、作物与生长阶段，不能照搬示例。',82,595,1100,40,23,C.soft);
s=slide('一条读数，要带上哪些信息？','探索 / 数据小档案','避免只显示一个无意义数字。让学生指出设备或位置、数值、单位、时间。时间用于判断数据是否新鲜。');
text(s,'28',90,213,310,170,142,C.green,false,SER);text(s,'只有一个数字，还不够。',91,435,510,55,32,C.orange,true,SER);table(s,[['数据要素','本课记录'],['位置 / 对象','一号棚 / 土壤'],['数值与单位','教学示数 28%'],['采样时间','09:25']],610,205,590,324,[220,370]);note(s,'缺少位置会用错对象；缺少时间可能把旧读数当作现在。');
s=slide('数据离开温室的第一段路','探索 / 连接与转发','图示是本课具体架构，不声明所有设备必经独立网关。说明能力充分的设备可直接联网。');
node(s,'传感器','测到土壤示数',72,274,230);arrow(s,322,326,58);node(s,'终端与网关','汇集或转发数据',400,274,250);arrow(s,670,326,58);node(s,'通信网络','有线 / Wi-Fi / 移动通信',748,274,425);text(s,'无线连接需要考虑距离、遮挡、供电和网络覆盖。',85,470,1120,50,29,C.green);note(s,'本课采用“终端经网络到服务器”的示例；网关不一定是独立必需设备。');
s=slide('网络连接与消息协议各管什么？','能量加油站 / 避免概念混淆','MQTT一般在TCP/IP之上工作。网络技术与消息协议分工不同，不把MQTT讲成无线技术，也不声称MQTT天然比TCP/IP慢或稳定性差。');
para(s,'网络连接','设备是否有路可走？\n例如：以太网、Wi-Fi、移动网络。\n要考虑覆盖、连接与传输条件。',70,210,530);para(s,'MQTT 消息协议','消息怎样发布和订阅？\n用主题组织消息接收关系。\n不负责测量或直接决定无线距离。',676,210,530);note(s,'类比：道路提供通行条件，收寄规则约定包裹如何投递。');
s=slide('说一说：把数据旅程排成一条线','活动 / 链路排序 4分钟','网页第3站拖动或上下移动排序。正确：采集、网络发送、Broker分发、平台判断发布控制、阀门执行并反馈。');
['A  平台规则判断并发指令','B  土壤探头采集读数','C  阀门执行并回传状态','D  Broker 按主题分发','E  终端或网关经网络发送'].forEach((v,i)=>{text(s,v,115,198+i*69,1090,48,30,i%2?C.green:C.ink);rule(s,115,250+i*69,1040)});text(s,'小组用“先……然后……最后……”解释排序依据。',112,592,1060,45,26,C.orange,true);
s=slide('完整链路：数据上行，指令下行','探索 / 参考路径','采用两个方向而非单向流水线。指出平台规则引擎与Broker是不同角色，可部署在同一云平台，也可分开。');
['感知 / 采集','网络发送','Broker 分发','平台规则','执行 / 反馈'].forEach((v,i)=>{node(s,v,['28%','携带主题','匹配订阅','低于阈值？','开阀后再采样'][i],64+i*236,249,207,145,i===3?C.green:C.sheet);if(i<4)arrow(s,276+i*236,308,24)});text(s,'上行：现场读数进入平台',76,202,700,37,25,C.orange,true);rule(s,160,463,950,C.orange);text(s,'下行：平台发布控制消息，控制器接收并驱动设备',172,486,945,50,29,C.green);note(s,'闭环的最后一步：继续采样或读取设备状态，核对动作是否奏效。');
s=slide('网络中控室：数据在这里汇合','探索 / 中控室 4分钟','先展示场景，再切换到数据。学生想象管理员远处查看多个棚。图片为概念插画，不虚构真实拍摄地点。');
await img(s,'room',64,190,780,438);text(s,'分散采集',889,239,302,55,36,C.green,true,SER);text(s,'多个位置、多个设备',892,310,310,55,23);text(s,'集中管理',889,406,302,55,36,C.orange,true,SER);text(s,'同一平台查看与处理',892,475,310,55,23);
s=slide('曲线记录了“刚才发生什么”','探索 / 历史查询','与网页第4站相同数据，09:20首次低于35%。先问学生再出示下一页证据表。所有数据教学构造。');
chart(s,[52,47,43,38,33,28],['09:00','09:05','09:10','09:15','09:20','09:25'],70,220,760,355);text(s,'土壤湿度示数（%）',85,181,670,30,20,C.soft);text(s,'第一次低于 35%\n是什么时候？',889,242,325,115,34,C.green,true,SER);text(s,'请指出相邻两次采样，\n用数值支持你的判断。',889,413,320,105,24,C.ink);note(s,'最新读数为 28%；“最新值”和“首次越界时间”是不同信息。');
s=slide('用原始记录验证你的判断','探索 / 证据表','09:15为38%，09:20为33%。解释时间戳与采样间隔：只能说09:20这次采样首次观测到低于阈值，不能精确知道两次采样间何时越界。');
table(s,[['采样时间','土壤示数','空气温度','观察结论'],['09:10','43%','28°C','未低于35%'],['09:15','38%','29°C','未低于35%'],['09:20','33%','29.5°C','首次观测到低于35%'],['09:25','28%','30°C','最新读数仍偏低']],64,200,1152,328,[220,250,260,422]);note(s,'采样有间隔：09:20 是首次“观测到”越界，不代表实际越界恰好发生在这一刻。');
s=slide('MQTT：发布、分发、订阅','能量加油站 / 核心实验 7分钟','术语从具体消息出发。发布者和订阅者都是客户端角色，一个设备可兼任。Broker一般不判断作物是否缺水。');
node(s,'发布者','土壤采集终端',70,248,290,165);arrow(s,376,306,60);node(s,'Broker','MQTT 消息服务器',457,248,310,165,C.green);arrow(s,786,306,60);node(s,'订阅者','云平台程序 / 手机',867,248,340,165);text(s,'发给服务器',85,459,295,35,25,C.orange);text(s,'根据主题与订阅分发',464,459,350,35,25,C.orange);text(s,'接收自己关心的消息',884,459,330,35,25,C.orange);note(s,'平台规则负责农业判断；Broker 负责消息分发，两者可以协同部署。');
s=slide('一条 MQTT 消息的两部分','能量加油站 / 主题与内容','主题示例是课堂自行约定，不是MQTT固定写法。JSON是应用格式，MQTT不强制。用字面数据解释，不需要学生写程序。');
text(s,'主题 Topic',75,203,530,45,30,C.orange,true);text(s,'farm/1/soil',75,271,650,70,47,C.green,true);text(s,'示例农场 / 一号棚 / 土壤',77,361,600,45,25);rule(s,75,426,1090);text(s,'消息内容 Payload',75,463,500,40,28,C.orange,true);text(s,'{"value": 28, "unit": "%"}',550,458,640,67,34,C.green,true);note(s,'主题说明消息类别；本实验用 JSON 装数值。其他内容格式也可以。');
s=slide('发布之前，先明确谁订阅了什么','活动 / 对照实验①','网页第5站先发布再订阅，观察没有手机消息；订阅后重新发布收到消息。本实验没有保留消息，也不模拟持久会话。');
table(s,[['动作','手机的状态','预期结果'],['还没订阅，先发布','尚无订阅','手机不会因此收到这条消息'],['订阅 farm/1/soil','已登记接收主题','等待后续匹配消息'],['再次发布 farm/1/soil','主题匹配','手机收到新消息']],64,200,1152,300,[380,300,472]);text(s,'为什么订阅以后，还要再发布一次？',83,549,1090,46,31,C.orange,true,SER);text(s,'本实验只演示新消息，不补发之前未保留的消息。',84,608,1080,38,23,C.soft);
s=slide('换一个棚号，消息还会到手机吗？','活动 / 对照实验②','保持手机订阅farm/1/soil，把发布主题改成farm/2/soil。不匹配就不会投递。大小写敏感。然后改为farm/+/soil挑战单层匹配。');
text(s,'手机订阅',76,205,500,40,27,C.soft);text(s,'farm/1/soil',76,265,580,62,44,C.green,true);text(s,'本次发布',708,205,500,40,27,C.soft);text(s,'farm/2/soil',708,265,490,62,44,C.orange,true);rule(s,78,380,1120);text(s,'棚号不同，精确订阅不匹配。',85,425,1100,60,35,C.green,true,SER);note(s,'挑战：farm/+/soil 中的 + 匹配一个层级；主题大小写要一致。');
s=slide('订阅、网络与实际动作是三道检查','活动 / 对照实验③','断开Broker连接，对照前面主题错误。讲清消息服务质量不代表执行设备已完成机械动作，不需要深入QoS实现。');
['连接是否正常？','主题是否匹配？','设备是否执行？'].forEach((t,i)=>{text(s,'0'+(i+1),74,211+i*112,86,60,44,C.orange,false,SER);text(s,t,202,211+i*112,400,55,32,C.green,true,SER);text(s,['离线时，新消息可能无法送达。','服务器按订阅关系选择接收方。','需要读取设备状态或后续数据。'][i],665,216+i*112,530,75,24)});note(s,'不要把“点了发送”“Broker 收到”“水阀打开”当作同一件事。');
s=slide('从消息到决定：写出一条控制规则','实践 / 规则实验 6分钟','结合课堂代码：低于35开阀，达到55关阀，中间保持原状态。第一次先让学生预测，不马上运行。');
text(s,'如果有效土壤示数低于',76,220,600,60,34,C.green,true,SER);text(s,'35%',780,194,400,96,72,C.orange,false,SER);text(s,'发布开阀指令',76,303,520,50,32,C.ink);rule(s,75,388,1110);text(s,'如果有效土壤示数达到',76,436,600,60,34,C.green,true,SER);text(s,'55%',780,410,400,96,72,C.orange,false,SER);text(s,'发布关阀指令',76,521,520,50,32,C.ink);text(s,'教学示例阈值，不能作为种植参数。',790,542,390,70,21,C.soft);
s=slide('两个阈值之间，保持原状态','实践 / 边界条件','用数轴解释滞回而不要求术语记忆。35%不会从关闭转开启，55%会关闭。模拟阀门反馈时需要说明先判断再推进环境读数。');
rect(s,85,282,340,90,'#F1DFCD');rect(s,425,282,360,90,C.pale);rect(s,785,282,400,90,'#DAE4CE');text(s,'低于 35%',116,303,285,45,31,C.orange,true);text(s,'35% 至低于 55%',449,303,320,45,27,C.green,true);text(s,'达到 55%',823,303,330,45,31,C.green,true);text(s,'自动开阀',110,421,300,50,29,C.orange);text(s,'保持原状态',449,421,315,50,29,C.green);text(s,'自动关阀',824,421,310,50,29,C.green);note(s,'保持区间可减少读数在临界值附近波动造成的频繁开关。');
s=slide('灌溉后，曲线应该发生什么变化？','实践 / 因果预测','示意值来自与网页一致的简化模型：开阀每步+8，关阀每步-2，变化并非真实土壤物理模型。0=28，1=36，2=44，3=52，4=60，5=58。第五步判断60>=55而关阀。');
chart(s,[28,36,44,52,60,58],['0','1','2','3','4','5'],65,230,780,360,[35,55]);text(s,'土壤湿度教学示数（%）',79,182,790,30,20,C.soft);text(s,'先预测，再运行',885,214,313,50,31,C.green,true,SER);text(s,'哪一步触发开阀？\n哪一步触发关阀？\n谁提供动作效果证据？',887,300,320,170,25);text(s,'横轴：模拟时间（分钟）',895,523,300,60,19,C.soft);
s=slide('一次完整实验需要留下哪些证据？','实践 / 小组记录','安排两人一组，一人操作一人记录。不要仅记录按钮动作，要写传感器值、规则判断与阀门反馈。');
table(s,[['操作步骤','重点观察','记录内容'],['初始28%，推进一次','规则是否命中','初始值、ON指令、阀门反馈'],['继续推进到停止条件','停止阈值是否生效','关阀前读数与OFF反馈'],['修改其中一个阈值','动作时机如何改变','对照前后差异'],['注入故障并再推进','指令与执行是否一致','故障证据与下一步检查']],64,202,1152,330,[380,350,422]);note(s,'网页第6站：支持逐步运行、连续运行、人工模式与三种故障。');
s=slide('故障会诊：按证据找环节','议一议 / 可选挑战 3分钟','对应网页第7站三题。先排除已确认正常的部分再说优先检查点。不给出“某现象一定等于某唯一故障”的过度结论。');
table(s,[['症状','现有证据','优先检查'],['手机无新消息','Broker有1号棚消息，手机订阅2号棚','主题与订阅关系'],['发出ON但没有水','网络在线，阀门反馈仍为OFF','阀门、驱动与反馈'],['大屏数字不变','时间戳停在09:10，网关心跳丢失','连接、过期数据提示']],64,202,1152,315,[250,560,342]);note(s,'不要只清除告警；先确认数据新鲜、连接正常、指令和反馈一致。');
s=slide('设计：给消息起一个清楚的主题名','设计 / 关键词准备','小组使用farm/棚号/数据种类的约定。不要给学生造成主题必须中文或必须英文的误解，约定只为课堂简化。');
text(s,'farm/1/soil',80,213,1100,90,67,C.green,true);text(s,'位置层级',82,352,290,45,28,C.orange,true);text(s,'对象类别',477,352,320,45,28,C.orange,true);text(s,'消息内容',904,352,305,45,28,C.orange,true);text(s,'一号棚 / 二号棚',81,410,360,75,26);text(s,'soil / temperature / valve',477,410,370,85,24);text(s,'读数或开关指令',904,410,285,85,26);note(s,'请写一个发布主题，并说明谁发布、谁订阅、消息内容是什么。');
s=slide('把本课内容接回单元思维导图','设计与实践 / 5分钟','教材要求在智慧农业示范区文件中添加农业物联网云平台分支。学生在网页写关键词后，可以转回常用思维导图软件组织分支与连线。');
node(s,'智慧农业示范区','单元中心主题',64,280,286,130,C.green);arrow(s,366,334,55);node(s,'农业物联网云平台','本课子主题',441,280,310,130,C.pale);[[810,202,'数据与设备'],[810,309,'平台功能'],[810,416,'MQTT 关系'],[810,523,'控制规则']].forEach(([x,y,t])=>{rect(s,x,y,385,68,C.sheet,C.line);text(s,t,x+20,y+17,340,45,29,C.green,true,SER)});rule(s,751,343,24,C.orange);rule(s,773,235,30,C.orange);rect(s,773,235,2,319,C.orange);[235,342,449,556].forEach(y=>rule(s,773,y,36,C.orange));
s=slide('关键词之间，还要写出关系','实践 / 作品示例','此页作参考，不让学生照抄全文。要求用自己的词解释因果，支持一个节点多分支。');
para(s,'数据与平台','土壤探头测到 28%。\n终端把读数经网络发往服务器。\n平台集中显示、存储和分析。',70,199,525);para(s,'消息与动作','终端发布 farm/1/soil。\n规则程序订阅并判断。\n控制器接收阀门主题的 ON/OFF。',679,199,525);note(s,'再补一条反馈关系：阀门执行后继续采样，检验土壤变化。');
s=slide('同伴互评：解释是否有依据？','评价 / 每项1分','共4分。网页结构检查仅验证有内容，不判定知识准确。请同伴用量规复述对方系统，并指出一处可改进点。');
table(s,[['评价维度','得分证据','分值'],['链路清楚','说明采集、网络、平台与执行关系','1'],['功能具体','写出监测、查询、报警或控制的例子','1'],['MQTT准确','说明主题、发布、Broker、订阅关系','1'],['规则完整','有有效数据、启动/停止条件、动作或反馈','1']],64,202,1152,330,[250,785,117]);note(s,'同伴说得出你的系统怎样工作，比堆很多名词更重要。');
s=slide('出口检测：先独立作答，再讲理由','评价 / 3分钟','对应网页8题中的代表题。答案1=消息协议，2=不匹配不投递，3=不能把旧数据当新数据。网页保留首次与订正后的成绩，避免重复点击加分。');
[['01','MQTT 解决什么问题？','消息怎样发布和订阅，还是无线信号能传多远？'],['02','订阅1号棚，发布2号棚？','手机会收到吗？请用“主题”解释。'],['03','数值没变，时间却停了？','你应该相信它，还是先检查连接和时间戳？']].forEach((a,i)=>{text(s,a[0],70,203+i*126,90,65,42,C.orange,false,SER);text(s,a[1],195,204+i*126,970,48,31,C.green,true,SER);text(s,a[2],195,260+i*126,970,55,25)});
s=slide('拓展：把这套思路带进教室','拓展 / 课后选做','选择空气质量或照明案例即可。测量对象、订阅者、动作清楚，并考虑误测、断网、权限。只做模型推理不要求真实安装传感器。');
text(s,'教室空气质量监测',71,207,1120,62,40,C.green,true,SER);table(s,[['采集什么','谁接收消息','可能采取的行动'],['空气质量相关指标','教师终端 / 管理平台','提醒核查，按条件通风']],64,302,1152,175,[340,400,412]);text(s,'进一步思考：传感器出错、网络断开、陌生人发指令时怎么办？',77,535,1110,70,28,C.orange,true);
s=slide('回到开头：水阀怎么知道番茄缺水？','课堂收束 / 回看猜想','让学生在网页第9站完成系统解释与迁移想法，下载学习单。强调土壤读数是判断依据之一，规则为人为设定，不是水阀自己知道。');
text(s,'它依靠一套协作过程。',80,210,1120,65,43,C.green,true,SER);text(s,'探头提供数据，网络传递消息。\nBroker 按主题分发，平台按规则判断。\n控制器驱动水阀，后续数据检验结果。',86,315,1110,210,33,C.ink);note(s,'把“出发前的猜想”改写成一段有设备、有消息、有规则的解释。');
s=slide('学习资料与实验约定','参考 / 教师备课页','此页可不在课堂逐条讲解。供教师核查教材来源与扩展内容。与用户原教材一致，MQTT作为重点替换讲解。概念插画用于课堂情境观察。');
text(s,'教材依据',80,196,1060,35,26,C.orange,true);text(s,'教育科学出版社《信息科技 八年级上册》\n第1课 3–7页；第2课 8–13页；第3课 14–18页。',81,245,1090,95,26);text(s,'MQTT 资料',80,370,1060,35,26,C.orange,true);text(s,'mqtt.org\ndocs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html',81,415,1110,85,24);text(s,'教学约定',80,538,1060,35,26,C.orange,true);text(s,'数据、阈值与变化速度均为教学模拟；插画是概念图。',81,583,1100,50,25);
await fs.mkdir(ROOT+'/build/complete/finalizer',{recursive:true});
const candidate=ROOT+'/build/complete/candidate.pptx';await(await PresentationFile.exportPptx(p)).save(candidate);
await fs.writeFile(ROOT+'/build/complete/notes.txt',allNotes.join('\n\n──────────\n\n'));
console.log('Exported',num,'slides. Finalizing...');
const final=ROOT+'/out/智慧农业_完整版/探秘农业物联网云平台.pptx';
const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath:final,pythonExecutable:'/Users/zengweihao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:SKILL+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:SKILL+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],fontPolicy:{basis:'design',families:[F,SER]},materializeLiteralChartWorkbooks:true,verifyArtifactToolImport:true,receiptPath:ROOT+'/build/complete/finalizer/validation-delivery.json'});
console.log(JSON.stringify(result));
