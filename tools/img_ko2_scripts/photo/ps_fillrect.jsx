app.displayDialogs = DialogModes.NO; app.preferences.rulerUnits = Units.PIXELS;
var D = "C:/Users/user/arg/omokage-kr/_adobe/photo/";
var A = (function(){ var f = new File($.fileName.replace(/\.jsx$/, ".args.txt")); f.open("r"); var t = f.read(); f.close(); return eval("(" + t + ")"); })();
while (app.documents.length) app.documents[0].close(SaveOptions.DONOTSAVECHANGES);
var doc = app.open(new File(D + "erased_" + A.name + ".psd"));
var L = null; for (var i = 0; i < doc.layers.length; i++) if (doc.layers[i].name == "erased") L = doc.layers[i];
doc.activeLayer = L;
for (var k = 0; k < A.rects.length; k++) { var q = A.rects[k];
  doc.selection.select([[q[0], q[1]], [q[2], q[1]], [q[2], q[3]], [q[0], q[3]]]); doc.selection.feather(1);
  var c = new SolidColor(); c.rgb.red = q[4]; c.rgb.green = q[5]; c.rgb.blue = q[6]; doc.selection.fill(c);
  L.applyAddNoise(A.noise || 2, NoiseDistribution.GAUSSIAN, true); L.applyGaussianBlur(0.6); }
doc.selection.deselect();
var so = new PhotoshopSaveOptions(); so.layers = true; doc.saveAs(new File(D + "erased_" + A.name + ".psd"), so, true);
doc.saveAs(new File(D + "erased_" + A.name + ".png"), new PNGSaveOptions(), true);
doc.close(SaveOptions.DONOTSAVECHANGES); "ok";
