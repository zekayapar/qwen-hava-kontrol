from generate import run,ROOT
import json,re
files={f:(ROOT/f).read_text() for f in ['app.js','index.html','engine.js']}
p='''Kod incelemesi ve ilkChrome kontrolü sonrası düzeltmeler. YalnızJSON {"replacements":[{"file":"app.js|index.html|engine.js","old":"exact unique old text","new":"replacement"},...]} döndür. Heroldmevcutkodda yalnız1kere olsun. Tamdosya üretme; noMarkdown. Bütün aşağıdaki sorunları düzelt:
1 startGame g.paused=true yeniBaşlaoyunuduraklatıyor; buradafalse (init/loadtruekalsın). Restart/Load/Import dragcleanup ve hız1/resetselector; loadgame.over iseendoverlay gösterilsin,playing=false.
2 render ctx.setTransform(DPR...)CSSboyuta görecanvaswidth/1000,height/700scale yerineDPRkullanmış,mobil/gendüzayarsız; doğruölçekleclearRect1000×700.
3 tüm r.busySeconds yanlış alanı r.busy. fuel değerisaniye, yüzdeişareti yerine sn. windbirimi enginebelirtilmemişdereceolmamalı, metin "Rüzgar etkisi: N". Guncelplane yokselnull, yaklaşma/clearbuttons g.over veya!playing durumdisabled.
4 onKey e.repeatignore; EnterBUTTONtargetnativeişleminekarışma. P/R buttonda nonEnterkısayolkalabilir; overgamepause/toggle olmaz.
5 pointerdown drag.pointerId sakla; cancelblur/visibilitychangeg.paused set edilirkendragcapturecleanup; pointercancel eolsunolmasındrag.pointerIdrelease. onpointermovebasılıdrawingaktifama100limitnoktafiltrearraydolanörnek4pxminimum yeterli.
6 Uçak list li rolebutton/tabIndex0/aria label tanımla,keyEnter/Spaceevent selectPlane sadece; globalEnter buttonve rolebutton elementten approachçiftolmayacak şekilde guard. 
7 yaklaşhelperbusy açıkpiststatei seçsin eğeruygunfreeyok görünürerror ve route değiştirmesin. İlkpointmerkez-60...sonrası180 degerrotaengineuygun.
8 index viewportmaximumscale/user-scalableno kaldır. Mobil başlangıçoverlayradarheight küçük clip; yalnızstartoverlaygörünürkenstage minheight360 CSS, oyunbaşladıktan minheightkalksın. Yönerge "uyarılar kırmızı olmadan" ayrım35warning12collisionaslıvar uygunTürkçenet. Türlejant şuanda Normal/Yakın/Tehlikeamaeksikhafif/orta/ağır; bunuTür renkleriyledeğiştir.
9 engineweatherstormTimer sıfırıaltınainincefalse yapıyorsun ama negatifstormTimer kalıyor;stormbitti bloğunastormTimer=0ekle,validserialize/deserializetutarlı.
Kodlar:\n'''+'\nFILE app.js\n'+files['app.js']+'\nFILE index.html\n'+files['index.html']+'\nFILE engine.js relevant snippet\n'+files['engine.js'][files['engine.js'].index('} else if (g.weather.storm)'):files['engine.js'].index('// Runway timers')]
run('08-integration-fixes','JSON metin yaması üret. Her old tam mevcut dosya metni olmalı ve unique. SadeceJSON, açıklamasız.',p,6144,False)
a=(ROOT/'benchmark/08-integration-fixes/response.md').read_text().strip();a=re.sub(r'^```(?:json)?\s*|\s*```$','',a);obj=json.loads(a)
for patch in obj['replacements']:
 f=patch['file'];assert f in files
 old=patch['old'];assert files[f].count(old)==1,(f,old[:70],files[f].count(old));files[f]=files[f].replace(old,patch['new'],1)
for f,v in files.items():(ROOT/f).write_text(v)
(ROOT/'benchmark/08-integration-fixes/patch.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2))
print('Applied model patches',len(obj['replacements']))
