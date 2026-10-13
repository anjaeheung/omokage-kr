N=$1; FIX=$2; AI=${3:-yes}; RUN="python /c/Users/user/oshi100-translation/scripts/adobe/run.py"; J="C:/Users/user/arg/omokage-kr/_adobe/photo"
OUT="C:/Users/user/arg/omokage-kr/overrides/records/images/${N}.png"; [ -n "$OUTP" ] && OUT="$OUTP"
python -I mk_mask.py $N
$RUN ps "$J/ps_erase.jsx" "{name:\"$N\"}" 2>&1 | grep -o "^ok\|RETRYLATER" | head -1
if [ -n "$FIX" ]; then FX=$(python -I mk_fix.py $N "$FIX" 40); echo "$FX"; case "$FX" in *"fix px 0 "*) ;; *) $RUN ps "$J/ps_fix.jsx" "{name:\"$N\", blur:4}" 2>&1 | grep -o "^ok\|RETRYLATER" | head -1;; esac; fi
[ "$AI" = yes ] && $RUN ai "$J/ai_place.jsx" "{name:\"$N\"}" 2>&1 | tail -1 | sed 's/[^ -~]//g' | cut -c1-160
$RUN ps "$J/ps_final.jsx" "{name:\"$N\", out:\"$OUT\", halo:false${EXTRA}}" 2>&1 | grep -o "^ok\|RETRYLATER" | head -1
