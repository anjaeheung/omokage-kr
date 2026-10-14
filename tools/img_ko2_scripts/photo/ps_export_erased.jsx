// erased_<이름>.psd 를 글자 없이 그대로 PNG 로 내보낸다(간판 글자를 아예 빼고 건물만 둘 때). args: {name, out}
app.displayDialogs = DialogModes.NO;
var D = "C:/Users/user/arg/omokage-kr/_adobe/photo/";
var A = (function(){ var f = new File($.fileName.replace(/\.jsx$/, ".args.txt")); f.open("r"); var t = f.read(); f.close(); return eval("(" + t + ")"); })();
while (app.documents.length) app.documents[0].close(SaveOptions.DONOTSAVECHANGES);
var doc = app.open(new File(D + "erased_" + A.name + ".psd"));
for (var i = 0; i < doc.layers.length; i++) doc.layers[i].visible = (doc.layers[i].name == "erased");
var so = new PhotoshopSaveOptions(); so.layers = true; doc.saveAs(new File(D + "final_" + A.name + "_notext.psd"), so, true);
doc.saveAs(new File(A.out), new PNGSaveOptions(), true);
doc.close(SaveOptions.DONOTSAVECHANGES); "ok";
