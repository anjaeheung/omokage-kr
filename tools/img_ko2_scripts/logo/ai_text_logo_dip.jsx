app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var D = "C:/Users/user/arg/omokage-kr/_adobe/logo/";
var A = (function(){ var f = new File($.fileName.replace(/\.jsx$/, ".args.txt")); f.open("r"); var t = f.read(); f.close(); return t ? eval("(" + t + ")") : {}; })();
var SW1 = A.sw1 || 18, SW2 = A.sw2 || 26;
var W = 6400, H = 4267;
var doc = app.documents.add(DocumentColorSpace.RGB, W, H);
app.coordinateSystem = CoordinateSystem.ARTBOARDCOORDINATESYSTEM;
var ref = doc.layers[0]; ref.name = "reference";
var pl = ref.placedItems.add(); pl.file = new File(D + "erased_logo.png"); pl.position = [0, 0]; pl.width = W; pl.height = H; ref.locked = true;
var tl = doc.layers.add(); tl.name = "text_ko (Diphylleia outlines)";
var red = new RGBColor(); red.red = 130; red.green = 5; red.blue = 6;
function paint(it, sw) {
  if (it.typename == "PathItem") { it.filled = true; it.fillColor = red; it.stroked = sw > 0; if (sw > 0) { it.strokeColor = red; it.strokeWidth = sw; it.strokeJoin = StrokeJoin.ROUNDENDJOIN; it.strokeCap = StrokeCap.ROUNDENDCAP; } }
  else if (it.typename == "CompoundPathItem") { for (var i = 0; i < it.pathItems.length; i++) paint(it.pathItems[i], sw); }
  else if (it.typename == "GroupItem") { for (var j = 0; j < it.pageItems.length; j++) paint(it.pageItems[j], sw); }
}
function place(svg, box, sw) {
  var g = tl.groupItems.createFromFile(new File(D + svg));
  var b = g.geometricBounds, w = b[2] - b[0], h = b[1] - b[3];
  var s = Math.min(box.w / w, box.h / h); g.resize(s * 100, s * 100);
  b = g.geometricBounds; g.translate(box.cx - (b[0] + b[2]) / 2, (-box.top) - b[1]);
  paint(g, sw); b = g.geometricBounds; return [Math.round(b[2] - b[0]), Math.round(b[1] - b[3])];
}
var r1 = place("dip_geukdan.svg", { cx: 3196, top: 800, w: 1900, h: 780 }, SW1);
var r2 = place("dip_omokage.svg", { cx: 3196, top: 1660, w: 4800, h: 1120 }, SW2);
doc.saveAs(new File(D + "text_logo_dip.ai"));
ref.visible = false;
var o = new ExportOptionsPNG24(); o.transparency = true; o.artBoardClipping = true; o.antiAliasing = true; o.horizontalScale = 100; o.verticalScale = 100;
doc.exportFile(new File(D + "text_logo.png"), ExportType.PNG24, o);
doc.close(SaveOptions.DONOTSAVECHANGES);
"ok " + r1 + " / " + r2;
