from generate import run,ROOT
import json,re
olds=["    g = s; sel = null; last = 0; uiAcc = 0;\n    if (g.over)","      g = s; sel = null; last = 0; uiAcc = 0;\n      if (g.over)","  const rw = g.runways.find(r => r.accepts.includes(p.type) && !r.closed);"]
p='''43kontrol41geçti. İkigerçekhata: loadhız4kalmış; busy pistyaklaşmarotası çiziliyor. JSON{"replacements":[{"old":exact,"new":replacement},...]} sadece3yama üret. İlk2load/importsatırında onPointerCancel({pointerId:drag?.pointerId}) çağır,speed=1,$('speedSelect').value='1',stage.game-activeclassadd;diğerstatekoru. Sonpistseçiminde busy<=0 şartıekle, sadeceuygunboşpistbulunsun. Özgün3old aşağıdaJSONliste; oldlarbytebyteaynıolsun. Yalnız3JSONyama, açıklamayok.\n'''+json.dumps(olds,ensure_ascii=False)
run('09-final-patch','Kesin metin değişiklikleri JSONüret.',p,2048,False)
a=(ROOT/'benchmark/09-final-patch/response.md').read_text().strip();a=re.sub(r'^```(?:json)?\s*|\s*```$','',a);obj=json.loads(a);code=(ROOT/'app.js').read_text()
for t in obj['replacements']:
 assert t['old'] in olds and code.count(t['old'])==1
 code=code.replace(t['old'],t['new'],1)
(ROOT/'app.js').write_text(code);(ROOT/'benchmark/09-final-patch/patch.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2))
