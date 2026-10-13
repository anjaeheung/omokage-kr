app.displayDialogs = DialogModes.NO; app.preferences.rulerUnits = Units.PIXELS;
var D = "C:/Users/user/arg/omokage-kr/_adobe/doc/";
var A = (function(){ var f = new File($.fileName.replace(/\.jsx$/, ".args.txt")); f.open("r"); var t = f.read(); f.close(); return eval("(" + t + ")"); })();
while (app.documents.length) app.documents[0].close(SaveOptions.DONOTSAVECHANGES);
var doc = app.open(new File(D + "erased_" + A.name + ".psd"));
var L = null; for (var i = 0; i < doc.layers.length; i++) if (doc.layers[i].name == "erased") L = doc.layers[i];
doc.activeLayer = L;
for (var k = 0; k < A.boxes.length; k++) {
  var b = A.boxes[k]; doc.selection.select([[b[0], b[1]], [b[2], b[1]], [b[2], b[3]], [b[0], b[3]]]);
  doc.selection.feather(4);
  for (var j = 0; j < 3; j++) L.applyGaussianBlur(A.blur || 14);
  L.applyAddNoise(A.noise || 1.5, NoiseDistribution.GAUSSIAN, true);
}
doc.selection.deselect();
var so = new PhotoshopSaveOptions(); so.layers = true; doc.saveAs(new File(D + "erased_" + A.name + ".psd"), so, true);
doc.saveAs(new File(D + "erased_" + A.name + ".png"), new PNGSaveOptions(), true);
doc.close(SaveOptions.DONOTSAVECHANGES); "ok";
