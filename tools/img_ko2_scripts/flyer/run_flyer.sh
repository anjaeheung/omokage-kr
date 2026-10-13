# 한 장 전체: 마스크 → PS 지우기 → 얼룩 고치기 → (AI 글자) → PS 합성
N=$1; FIX=$2; AI=${3:-yes}; RUN="python /c/Users/user/oshi100-translation/scripts/adobe/run.py"; J="C:/Users/user/arg/omokage-kr/_adobe/flyer"
python -I mk_mask.py $N
$RUN ps "$J/ps_erase.jsx" "{name:\"$N\"}" 2>&1 | grep -o "^ok\|RETRYLATER" | head -1
python -I mk_fix.py $N "$FIX" 120
$RUN ps "$J/ps_fix.jsx" "{name:\"$N\", blur:8}" 2>&1 | grep -o "^ok\|RETRYLATER" | head -1
[ "$AI" = yes ] && $RUN ai "$J/ai_place.jsx" "{name:\"$N\"}" 2>&1 | tail -1 | sed 's/[^ -~]//g'
$RUN ps "$J/ps_final.jsx" "{name:\"$N\", out:\"C:/Users/user/arg/omokage-kr/overrides/images/${N}kouen.png\"${EXTRA}}" 2>&1 | grep -o "^ok\|RETRYLATER" | head -1
python -I -c "
from PIL import Image
a=Image.open('src_$N.png').convert('RGB'); b=Image.open('../../overrides/images/${N}kouen.png').convert('RGB')
c=Image.new('RGB',(2128,1492),'white'); c.paste(a,(0,0)); c.paste(b,(1074,0)); c.save('../../tools/img_ko2/flyer/cmp_$N.png')"
