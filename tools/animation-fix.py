from generate import run,ROOT
import json,re
c=(ROOT/'app.js').read_text();old=c[c.index('    if (uiAcc >= 0.25)'):c.index('\n  }\n  render();',c.index('    if (uiAcc >= 0.25)'))]
p='''Yeni tarayıcıtesti yakaladı:loop herframehızı1e döndürüpdragıtemizliyor. Bu benim önceki promptta yanlışbloğu da yamaya dahil etmemden kaynaklandı;cleanupyükleme/importlarda kalacak. Yalnızaşağıdaki loopblocundaki onPointerCancel+speed1+classadd SATIRINI kaldır. UIrateupdate ve if(g.over) oynatsonuç korunacak. TekJSON{"old":"exactblock","new":"blockwithoutonlythatline"}; başkaedit yok.\n'''+old
run('13-animation-fix','Tek kesin JSONold/newyama üret.',p,1024,False)
a=(ROOT/'benchmark/13-animation-fix/response.md').read_text().strip();a=re.sub(r'^```(?:json)?\s*|\s*```$','',a);o=json.loads(a);assert o['old']==old and c.count(old)==1;c=c.replace(old,o['new'],1);(ROOT/'app.js').write_text(c);(ROOT/'benchmark/13-animation-fix/patch.json').write_text(json.dumps(o,ensure_ascii=False,indent=2))
