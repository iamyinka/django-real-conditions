#!/usr/bin/env bash
# Two-pass EBU R128 loudness normalization, then automated signal checks.
# Target: -16 LUFS integrated, -1.5 dBTP true peak (the pilot's approved standard).
# Usage: bash tools/course/produce/normalize_and_check.sh course/modules/M00/M00.01
set -euo pipefail
d="$1/render"
in="$d/narration_raw.wav"

# Pass 1: measure.
m=$(ffmpeg -hide_banner -nostats -i "$in" -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$m" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
# Pass 2: apply the measured values (linear mode), resample to 48 kHz.
ffmpeg -hide_banner -loglevel error -y -i "$in" -af \
  "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true" \
  -ar 48000 "$d/narration.wav"

{
  echo "duration_s: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$d/narration.wav")"
  ffmpeg -hide_banner -nostats -i "$d/narration.wav" -af ebur128=peak=true -f null - 2>&1 \
    | sed -n '/Summary:/,$p' | grep -E "I:|LRA:|Peak:" | sed 's/^ */ebur128 /'
  echo "clipped_samples (|x|>=0.999): $(ffmpeg -hide_banner -loglevel error -i "$d/narration.wav" -f f32le -ac 1 - \
    | python3 -I -c 'import sys,array; a=array.array("f"); a.frombytes(sys.stdin.buffer.read()); print(sum(1 for x in a if abs(x)>=0.999))')"
  echo "silences >= 1.5s (scene gaps are 0.9s; lead-out is 1.5s):"
  ffmpeg -hide_banner -nostats -i "$d/narration.wav" -af silencedetect=noise=-45dB:d=1.5 -f null - 2>&1 \
    | grep -E "silence_(start|end)" | sed 's/^.*\] /  /'
} > "$d/checks.txt"
cat "$d/checks.txt"
