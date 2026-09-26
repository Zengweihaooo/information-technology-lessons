#!/usr/bin/env bash
set -euo pipefail

SOURCE_VIDEO="/Users/zengweihao/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_szw624gslah521_1f3c/msg/video/2026-09/870dca908919ae1518b3cc4f9cfaea7e_raw.mp4"
BASE_DIR="/Users/zengweihao/Desktop/信息技术/out/video_cloud_platform_analysis"
SOURCE_DRAFT="$BASE_DIR/drafts/cloud-platform-source"
EDIT_DRAFT="$BASE_DIR/物联网云平台四功能_可编辑草稿_含11分13秒片段_最终"
FINAL_VIDEO="$BASE_DIR/物联网云平台四功能_课堂片段_含11分13秒_2分59秒.mp4"
LABEL_DIR="$BASE_DIR/labels"

# Timeline order:
# A 03:16.845–04:01.643  设备接入画面
# B 11:13.000–11:33.000  数据采集、上传数据中心、二维码追溯
# C 04:01.643–05:56.323  数据汇聚、分析和自动控制
A_START="196.845"
A_END="241.643"
A_DURATION="44.798"
B_START="673.000"
B_DURATION="20.000"
C_START="241.643"
C_DURATION="114.680"
TOTAL_DURATION="179.478"

if [[ ! -f "$SOURCE_VIDEO" || ! -e "$SOURCE_DRAFT" ]]; then
  echo "Required source video or source draft is missing." >&2
  exit 1
fi

mkdir -p "$LABEL_DIR"

if [[ ! -e "$EDIT_DRAFT" ]]; then
  capcut cut "$SOURCE_DRAFT" "$A_START" "$A_END" --out "$EDIT_DRAFT"

  added_b=$(capcut add-video "$EDIT_DRAFT" "$SOURCE_VIDEO" "$A_DURATION" 693.000 --track-name video)
  echo "$added_b"
  id_b=$(printf '%s' "$added_b" | jq -r '.segment_id')
  capcut trim "$EDIT_DRAFT" "$id_b" "$B_START" "$B_DURATION"

  added_c=$(capcut add-video "$EDIT_DRAFT" "$SOURCE_VIDEO" 64.798 356.323 --track-name video)
  echo "$added_c"
  id_c=$(printf '%s' "$added_c" | jq -r '.segment_id')
  capcut trim "$EDIT_DRAFT" "$id_c" "$C_START" "$C_DURATION"

  capcut add-text "$EDIT_DRAFT" 0 "$A_DURATION" \
    "01 设备互联｜传感器、农机接入平台" \
    --font-size 18 --color '#FFFFFF' --align 0 --x -0.72 --y -0.78 --track-name "功能提示"

  capcut add-text "$EDIT_DRAFT" "$A_DURATION" 42.370 \
    "02 数据汇聚｜采集数据传到数据中心" \
    --font-size 18 --color '#FFFFFF' --align 0 --x -0.72 --y -0.78 --track-name "功能提示"

  capcut add-text "$EDIT_DRAFT" 87.168 40.627 \
    "03 查看与分析｜发现变化和异常" \
    --font-size 18 --color '#FFFFFF' --align 0 --x -0.72 --y -0.78 --track-name "功能提示"

  capcut add-text "$EDIT_DRAFT" 127.795 51.683 \
    "04 决策与控制｜依据数据调节设备" \
    --font-size 18 --color '#FFFFFF' --align 0 --x -0.72 --y -0.78 --track-name "功能提示"
fi

font="/System/Library/Fonts/STHeiti Medium.ttc"
magick -size 450x42 xc:none \
  -fill '#1F6D3CBF' -draw 'roundrectangle 0,0 449,41 10,10' \
  -font "$font" -pointsize 18 -fill white -gravity west \
  -annotate +12+0 '01 设备互联｜传感器、农机接入平台' "$LABEL_DIR/01.png"
magick -size 450x42 xc:none \
  -fill '#1F6D3CBF' -draw 'roundrectangle 0,0 449,41 10,10' \
  -font "$font" -pointsize 18 -fill white -gravity west \
  -annotate +12+0 '02 数据汇聚｜采集数据传到数据中心' "$LABEL_DIR/02.png"
magick -size 450x42 xc:none \
  -fill '#1F6D3CBF' -draw 'roundrectangle 0,0 449,41 10,10' \
  -font "$font" -pointsize 18 -fill white -gravity west \
  -annotate +12+0 '03 查看与分析｜发现变化和异常' "$LABEL_DIR/03.png"
magick -size 450x42 xc:none \
  -fill '#1F6D3CBF' -draw 'roundrectangle 0,0 449,41 10,10' \
  -font "$font" -pointsize 18 -fill white -gravity west \
  -annotate +12+0 '04 决策与控制｜依据数据调节设备' "$LABEL_DIR/04.png"

if [[ ! -e "$FINAL_VIDEO" ]]; then
  ffmpeg -hide_banner -loglevel error \
    -ss "$A_START" -t "$A_DURATION" -i "$SOURCE_VIDEO" \
    -ss "$B_START" -t "$B_DURATION" -i "$SOURCE_VIDEO" \
    -ss "$C_START" -t "$C_DURATION" -i "$SOURCE_VIDEO" \
    -loop 1 -i "$LABEL_DIR/01.png" \
    -loop 1 -i "$LABEL_DIR/02.png" \
    -loop 1 -i "$LABEL_DIR/03.png" \
    -loop 1 -i "$LABEL_DIR/04.png" \
    -filter_complex \
    "[0:v]setpts=PTS-STARTPTS[v0];[0:a]asetpts=PTS-STARTPTS[a0];\
     [1:v]setpts=PTS-STARTPTS[v1];[1:a]asetpts=PTS-STARTPTS[a1];\
     [2:v]setpts=PTS-STARTPTS[v2];[2:a]asetpts=PTS-STARTPTS[a2];\
     [v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[base][aout];\
     [3:v]format=rgba[l1];[4:v]format=rgba[l2];[5:v]format=rgba[l3];[6:v]format=rgba[l4];\
     [base][l1]overlay=15:12:enable='between(t,0,44.798)'[o1];\
     [o1][l2]overlay=15:12:enable='between(t,44.798,87.168)'[o2];\
     [o2][l3]overlay=15:12:enable='between(t,87.168,127.795)'[o3];\
     [o3][l4]overlay=15:12:enable='between(t,127.795,179.478)'[vout]" \
    -map '[vout]' -map '[aout]' -t "$TOTAL_DURATION" \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
    -c:a aac -b:a 128k -movflags +faststart \
    "$FINAL_VIDEO"
fi

capcut lint "$EDIT_DRAFT" --max-cue-secs 180 --max-chars 40
capcut info "$EDIT_DRAFT" -H
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=index,codec_type,codec_name,width,height \
  -of json "$FINAL_VIDEO"
