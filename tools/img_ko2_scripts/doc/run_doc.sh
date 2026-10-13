# 서류 한 장: 마스크 → PS 지우기 → 얼룩 → AI 글자 → PS 합성. N=이름, FIX=얼룩 조건, AI=yes|no, EXTRA=ps_final 추가 인자
N=$1; FIX=$2; AI=${3:-yes}; RUN="python /c/Users/user/oshi100-translation/scripts/adobe/run.py"; J="C:/Users/user/arg/omokage-kr/_adobe/doc"
OUT="C:/Users/user/arg/omokage-kr/overrides/records/images/${N}.png"
python -I mk_mask.py $N
$RUN ps "$J/ps_erase.jsx" "{name:\"$N\"}" 2>&1 | grep -o "^ok\|RETRYLATER" | head -1
FX=$(python -I mk_fix.py $N "$FIX" 60); echo "$FX"
case "$FX" in *"fix px 0 "*) ;; *) $RUN ps "$J/ps_fix.jsx" "{name:\"$N\", blur:6}" 2>&1 | grep -o "^ok\|RETRYLATER" | head -1;; esac
[ "$AI" = yes ] && $RUN ai "$J/ai_place.jsx" "{name:\"$N\"}" 2>&1 | tail -1 | sed 's/[^ -~]//g' | cut -c1-200
$RUN ps "$J/ps_final.jsx" "{name:\"$N\", out:\"$OUT\", halo:false${EXTRA}}" 2>&1 | grep -o "^ok\|RETRYLATER" | head -1
python -I -c "
from PIL import Image
a=Image.open('src_$N.png').convert('RGB'); b=Image.open(r'$OUT').convert('RGB')
c=Image.new('RGB',(a.width*2+20,a.height),'white'); c.paste(a,(0,0)); c.paste(b,(a.width+20,0)); c.save('../../tools/img_ko2/doc/cmp_$N.png')"
