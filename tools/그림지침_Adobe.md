# 그림 한국어화 — Photoshop·Illustrator 로 다시 하기

콘테 요청(2026-10-05): 「이미지 번역은 일러스트레이터와 포토샵을 이용해서 작업해줘」.
1차 결과(파이썬만으로 만든 것)는 `tools/img_ko/<묶음>/out/` 에 있다 — **번역문·배치·글꼴 선택은 그대로 참고/재사용**하고
(각 묶음의 `번역표.md`, `tools/img_ko_scripts/<묶음>/make.py` 에 좌표·크기·지울 영역이 다 있다),
**지우기는 Photoshop, 글자는 Illustrator** 로 다시 만든다. `tools/그림지침.md` 의 규칙(빠짐없이·같은 결·이질감 없게·줄바꿈 등)은 그대로.

## Adobe 다루는 법
- 실행: `python tools/adobe/run.py ps <jsx>` / `python tools/adobe/run.py ai <jsx> [인자]` (작업 폴더 C:\Users\user\arg\nameisasleep-kr 에서).
  run.py 가 잠금(_adobe/adobe.lock)으로 한 번에 하나만 Adobe 를 쓰게 한다 — **다른 에이전트도 동시에 쓰고 있으니 반드시 run.py 로만 부를 것.**
  jsx 하나는 짧게(몇 장 단위) 끊어서, 잠금을 오래 잡지 말 것. 앱을 종료(app.quit)하지 말 것. 연 문서는 jsx 안에서 꼭 닫을 것.
- **경로는 ASCII 만.** 작업 파일은 `C:/Users/user/arg/nameisasleep-kr/_adobe/<묶음>/` 에(영문 파일명). jsx 도 거기에.
- Illustrator 에 보이는 한글 글꼴(PostScript 이름): HiMelody-Regular, GowunDodum-Regular, PoorStory-Regular, Gaegu-Regular/Bold,
  GamjaFlower-Regular, Jua-Regular, NanumPen-Regular, NanumBrush, NanumMyeongjoBold/ExtraBold, GowunBatang-Bold,
  NotoSansKR-Thin/Light/DemiLight/Regular/Medium/Bold/Black, NotoSerifKR-ExtraLight/Light/Regular/Medium/SemiBold/Bold/Heavy,
  MalgunGothic/MalgunGothicBold, Batang. (`app.textFonts.getByName("...")`)
- 예전 작품의 jsx 참고: `C:/Users/user/arg/yumifuri-kr/tools/adobe_scripts/` (ps_erase.jsx = 마스크→내용 인식 칠, ai_sign.jsx·ai_sketch.jsx·ai_magazine.jsx = 글자 배치·PNG 내보내기).
  Illustrator 팁: app.userInteractionLevel = DONTDISPLAYALERTS, 대지 = 그림 px 와 같은 pt, coordinateSystem = ARTBOARDCOORDINATESYSTEM(위가 0, y 는 음수로), 
  PNG 내보내기 ExportOptionsPNG24(transparency, horizontalScale/verticalScale 400, antiAliasing) → 파이썬/PS 에서 1/4 로 줄이면 획이 곱다.
  Photoshop 내용 인식: ps_erase.jsx 의 executeAction("Fl  ", contentAware) 방식.

## 흐름 (그림마다)
1. 파이썬: 원본 → `_adobe/<묶음>/src_<이름>.png`, 지울 곳 마스크 `mask_<이름>.png`(흰색=지움, 글자보다 1~3px 넉넉히).
2. **Photoshop**: 마스크 영역을 내용 인식 칠 → `erased_<이름>.png` + `.psd`.
   괘선·줄무늬·단색 UI 처럼 내용 인식이 망치기 쉬운 곳은 PS 안에서 다른 방법(복제 도장·패치·영역 나눠 여러 번 칠하기, 단색이면 그 색으로 칠)을 써도 된다.
   PS 결과가 원본 결을 깨는 좁은 곳에 한해 1차 파이썬 지우기를 섞어도 되지만, 기본은 PS. 어떻게 했는지 보고에 적는다.
3. **Illustrator**: 그림 크기 대지에 지운 바탕을 잠근 참고층으로 깔고, 한국어 글자를 문자 객체로 배치(글꼴·크기·자간·행간·색을 원본에 맞춤, 기울기·세로쓰기 등도 Illustrator 기능으로).
   편집용 `.ai` 저장(문자 살아 있게), 글자층만 투명 PNG 400% 로 내보내기.
4. **Photoshop**: 지운 바탕 위에 글자 PNG 를 층으로 얹어(1/4 크기, 종이 위 잉크면 곱하기 등 원본 같은 합성), 층이 살아 있는 `final_<이름>.psd` 와
   완성 PNG 저장. 완성 PNG 는 원본과 같은 크기·모드(RGBA 면 알파 그대로).
5. 완성 PNG → `tools/img_ko2/<묶음>/out/<원본 파일명>.png`, 비교 그림 `tools/img_ko2/<묶음>/cmp_<이름>.png`(원본|새 판).
   jsx·py 는 `tools/img_ko2_scripts/<묶음>/` 에도 복사(다시 만들 수 있게). .ai/.psd 는 _adobe 에 둔다(커밋 안 함).
6. Read 로 비교 그림을 확대해 보며 최소 2회 고친다. 1차 판보다 나빠지면 안 된다.

## 보고
한국어로: 만든 그림, Photoshop·Illustrator 를 각각 어디에 썼는지, 남은 아쉬운 점(정직하게).
