from pathlib import Path
import base64, zipfile
root=Path('/Users/zengweihao/Desktop/信息技术')
h=(root/'build/complete/game.html').read_text(); css=(root/'build/complete/game.css').read_text(); js=(root/'build/complete/game.js').read_text()
img=base64.b64encode((root/'build/complete/assets/park.jpg').read_bytes()).decode()
out=h.replace('/*CSS*/',css).replace('/*JS*/',js).replace('IMAGE_PARK','data:image/jpeg;base64,'+img)
target=root/'out/智慧农业_完整版/互动课堂.html'; target.write_text(out)
zip_path=root/'out/智慧农业课堂材料.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in [root/'out/智慧农业_完整版/互动课堂.html',root/'out/智慧农业_完整版/探秘农作物物联网云平台.pptx',root/'out/智慧农业_完整版/教师使用说明.md']:
  if p.exists(): z.write(p,p.name)
print(target, target.stat().st_size, zip_path.stat().st_size)
