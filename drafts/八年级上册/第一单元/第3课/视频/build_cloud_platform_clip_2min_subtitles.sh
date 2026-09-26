#!/usr/bin/env bash
set -euo pipefail

SOURCE_VIDEO="/Users/zengweihao/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_szw624gslah521_1f3c/msg/video/2026-09/870dca908919ae1518b3cc4f9cfaea7e_raw.mp4"
BASE_DIR="/Users/zengweihao/Desktop/信息技术/out/video_cloud_platform_analysis"
SOURCE_DRAFT="$BASE_DIR/drafts/cloud-platform-source"
EDIT_DRAFT="$BASE_DIR/物联网云平台四功能_两分钟_可编辑草稿"
FINAL_VIDEO="$BASE_DIR/物联网云平台四功能_两分钟课堂片段_底部字幕.mp4"
LABEL_DIR="$BASE_DIR/labels_2min"

# Four selected sections, ordered as the lesson flow:
# A 03:16.845–03:50.000  devices and farm equipment connecting to the platform
# B 11:13.000–11:32.000  field collection, upload to the data centre, QR traceability
# C 04:01.643–04:30.000  data transmission/storage/analysis and dashboards
# D 05:04.640–05:43.000  greenhouse monitoring and data-driven equipment control
A_START="196.845"; A_DURATION="33.155"; A_END="230.000"
B_START="673.000"; B_DURATION="19.000"
C_START="241.643"; C_DURATION="28.357"
D_START="304.640"; D_DURATION="38.360"
T_B="33.155"; T_C="52.155"; T_D="80.512"; TOTAL_DURATION="118.872"

if [[ ! -f "$SOURCE_VIDEO" || ! -e "$SOURCE_DRAFT" ]]; then
  echo "Required source video or source draft is missing." >&2
  exit 1
fi

mkdir -p "$LABEL_DIR"

if [[ ! -e "$EDIT_DRAFT" ]]; then
  capcut cut "$SOURCE_DRAFT" "$A_START" "$A_END" --out "$EDIT_DRAFT"

  added_b=$(capcut add-video "$EDIT_DRAFT" "$SOURCE_VIDEO" "$T_B" 692.000 --track-name video)
  echo "$added_b"
  id_b=$(printf '%s' "$added_b" | jq -r '.segment_id')
  capcut trim "$EDIT_DRAFT" "$id_b" "$B_START" "$B_DURATION"

  added_c=$(capcut add-video "$EDIT_DRAFT" "$SOURCE_VIDEO" "$T_C" 270.000 --track-name video)
  echo "$added_c"
  id_c=$(printf '%s' "$added_c" | jq -r '.segment_id')
  capcut trim "$EDIT_DRAFT" "$id_c" "$C_START" "$C_DURATION"

  added_d=$(capcut add-video "$EDIT_DRAFT" "$SOURCE_VIDEO" "$T_D" 343.000 --track-name video)
  echo "$added_d"
  id_d=$(printf '%s' "$added_d" | jq -r '.segment_id')
  capcut trim "$EDIT_DRAFT" "$id_d" "$D_START" "$D_DURATION"

  capcut add-text "$EDIT_DRAFT" 0 "$A_DURATION" \
    "01 设备互联：传感器、农机接入云平台" \
    --font-size 16 --color '#FFFFFF' --align 1 --x 0 --y 0.78 --track-name "底部字幕"
  capcut add-text "$EDIT_DRAFT" "$T_B" "$B_DURATION" \
    "02 数据汇聚：采集数据上传数据中心" \
    --font-size 16 --color '#FFFFFF' --align 1 --x 0 --y 0.78 --track-name "底部字幕"
  capcut add-text "$EDIT_DRAFT" "$T_C" "$C_DURATION" \
    "03 查看与分析：平台仪表盘发现变化" \
    --font-size 16 --color '#FFFFFF' --align 1 --x 0 --y 0.78 --track-name "底部字幕"
  capcut add-text "$EDIT_DRAFT" "$T_D" "$D_DURATION" \
    "04 决策与控制：依据数据自动调节设备" \
    --font-size 16 --color '#FFFFFF' --align 1 --x 0 --y 0.78 --track-name "底部字幕"
