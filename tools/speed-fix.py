from generate import run,ROOT
import json,re
c=(ROOT/'app.js').read_text();lines=c.splitlines();olds=[]
for i,l in enumerate(lines):
 if 'uiAcc = 0;' in l and i+1<len(lines) and 'if (g.over)' in lines[i+1]:olds.append(l+'\n'+lines[i+1])
p='''Son41numaralıtestfailed: g.over FALSE normal kayıt yüklemesinde speed4kalıyor. Cleanup sadeceif(g.over) İÇİNDE olmamalı. Aşağıdakiheroldtammetinde uiAcc=0; satırıile if(g.over){ arasına,ifdenÖNCE koşulsuz "onPointerCancel({pointerId:drag?.pointerId}); speed = 1; $('speedSelect').value = '1'; document.querySelector('.stage').classList.add('game-active');" satırını ekle. olddakiif(g.over) { satırıbraceDÂHİLkorunmalı. İçblokcleanup tekrarı kalsa sorun yok; normalelse de ilkcleanupçalışacak. YalnızJSON {"replacements":[{"old":"exact","new":"..."},...]} üret.\n'''+json.dumps(olds,ensure_ascii=False)
run('12-speed-reset','Verilen2satırbloğun arasına tekkoşulsuzsatır ekleyen JSONyama üret.',p,1024,False)
a=(ROOT/'benchmark/12-speed-reset/response.md').read_text().strip();a=re.sub(r'^```(?:json)?\s*|\s*```$','',a);o=json.loads(a)
for t in o['replacements']:
 assert t['old'] in olds and c.count(t['old'])==1
 c=c.replace(t['old'],t['new'],1)
(ROOT/'app.js').write_text(c);(ROOT/'benchmark/12-speed-reset/patch.json').write_text(json.dumps(o,ensure_ascii=False,indent=2))
