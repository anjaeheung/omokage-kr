app.displayDialogs = DialogModes.NO; app.preferences.rulerUnits = Units.PIXELS;
var D = "C:/Users/user/arg/omokage-kr/_adobe/logo/";
while (app.documents.length) app.documents[0].close(SaveOptions.DONOTSAVECHANGES);
var doc = app.open(new File(D + "src_logo.png"));
if (doc.mode != DocumentMode.RGB) doc.changeMode(ChangeMode.RGB);
doc.activeLayer.isBackgroundLayer = false; doc.activeLayer.name = "original";
var m = app.open(new File(D + "mask_logo_rgba.png"));
m.activeLayer.duplicate(doc, ElementPlacement.PLACEATBEGINNING); m.close(SaveOptions.DONOTSAVECHANGES);
app.activeDocument = doc;
var ml = doc.layers[0];
// 마스크 층의 불투명 부분을 선택 영역으로
var d = new ActionDescriptor(), r = new ActionReference(); r.putProperty(charIDToTypeID("Chnl"), charIDToTypeID("fsel"));
d.putReference(charIDToTypeID("null"), r); var r2 = new ActionReference(); r2.putEnumerated(charIDToTypeID("Chnl"), charIDToTypeID("Chnl"), charIDToTypeID("Trsp"));
d.putReference(charIDToTypeID("T   "), r2); executeAction(charIDToTypeID("setd"), d, DialogModes.NO);
ml.remove();
doc.activeLayer = doc.layers[0];
var f = new ActionDescriptor(); f.putEnumerated(charIDToTypeID("Usng"), charIDToTypeID("FlCn"), stringIDToTypeID("contentAware"));
f.putUnitDouble(charIDToTypeID("Opct"), charIDToTypeID("#Prc"), 100); f.putEnumerated(charIDToTypeID("Md  "), charIDToTypeID("BlnM"), charIDToTypeID("Nrml"));
executeAction(charIDToTypeID("Fl  "), f, DialogModes.NO); doc.selection.deselect();
// 왼쪽 밑줄을 마름모 중심(x=3196) 기준으로 좌우 뒤집어 오른쪽 밑줄을 다시 만든다
var C = 3196, L = 1325, R = 3110, T = 2845, B = 3160;
doc.selection.select([[L, T], [R, T], [R, B], [L, B]]); doc.selection.copy(); doc.selection.deselect();
var p = doc.paste(); p.name = "swash_right_mirrored";
p.resize(-100, 100, AnchorPosition.MIDDLECENTER);
var b = p.bounds; p.translate((2 * C - R) - b[0].value, T - b[1].value);
var so = new PhotoshopSaveOptions(); so.layers = true; doc.saveAs(new File(D + "erased_logo.psd"), so, true);
var po = new PNGSaveOptions(); doc.saveAs(new File(D + "erased_logo.png"), po, true);
doc.close(SaveOptions.DONOTSAVECHANGES);
"ok";
