// erased_<이름>.psd 의 남은 원작 글자 찌꺼기를 타원 영역 내용 인식 칠로 지운다. args: {name, spots:[[cx,cy,r],...]}
app.displayDialogs = DialogModes.NO; app.preferences.rulerUnits = Units.PIXELS;
var D = "C:/Users/user/arg/omokage-kr/_adobe/photo/";
var A = (function(){ var f = new File($.fileName.replace(/\.jsx$/, ".args.txt")); f.open("r"); var t = f.read(); f.close(); return eval("(" + t + ")"); })();
var N = A.name;
while (app.documents.length) app.documents[0].close(SaveOptions.DONOTSAVECHANGES);
var doc = app.open(new File(D + "erased_" + N + ".psd"));
var L = null; for (var i = 0; i < doc.layers.length; i++) if (doc.layers[i].name == "erased") L = doc.layers[i];
doc.activeLayer = L;
for (var k = 0; k < A.spots.length; k++) {
  var s = A.spots[k], x0 = s[0] - s[2], y0 = s[1] - s[2], x1 = s[0] + s[2], y1 = s[1] + s[2];
  var d = new ActionDescriptor(), r = new ActionReference(); r.putProperty(charIDToTypeID("Chnl"), charIDToTypeID("fsel")); d.putReference(charIDToTypeID("null"), r);
  var e = new ActionDescriptor(); e.putUnitDouble(charIDToTypeID("Top "), charIDToTypeID("#Pxl"), y0); e.putUnitDouble(charIDToTypeID("Left"), charIDToTypeID("#Pxl"), x0);
  e.putUnitDouble(charIDToTypeID("Btom"), charIDToTypeID("#Pxl"), y1); e.putUnitDouble(charIDToTypeID("Rght"), charIDToTypeID("#Pxl"), x1);
  d.putObject(charIDToTypeID("T   "), charIDToTypeID("Elps"), e); executeAction(charIDToTypeID("setd"), d, DialogModes.NO);
  var f = new ActionDescriptor(); f.putEnumerated(charIDToTypeID("Usng"), charIDToTypeID("FlCn"), stringIDToTypeID("contentAware"));
  f.putUnitDouble(charIDToTypeID("Opct"), charIDToTypeID("#Prc"), 100); f.putEnumerated(charIDToTypeID("Md  "), charIDToTypeID("BlnM"), charIDToTypeID("Nrml"));
  executeAction(charIDToTypeID("Fl  "), f, DialogModes.NO); doc.selection.deselect();
}
var so = new PhotoshopSaveOptions(); so.layers = true; doc.saveAs(new File(D + "erased_" + N + ".psd"), so, true);
doc.saveAs(new File(D + "erased_" + N + ".png"), new PNGSaveOptions(), true);
doc.close(SaveOptions.DONOTSAVECHANGES); "ok";
