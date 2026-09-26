const units={
1:{title:'认识物联网 · 探秘智慧农业示范区',lessons:['认识智慧农业','探索智慧温室大棚','探秘农业物联网云平台','探究智慧农业应用领域']},
2:{title:'物联网实验流程 · 灯光警报呼叫器',lessons:['LED 小灯闪烁','控制蜂鸣器周期响铃','显示警报信息','实现灯光警报呼叫器']},
3:{title:'物联网数据采集 · 温湿度采集器',lessons:['采集环境温度','采集土壤湿度','简易温湿度采集器','警报采集结果','智能温湿度采集器']},
4:{title:'物联网数据传输 · 简易温湿度传输系统',lessons:['物联网数据传输技术','温湿度的蓝牙传输','升级数据传输距离','温湿度远程监测报警','温湿度的报警与响应']}};
const available={'1-1':true,'1-3':true,'1-4':true};
const res={
'1-1':[
['🌾','智慧农业示范区平台','互动课堂网页','lessons/unit-1/lesson-1/课堂探究—智慧农业示范区平台.html','打开网页'],
['🧩','课堂活动管理系统','课堂活动网页','lessons/unit-1/lesson-1/课堂活动管理系统.html','打开网页'],
['📝','课堂小测','课堂练习网页','lessons/unit-1/lesson-1/课堂小测.html','打开网页'],
['📊','课堂小测数据看板','查看测验数据','lessons/unit-1/lesson-1/课堂小测数据看板.html','打开网页'],
['📽️','课件预览 PDF','浏览完整课件','lessons/unit-1/lesson-1/课件预览.pdf','打开 PDF'],
['⬇️','下载可编辑 PPT','PowerPoint 原文件','https://github.com/Zengweihaooo/information-technology-lessons/blob/main/docs/lessons/unit-1/lesson-1/PPT—认识智慧农业.pptx','在 GitHub 下载'],
['✍️','随堂测试','课堂练习网页','lessons/unit-1/lesson-1/随堂测试.html','打开网页']],
'1-3':[
['🧪','互动课堂','探索农业物联网云平台','lessons/unit-1/lesson-3/互动课堂.html','打开网页'],
['📄','课件预览 PDF','浏览完整课件','lessons/unit-1/lesson-3/课件预览.pdf','打开 PDF'],
['⬇️','下载可编辑 PPT','PowerPoint 原文件','lessons/unit-1/lesson-3/探秘农业物联网云平台.pptx','下载课件']],
'1-4':[
['🌱','智慧农场教学网页','突发事件系统设计课堂','lessons/unit-1/lesson-4/智慧农场教学网页.html','打开网页']]
};
function renderIndex(){let grid=document.querySelector('#lesson-grid');if(!grid)return;let tabs=[...document.querySelectorAll('[data-unit]')];function show(u){tabs.forEach(t=>t.classList.toggle('active',t.dataset.unit==u));document.querySelector('#unit-heading').innerHTML=`<h3>第${'一二三四'[u-1]}单元 <small>${units[u].title}</small></h3><small>${units[u].lessons.length} 课</small>`;grid.innerHTML=units[u].lessons.map((name,i)=>{let id=`${u}-${i+1}`,has=available[id],label=`八年级上册 · 第${'一二三四'[u-1]}单元 · 第${i+1}课`;return `<${has?'a':'div'} class="lesson-card ${has?'available':'empty'}" ${has?`href="lesson.html?id=${id}"`:''}><div class="lesson-no">${String(i+1).padStart(2,'0')}</div><div class="lesson-body"><small>${label}</small><h4>${name}</h4><p>${has?'网页与课件资源':'资料整理中'}</p></div><span class="lesson-arrow">${has?'↗':'·'}</span></${has?'a':'div'}>`}).join('')}tabs.forEach(t=>t.addEventListener('click',()=>show(t.dataset.unit)));show(1)}
function renderLesson(){let main=document.querySelector('#lesson-main');if(!main)return;let id=new URLSearchParams(location.search).get('id');if(!available[id]){main.innerHTML='<h1>暂未收录这一课</h1><p><a href="./">返回课程目录</a></p>';return}let [u,n]=id.split('-').map(Number),title=units[u].lessons[n-1],items=res[id];document.title=`第 ${n} 课 · ${title} | 信息科技`;main.innerHTML=`<div class="crumb"><a href="./">首页</a> / 八年级上册 / 第一单元 / 第 ${n} 课</div><div class="lesson-title"><div><div class="tag">GRADE 8 · UNIT 01 · LESSON ${String(n).padStart(2,'0')}</div><h1>${title}</h1><p>8 上第一单元第${'一二三四'[n-1]}课 · 选择以下资源直接进入课堂。</p></div></div><div class="resource-grid">${items.map(([icon,label,desc,url,action])=>`<article class="resource"><div><div class="icon">${icon}</div><h3>${label}</h3><p>${desc}</p></div><a href="${encodeURI(url)}" target="_blank" rel="noopener">${action} ↗</a></article>`).join('')}</div>${[1,3].includes(n)?'<div id="slides-root"></div>':''}`;if([1,3].includes(n))renderSlides(n)}
function renderSlides(n){let count=n===3?33:11;if(!count)return;let dir=`assets/slides/lesson-${n}`,i=1,root=document.querySelector('#slides-root');root.innerHTML=`<section class="viewer" id="viewer"><div class="viewer-top"><span>课件网页演示 · 第 ${n} 课</span><button id="fullscreen">全屏演示 ⛶</button></div><div class="viewer-stage"><img id="slide-image" alt="课件第 1 页"></div><div class="viewer-controls"><button id="prev">← 上一页</button><span id="counter"></span><button id="next">下一页 →</button></div></section>`;let img=root.querySelector('#slide-image'),counter=root.querySelector('#counter'),prev=root.querySelector('#prev'),next=root.querySelector('#next');function show(){img.src=`${dir}/slide-${String(i).padStart(2,'0')}.jpg`;img.alt=`课件第 ${i} 页`;counter.textContent=`${i} / ${count}`;prev.disabled=i===1;next.disabled=i===count}prev.onclick=()=>{i--;show()};next.onclick=()=>{i++;show()};root.querySelector('#fullscreen').onclick=()=>root.querySelector('#viewer').requestFullscreen?.();document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'&&i<count){i++;show()}if(e.key==='ArrowLeft'&&i>1){i--;show()}});show()}
renderIndex();renderLesson();
