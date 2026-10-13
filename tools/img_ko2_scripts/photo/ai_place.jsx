// items_<이름>.json 을 읽어 글자를 상자에 맞춰 놓고, 글자층·후광층을 따로 PNG 로 내보낸다.
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var D = "C:/Users/user/arg/omokage-kr/_adobe/photo/";
var A = (function(){ var f = new File($.fileName.replace(/\.jsx$/, ".args.txt")); f.open("r"); var t = f.read(); f.close(); return eval("(" + t + ")"); })();
var N = A.name;
var jf = new File(D + "items_" + N + ".json"); jf.encoding = "UTF-8"; jf.open("r"); var S = eval("(" + jf.read() + ")"); jf.close();
var doc = app.documents.add(DocumentColorSpace.RGB, S.w, S.h);
app.coordinateSystem = CoordinateSystem.ARTBOARDCOORDINATESYSTEM;
var ref = doc.layers[0]; ref.name = "reference";
var pl = ref.placedItems.add(); pl.file = new File(D + "erased_" + N + ".png"); pl.position = [0, 0]; pl.width = S.w; pl.height = S.h; ref.locked = true;
var halo = doc.layers.add(); halo.name = "halo";
var tl = doc.layers.add(); tl.name = "text_ko";
function rgb(c) { var k = new RGBColor(); k.red = c[0]; k.green = c[1]; k.blue = c[2]; return k; }
function vb(tf) { var d = tf.duplicate(); var o = d.createOutline(); var b = o.visibleBounds; o.remove(); return b; }
var rep = [];
for (var i = 0; i < S.items.length; i++) {
  var it = S.items[i], bx = it.box; // [x0,y0,x1,y1] px
  if (it.circle) { var c0 = it.circle; var el = tl.pathItems.ellipse(-(c0[1] - c0[2]), c0[0] - c0[2], c0[2] * 2, c0[2] * 2);
    el.filled = false; el.stroked = true; el.strokeColor = rgb(it.color); el.strokeWidth = it.sw || 2; rep.push("circle"); continue; }
  if (it.svg) { // 글꼴 윤곽선(SVG)을 넣는 경우
    var g = tl.groupItems.createFromFile(new File(D + it.svg));
    var gb = g.geometricBounds, gw = gb[2] - gb[0], gh = gb[1] - gb[3];
    var gs = Math.min((bx[2] - bx[0]) / gw, (bx[3] - bx[1]) / gh); g.resize(gs * 100, gs * 100);
    gb = g.geometricBounds;
    var gx = it.align == "center" ? ((bx[0] + bx[2]) / 2 - (gb[0] + gb[2]) / 2) : (bx[0] - gb[0]);
    g.translate(gx, (-((bx[1] + bx[3]) / 2)) - ((gb[1] + gb[3]) / 2));
    function paint(o, col, sw) { if (o.typename == "PathItem") { o.filled = true; o.fillColor = col; o.stroked = sw > 0; if (sw > 0) { o.strokeColor = col; o.strokeWidth = sw; o.strokeJoin = StrokeJoin.ROUNDENDJOIN; } }
      else if (o.typename == "CompoundPathItem") { for (var q = 0; q < o.pathItems.length; q++) paint(o.pathItems[q], col, sw); }
      else if (o.typename == "GroupItem") { for (var q2 = 0; q2 < o.pageItems.length; q2++) paint(o.pageItems[q2], col, sw); } }
    if (it.halo) { var hg = g.duplicate(halo, ElementPlacement.PLACEATBEGINNING); paint(hg, rgb(it.halo.color), (it.sw || 0) + it.halo.width); }
    paint(g, rgb(it.color), it.sw || 0); gb = g.geometricBounds; rep.push(it.svg + ":" + Math.round(gb[2] - gb[0]) + "x" + Math.round(gb[1] - gb[3])); continue;
  }
  var tf = tl.textFrames.add(); tf.contents = it.text;
  var ca = tf.textRange.characterAttributes; ca.textFont = app.textFonts.getByName(it.font); ca.size = it.pt || 100; ca.fillColor = rgb(it.color);
  ca.tracking = it.tracking || 0;
  if (it.sw) { ca.strokeColor = rgb(it.color); ca.strokeWeight = it.sw; }
  var b = vb(tf), w = b[2] - b[0], h = b[1] - b[3];
  var s = Math.min((bx[2] - bx[0]) / w, (bx[3] - bx[1]) / h);
  if (it.size) s = it.size / h; // 높이를 직접 정할 때
  if (!it.pt) tf.resize(s * 100, s * 100);
  if (it.sw) tf.textRange.characterAttributes.strokeWeight = it.sw; // 획은 크기와 따로
  b = vb(tf); w = b[2] - b[0]; h = b[1] - b[3];
  var tx = it.align == "center" ? ((bx[0] + bx[2]) / 2 - (b[0] + b[2]) / 2) : it.align == "right" ? (bx[2] - b[2]) : (bx[0] - b[0]);
  var ty = (-((bx[1] + bx[3]) / 2)) - ((b[1] + b[3]) / 2);
  tf.translate(tx, ty);
  if (it.rotate) tf.rotate(it.rotate, true, false, false, false, Transformation.CENTER);
  if (it.halo) {
    var hf = tf.duplicate(halo, ElementPlacement.PLACEATBEGINNING);
    var hc = hf.textRange.characterAttributes; hc.fillColor = rgb(it.halo.color); hc.strokeColor = rgb(it.halo.color); hc.strokeWeight = (it.sw || 0) + it.halo.width;
  }
  rep.push(it.text.substr(0, 6) + ":" + Math.round(w) + "x" + Math.round(h));
}
doc.saveAs(new File(D + "text_" + N + ".ai"));
var o = new ExportOptionsPNG24(); o.transparency = true; o.artBoardClipping = true; o.antiAliasing = true; o.horizontalScale = 400; o.verticalScale = 400;
ref.visible = false; halo.visible = false; doc.exportFile(new File(D + "text_" + N + ".png"), ExportType.PNG24, o);
halo.visible = true; tl.visible = false; doc.exportFile(new File(D + "halo_" + N + ".png"), ExportType.PNG24, o);
doc.close(SaveOptions.DONOTSAVECHANGES);
"ok " + rep.join(" | ");
