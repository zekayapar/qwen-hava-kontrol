from generate import run,ROOT
import json,re
code=(ROOT/'app.js').read_text();olds=[l for l in code.splitlines() if 'if (g.over) { onPointerCancel' in l]
p='''Son yaman sözdizimini bozdu: old if(g.over) satırında açılansüslüparantezyoktu fakat new içine ekledin ve aşağıdaki mevcut { kaldı; if..else bozuldu. stage tanımlıdeğil.document.querySelector('.stage') kullan. Aşağıdaki2tamline içinJSONreplacements üret. Newsatır: onPointerCancel({pointerId:drag?.pointerId}); speed=1; $('speedSelect').value='1'; document.querySelector('.stage').classList.add('game-active'); sonra YENİSATIR aynıindent if (g.over) ifadesi, süslüparantezsiz; mevcut sonraki { olduğu gibi kalır. Cleanup koşuldanönceherload çalışmalı. YalnızJSON{"replacements":[{"old":"exactline","new":"..."},...]}.\n'''+json.dumps(olds,ensure_ascii=False)
run('10-syntax-fix','YalnızJSON metin yamaları üret, ifadelerdengeçerliJSyap.',p,1024,False)
a=(ROOT/'benchmark/10-syntax-fix/response.md').read_text().strip();a=re.sub(r'^```(?:json)?\s*|\s*```$','',a);o=json.loads(a)
for t in o['replacements']:
 assert t['old'] in olds and code.count(t['old'])==1
 code=code.replace(t['old'],t['new'],1)
(ROOT/'app.js').write_text(code);(ROOT/'benchmark/10-syntax-fix/patch.json').write_text(json.dumps(o,ensure_ascii=False,indent=2))
