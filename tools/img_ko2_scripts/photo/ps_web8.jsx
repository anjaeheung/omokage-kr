app.displayDialogs = DialogModes.NO;
var A = (function(){ var f = new File($.fileName.replace(/\.jsx$/, ".args.txt")); f.open("r"); var t = f.read(); f.close(); return eval("(" + t + ")"); })();
while (app.documents.length) app.documents[0].close(SaveOptions.DONOTSAVECHANGES);
var out = [];
for (var i = 0; i < A.files.length; i++) {
  var f = new File(A.files[i]); var d = app.open(f);
  var w = new ExportOptionsSaveForWeb(); w.format = SaveDocumentType.PNG; w.PNG8 = true; w.colors = 256;
  w.colorReduction = ColorReductionType.SELECTIVE; w.dither = Dither.DIFFUSION; w.ditherAmount = A.dither || 60; w.transparency = false;
  d.exportDocument(f, ExportType.SAVEFORWEB, w); d.close(SaveOptions.DONOTSAVECHANGES); out.push(f.name);
}
out.join(",");
