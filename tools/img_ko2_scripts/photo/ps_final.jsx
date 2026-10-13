app.displayDialogs = DialogModes.NO; app.preferences.rulerUnits = Units.PIXELS;
var D = "C:/Users/user/arg/omokage-kr/_adobe/photo/";
var A = (function(){ var f = new File($.fileName.replace(/\.jsx$/, ".args.txt")); f.open("r"); var t = f.read(); f.close(); return eval("(" + t + ")"); })();
var N = A.name, OUT = A.out, HB = (A.haloBlur == null ? 1.2 : A.haloBlur), HO = (A.haloOpacity || 90);
while (app.documents.length) app.documents[0].close(SaveOptions.DONOTSAVECHANGES);
var doc = app.open(new File(D + "erased_" + N + ".psd"));
function addPng(path, name) {
  var t = app.open(new File(path)); t.resizeImage(UnitValue(doc.width.value, "px"), UnitValue(doc.height.value, "px"), 72, ResampleMethod.BICUBICSHARPER);
  var L = t.activeLayer.duplicate(doc, ElementPlacement.PLACEATBEGINNING); t.close(SaveOptions.DONOTSAVECHANGES); app.activeDocument = doc;
  L = doc.layers[0]; L.name = name; return L;
}
if (A.halo !== false) { var h = addPng(D + "halo_" + N + ".png", "halo"); if (HB > 0) h.applyGaussianBlur(HB); h.opacity = HO; }
var T = addPng(D + "text_" + N + ".png", "text_ko");
if (A.soft) { for (var k = 0; k < A.soft.length; k++) { var q = A.soft[k]; doc.activeLayer = T;
  doc.selection.select([[q[0], q[1]], [q[2], q[1]], [q[2], q[3]], [q[0], q[3]]]);
  T.applyGaussianBlur(q[4]); T.applyAddNoise(q[5], NoiseDistribution.GAUSSIAN, true); doc.selection.deselect(); } }
if (A.textOpacity) T.opacity = A.textOpacity;
var so = new PhotoshopSaveOptions(); so.layers = true; doc.saveAs(new File(D + "final_" + N + ".psd"), so, true);
doc.saveAs(new File(OUT), new PNGSaveOptions(), true);
doc.close(SaveOptions.DONOTSAVECHANGES); "ok";
