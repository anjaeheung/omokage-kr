app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var D = "C:/Users/user/arg/omokage-kr/_adobe/logo/";
var W = 6400, H = 4267;
var doc = app.documents.add(DocumentColorSpace.RGB, W, H);
app.coordinateSystem = CoordinateSystem.ARTBOARDCOORDINATESYSTEM;
var ref = doc.layers[0]; ref.name = "reference";
var pl = ref.placedItems.add(); pl.file = new File(D + "erased_logo.png");
pl.position = [0, 0]; pl.width = W; pl.height = H; ref.locked = true;
var tl = doc.layers.add(); tl.name = "text_ko";
var red = new RGBColor(); red.red = 130; red.green = 5; red.blue = 6;
function place(str, font, box) {
  var tf = tl.textFrames.add(); tf.contents = str;
  var ca = tf.textRange.characterAttributes; ca.textFont = app.textFonts.getByName(font); ca.size = 1000; ca.fillColor = red; ca.tracking = 0; ca.strokeColor = red; ca.strokeWeight = box.sw;
  function vb() { var d = tf.duplicate(); var o = d.createOutline(); var b = o.visibleBounds; o.remove(); return b; } // [l,t,r,b], t>b
  var b = vb(), w = b[2] - b[0], h = b[1] - b[3];
  var s = Math.min(box.w / w, box.h / h);
  tf.resize(s * 100, s * 100);
  b = vb(); w = b[2] - b[0]; h = b[1] - b[3];
  var cx = (b[0] + b[2]) / 2, top = b[1];
  tf.translate(box.cx - cx, (-box.top) - top);
  return [Math.round(w), Math.round(h)];
}
var r1 = place("\uADF9\uB2E8", "NotoSerifKR-Heavy", { cx: 3196, top: 790, w: 2000, h: 800, sw: 22 });
var r2 = place("\uC624\uBAA8\uCE74\uAC8C", "NotoSerifKR-Heavy", { cx: 3196, top: 1660, w: 4880, h: 1130, sw: 30 });
doc.saveAs(new File(D + "text_logo.ai"));
ref.visible = false;
var o = new ExportOptionsPNG24(); o.transparency = true; o.artBoardClipping = true; o.antiAliasing = true; o.horizontalScale = 100; o.verticalScale = 100;
doc.exportFile(new File(D + "text_logo.png"), ExportType.PNG24, o);
doc.close(SaveOptions.DONOTSAVECHANGES);
"ok " + r1 + " / " + r2;
