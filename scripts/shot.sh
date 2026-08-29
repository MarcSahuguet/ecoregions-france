#!/bin/bash
# shot.sh <décalage vertical> <largeur> <hauteur> <sortie> [thème light|dark] [action JS]
set -e
off=$1; w=$2; h=$3; out=$4; theme=${5:-}; act=${6:-}
dir=$(dirname "$out")
cat > "$dir/_frame.html" <<EOF
<meta charset="utf-8">
<style>html,body{margin:0;background:#888;overflow:hidden}
 .v{width:${w}px;height:${h}px;overflow:hidden;position:relative}
 iframe{position:absolute;top:-${off}px;left:0;width:${w}px;height:11000px;border:0}</style>
<div class="v"><iframe id="f" src="file:///Users/marc/franceregions/site/index.html"></iframe></div>
<script>
const f=document.getElementById('f');
f.onload=()=>{ const d=f.contentDocument, W=f.contentWindow;
  if ("$theme") d.documentElement.dataset.theme="$theme";
  try{ $act }catch(e){ console.log('ACT ERR',e.message) } };
</script>
EOF
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --allow-file-access-from-files --hide-scrollbars --force-device-scale-factor=1.5 \
  --window-size="$w","$h" --virtual-time-budget=9000 --screenshot="$out" \
  "file://$dir/_frame.html" 2>/dev/null
echo "$out"
