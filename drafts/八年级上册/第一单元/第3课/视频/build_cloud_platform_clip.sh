#!/usr/bin/env bash
set -euo pipefail

SOURCE_VIDEO="/Users/zengweihao/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_szw624gslah521_1f3c/msg/video/2026-09/870dca908919ae1518b3cc4f9cfaea7e_raw.mp4"
BASE_DIR="/Users/zengweihao/Desktop/信息技术/out/video_cloud_platform_analysis"
DRAFTS_DIR="$BASE_DIR/drafts"
SOURCE_DRAFT="$DRAFTS_DIR/cloud-platform-source"
EDIT_DRAFT="$BASE_DIR/物联网云平台四功能_可编辑草稿"
FINAL_VIDEO="$BASE_DIR/物联网云平台四功能_课堂片段_2分59秒.mp4"
LABEL_DIR="$BASE_DIR/labels"
START="196.845"
END="376.323"
DURATION="179.478"

if [[ ! -f "$SOURCE_VIDEO" ]]; then
  echo "Source video not found: $SOURCE_VIDEO" >&2
  exit 1
fi

mkdir -p "$DRAFTS_DIR" "$LABEL_DIR"

if [[ ! -e "$SOURCE_DRAFT" ]]; then
  capcut quickstart cloud-platform-source \
    --video "$SOURCE_VIDEO" \
    --drafts "$DRAFTS_DIR" \
    --width 480 \
    --height 270
fi

if [[ ! -e "$EDIT_DRAFT" ]]; then
  capcut cut "$SOURCE_DRAFT" "$START" "$END" --out "$EDIT_DRAFT"

  capcut add-text "$EDIT_DRAFT" 0 44.798 \
    "01 设备互联｜传感器、农机接入平台" \
    --font-size 18 --color '#FFFFFF' --align 0 --x -0.72 --y -0.78 --track-name "功能提示"

  capcut add-text "$EDIT_DRAFT" 44.798 22.370 \
    "02 数据汇聚｜分散数据集中存储" \
    --font-size 18 --color '#FFFFFF' --align 0 --x -0.72 --y -0.78 --track-name "功能提示"

  capcut add-text "$EDIT_DRAFT" 67.168 40.627 \
    "03 查看与分析｜发现变化和异常" \
    --font-size 18 --color '#FFFFFF' --align 0 --x -0.72 --y -0.78 --track-name "功能提示"

  capcut add-text "$EDIT_DRAFT" 107.795 71.683 \
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
  -annotate +12+0 '02 数据汇聚｜分散数据集中存储' "$LABEL_DIR/02.png"
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
    -ss "$START" -i "$SOURCE_VIDEO" \
    -loop 1 -i "$LABEL_DIR/01.png" \
    -loop 1 -i "$LABEL_DIR/02.png" \
    -loop 1 -i "$LABEL_DIR/03.png" \
    -loop 1 -i "$LABEL_DIR/04.png" \
    -filter_complex \
    "[0:v]setpts=PTS-STARTPTS[base];\
     [1:v]format=rgba[l1];[2:v]format=rgba[l2];[3:v]format=rgba[l3];[4:v]format=rgba[l4];\
     [base][l1]overlay=15:12:enable='between(t,0,44.798)'[v1];\
     [v1][l2]overlay=15:12:enable='between(t,44.798,67.168)'[v2];\
     [v2][l3]overlay=15:12:enable='between(t,67.168,107.795)'[v3];\
     [v3][l4]overlay=15:12:enable='between(t,107.795,179.478)'[vout]" \
    -map '[vout]' -map '0:a?' -t "$DURATION" \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
    -c:a aac -b:a 128k -movflags +faststart \
    "$FINAL_VIDEO"
fi

capcut lint "$EDIT_DRAFT" --no-check-paths --max-cue-secs 180 --max-chars 40
capcut info "$EDIT_DRAFT" -H
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=index,codec_type,codec_name,width,height \
  -of json "$FINAL_VIDEO"
