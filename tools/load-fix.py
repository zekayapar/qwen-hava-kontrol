from generate import run,ROOT
import json,re
c=(ROOT/'app.js').read_text();a=c[c.index('function doLoad()'):c.index('function doExport()')];b=c[c.index('function onFile(e)'):c.index('function togglePause()')]
p='''Önceki kesin metin yamalarında parantez sınırı belirsizliği sözdizimini bozdu; uygulama eşleştirmesi de başarısız. ArtıkikifonksiyonunTAMAMINI üret. JSON{"doLoad":"tam function doLoad() {...}","onFile":"tam function onFile(e) {...}"}. Aynıg,sel,last,uiAcc,playing,speed ve yardımcıları kullan. g=s valid deserialize sonrası koşuldanÖNCE onPointerCancel({pointerId:drag?.pointerId}); speed=1;$('speedSelect').value='1';document.querySelector('.stage').classList.add('game-active');sel=null;last=0;uiAcc=0. g.overyseplayingfalse,endOverlayhiddenfalse,showEnd. Aksi g.pausedtrue,playingtrue,startoverlayhidden,endoverlayhidden,setErr. onFile size100KB,rdonerror,invalidverimevcutoyunudeğiştirme. globalstage değişkenYOK. Sözdizimi tam validJS. JSONyalnız. Eski bozukfonksiyonlar:\n'''+a+'\n'+b
run('11-load-functions','Tam JavaScriptfonksiyonları JSONstring alanlarında üret.',p,2048,False)
a=(ROOT/'benchmark/11-load-functions/response.md').read_text().strip();a=re.sub(r'^```(?:json)?\s*|\s*```$','',a);o=json.loads(a)
for name,nextname in [('doLoad','doExport'),('onFile','togglePause')]:
 start=c.index('function '+name+'(');end=c.index('function '+nextname+'(',start);assert o[name].startswith('function '+name+'(');c=c[:start]+o[name]+'\n'+c[end:]
(ROOT/'app.js').write_text(c);(ROOT/'benchmark/11-load-functions/patch.json').write_text(json.dumps(o,ensure_ascii=False,indent=2))
