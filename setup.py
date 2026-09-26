from pathlib import Path
from shutil import copy2, copytree
root=Path(__file__).resolve().parent
src=root.parent

def put(a,b):
 p=src/a;q=root/b;q.parent.mkdir(parents=True,exist_ok=True);copy2(p,q)
put(Path('out/智慧农场_突发事件系统设计课堂.html'),Path('docs/lessons/unit-1/lesson-4/智慧农场教学网页.html'))
put(Path('out/智慧农业_完整版/互动课堂.html'),Path('docs/lessons/unit-1/lesson-3/互动课堂.html'))
put(Path('out/智慧农业_完整版/探秘农业物联网云平台.pptx'),Path('docs/lessons/unit-1/lesson-3/探秘农业物联网云平台.pptx'))
put(Path('out/智慧农业_完整版/课件预览.pdf'),Path('docs/lessons/unit-1/lesson-3/课件预览.pdf'))
put(Path('out/智慧农业_完整版/教师使用说明.md'),Path('final/八年级上册/第一单元/第3课/教师使用说明.md'))
put(Path('out/智慧农业_完整版/课件封面.png'),Path('docs/assets/lesson-3-cover.png'))
for name in ['课堂探究—智慧农业示范区平台.html','课堂活动管理系统.html']:
 put(Path('8年级上册/1.1认识智慧农业')/name,Path('docs/lessons/unit-1/lesson-1')/name)
for name in ['课堂小测.html','课堂小测数据看板.html']:
 put(Path('8年级上册/1.1认识智慧农业/课堂小测')/name,Path('docs/lessons/unit-1/lesson-1')/name)
put(Path('8年级上册/第一单元/第1课 认识智慧农业/随堂测试.html'),Path('docs/lessons/unit-1/lesson-1/随堂测试.html'))
put(Path('8年级上册/章节目录.md'),Path('课程目录.md'))
for p in (src/'output').glob('*.pptx'):
 put(p.relative_to(src),Path('drafts/八年级上册/第一单元/第3课/PPT迭代')/p.name)
for p in (src/'out').glob('*.html'):
 if p.name!='智慧农场_突发事件系统设计课堂.html':
  put(p.relative_to(src),Path('drafts/八年级上册/第一单元/第3课/网页迭代')/p.name)
for p in (src/'out').glob('*.pptx'):
 put(p.relative_to(src),Path('drafts/八年级上册/第一单元/第3课/PPT迭代')/p.name)
for p in (src/'build').rglob('*'):
 if p.is_file() and p.suffix in {'.py','.mjs','.js','.css','.html','.txt','.json'} and 'node_modules' not in p.parts:
  put(p.relative_to(src),Path('drafts/构建源码')/p.relative_to(src/'build'))
for p in (src/'out/video_cloud_platform_analysis').rglob('*'):
 if p.is_file() and not p.name.startswith('.') and (p.suffix in {'.sh','.bak','.mp4'} or '可编辑草稿' in p.name):
  put(p.relative_to(src),Path('drafts/八年级上册/第一单元/第3课/视频')/p.relative_to(src/'out/video_cloud_platform_analysis'))
for p in (src/'out/智慧农场素材').glob('*'):
 if p.is_file():put(p.relative_to(src),Path('final/八年级上册/第一单元/第4课/素材')/p.name)
put(Path('out/智慧农业课堂材料.zip'),Path('drafts/八年级上册/第一单元/第3课/智慧农业课堂材料.zip'))
put(Path('out/第3课_探秘农业物联网云平台.pptx'),Path('drafts/八年级上册/第一单元/第3课/PPT迭代/第3课_探秘农业物联网云平台.pptx'))
for p in (src/'8年级上册/1.1认识智慧农业').rglob('*'):
 if p.is_file() and p.suffix=='.html':
  put(p.relative_to(src),Path('drafts/八年级上册/第一单元/第1课')/p.relative_to(src/'8年级上册/1.1认识智慧农业'))