fi

font="/System/Library/Fonts/STHeiti Medium.ttc"
magick -size 450x42 xc:none -fill '#0E3A26D9' -draw 'roundrectangle 0,0 449,41 10,10' \
  -font "$font" -pointsize 16 -fill white -gravity center \
  -annotate +0+0 '01 设备互联：传感器、农机接入云平台' "$LABEL_DIR/01.png"
magick -size 450x42 xc:none -fill '#0E3A26D9' -draw 'roundrectangle 0,0 449,41 10,10' \
  -font "$font" -pointsize 16 -fill white -gravity center \
  -annotate +0+0 '02 数据汇聚：采集数据上传数据中心' "$LABEL_DIR/02.png"
magick -size 450x42 xc:none -fill '#0E3A26D9' -draw 'roundrectangle 0,0 449,41 10,10' \
  -font "$font" -pointsize 16 -fill white -gravity center \
  -annotate +0+0 '03 查看与分析：平台仪表盘发现变化' "$LABEL_DIR/03.png"
magick -size 450x42 xc:none -fill '#0E3A26D9' -draw 'roundrectangle 0,0 449,41 10,10' \
  -font "$font" -pointsize 16 -fill white -gravity center \
  -annotate +0+0 '04 决策与控制：依据数据自动调节设备' "$LABEL_DIR/04.png"

if [[ ! -e "$FINAL_VIDEO" ]]; then
  ffmpeg -hide_banner -loglevel error \
    -ss "$A_START" -t "$A_DURATION" -i "$SOURCE_VIDEO" \
    -ss "$B_START" -t "$B_DURATION" -i "$SOURCE_VIDEO" \
    -ss "$C_START" -t "$C_DURATION" -i "$SOURCE_VIDEO" \
    -ss "$D_START" -t "$D_DURATION" -i "$SOURCE_VIDEO" \
    -loop 1 -i "$LABEL_DIR/01.png" -loop 1 -i "$LABEL_DIR/02.png" \
    -loop 1 -i "$LABEL_DIR/03.png" -loop 1 -i "$LABEL_DIR/04.png" \
    -filter_complex \
    "[0:v]setpts=PTS-STARTPTS[v0];[0:a]asetpts=PTS-STARTPTS[a0];\
     [1:v]setpts=PTS-STARTPTS[v1];[1:a]asetpts=PTS-STARTPTS[a1];\
     [2:v]setpts=PTS-STARTPTS[v2];[2:a]asetpts=PTS-STARTPTS[a2];\
     [3:v]setpts=PTS-STARTPTS[v3];[3:a]asetpts=PTS-STARTPTS[a3];\
     [v0][a0][v1][a1][v2][a2][v3][a3]concat=n=4:v=1:a=1[base][aout];\
     [4:v]format=rgba[l1];[5:v]format=rgba[l2];[6:v]format=rgba[l3];[7:v]format=rgba[l4];\
     [base][l1]overlay=15:216:enable='between(t,0,33.155)'[o1];\
     [o1][l2]overlay=15:216:enable='between(t,33.155,52.155)'[o2];\
     [o2][l3]overlay=15:216:enable='between(t,52.155,80.512)'[o3];\
     [o3][l4]overlay=15:216:enable='between(t,80.512,118.872)'[vout]" \
    -map '[vout]' -map '[aout]' -t "$TOTAL_DURATION" \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
    -c:a aac -b:a 128k -movflags +faststart \
    "$FINAL_VIDEO"
fi

capcut lint "$EDIT_DRAFT" --max-cue-secs 120 --max-chars 40
capcut segments "$EDIT_DRAFT" -H
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=index,codec_type,codec_name,width,height \
  -of json "$FINAL_VIDEO"
