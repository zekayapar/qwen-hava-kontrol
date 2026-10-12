from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];s=json.loads((R/'benchmark/SUMMARY.json').read_text());c=json.loads((R/'benchmark/COMPARISON.json').read_text())
out='''# zeka kule — yönlendirilmiş Qwen geliştirme kaydı

13 Ekim2026. HTML/CSS, engine.js simülasyonu ve app.js kontrolleri yerel Qwen3.8 tarafından üretildi. Codex kapsam/API sözleşmesi, promptlar, geri bildirimler, testler, kayıt/yama uygulama araçları, grafikler, repo ve siteyazısını hazırladı. Küçük yamalarda kesin mantık ve konum yönlendirmesi verildi; Qwen tekbaşına/bağımsız geliştirdi iddiası yok. Oyun kodu elle tamamlanmadı; tüm değişiklikler kaydedilmiş modelyanıtlarından alındı.

## Kapsam

1000×700 radar, iki pist ve tür/yön uyumu, pist doluluğu, hafif/orta/ağır uçaklar, rota çizme ve yaklaşma yardımcısı, yakıt, yakınlık/çarpışma, seedli trafik, normal/zor, fırtına/pist kapanışı,1×/2×/4×hız, pause/focus,localStoragekayıt ve JSONiçe/dışa aktarma. Gerçek havacılık simülasyonu değil. Rüzgar değeri gerçek fizik modeli değil; fırtına pist kullanılabilirliğini etkiler.

## Bütün denemeler

| Tur | Girdi | Çıktı | Toplam | İlk içerik ms | HTTP sn | Bitiş |
|---|---:|---:|---:|---:|---:|---|
'''
for r in s['rounds']:
 u=r['usage'];out+=f"| {r['round']} | {u['prompt_tokens']} | {u['completion_tokens']} | {u['total_tokens']} | {r['ttft_ms']:.3f} | {r['total_s']:.3f} | {r['finish_reason']} |\n"
out+='''
06-integration-fixes ayrıca HTTP400 ile reddedildi. Kullanım/süre raporlanmadı ve ilk hata gövdesi yakalanmadı; birleşik tamdosya girdisi+çıktıbütçesi bağlamı aşmış olması request'ten çıkarımdır, ölçülen hata gövdesi değil. request.json ve error.json korunur. Toplam13deneme,12usagebildirilenyanıt. Kesilen02/07yanıtları kullanıma dahildir.

## Hatalar ve düzeltmeler

- 01motor:24öncedenyazılantest23geçti. Aynıkonumdaki ilkwaypoint tüketilip kalanmesafe kullanılmıyordu.8sonradanreviewtest0/8:PRNGstate ilerlememesi,çokluçarpışmasayımı ve savevalidasyonu.
- 02tamUI8192çıktıda kesildi; kullanılmadı. HTML/CSSvecontroller ayrıisteklere bölündü.
- 03motorfix32/32geçti. Sonradanfırtınabitişisave testi eklendi; negatifstormTimerhatası bulundu.
- 04shell ve05controller üretildi.10UItesti0/10; bazıları aynıbaşlangıçpausedhatasına bağlı,10bağımsızhata demekdeğil.
- 06HTTP400;07JSONyama4096tokenda kesildi; uygulanmadı.
- 08yama22değişiklik. İlk43test35/43 çıktısının8hatası CodexVMmock'ta document.querySelector eksikliğiydi; harnessdüzeltildi. Gerçek41/43, loadhız ve busy-pistyardımcısı kaldı.
- 09kesinmetinyaması sözdizimini bozdu. Prompt/yama sınırının belirsizliği de bu hataya katkıda bulundu. 10yanıtının patch eşleştirmesi başarısızdı, uygulanmadı.
- 11iki yükleme fonksiyonu yeniden üretildi;42/43,cleanupnormalyükleme dışında kalmıştı.
- 12cleanup düzeltmesi43/43. Tarayıcıda hız herframe1edönüyordu: Codexpromptu yanlışlıkla animasyonloopbloğunu da yamaya dahil etmişti. Bu yönlendirme hatası Codex'e ait. İkiekUIregresyontesti45testin43ünügeçirdi.
- 13yalnızloopcleanup kaldırıldı. Final45/45 (24önkabul+9motorreview+12UIVM). Test-only VM instrumentation test dosyasında, oyunruntimeında gizlitesthook yok.

## Gerçek tarayıcı ve senaryolar

Chrome başlatma,trafik,uçak seçimi,yaklaşma rotaçizimi,pause/load/continue,hız ve mobil390×844 görünümü kontrol edilir. Gerçektelefon/tümtarayıcı testi değil. tools/scenario.mjs5seedzor senaryodaotomatikyardımcırotalar kullanır:7–14iniş,üçolayda oyunbiter;66–101saniye simüle süre. Her10ticksave/restorestateeşitliği doğrulandı. Simülesüre duvarsaat/GPUloadtesti değil; hedef600sn tüm senaryolarda bitişnedeniyle tamamlanmadı. Genel oyun dengesi ayrıca kullanıcı denemesi ister.

## Koşullar ve ölçüm tanımları

Qwen3.8-27BNVFP4,nvidia revision482ca0f3832238542f8f5295dde86b5f22711d80;GPU0/1 2RTX5090/32GB TP2/MTP3. ThreadripperPRO5955WX;GPU2coder+embedding açık. NVIDIA595.99.02,Ubuntu26.04.1LTS,kernel7.0.0-38-generic,vLLM0.30.0,PyTorch2.13.0+cu132,CUDA runtime13.2,FlashInfer0.6.18.post1,Transformers5.18.0. Context16384,sequence10,batch2048,graph128,FlashInferattention,BF16KV,prefixcacheaçık. Cache sıfırlanmadı,diğerüretimtrafiği kontrol edilmedi;ısıtma/izoleyük/yinedenmodelyükleme yapılmadı. GPUunitleri/ayarları değiştirilmedi.

Temperature0.2,modelseed42,düşünmekapalı; doğalEOS,ignore_eosyok. İstekbudget4096/8192/6144/2048/1024 kaydedilmişrequest'te. YerelvLLM8000direct SSE;gateway/HTTPS dahil değil. MüşteriAPIbudget/izinleri değiştirilmedi. OyununseedliPRNGsi ayrı,modelseed42 ile aynı kavram değil.

TTFT ilk içerik parçası istemciye ulaşması;HTTPtime isteğinden tümakışsonuna. E2Etps çıktı/HTTPsüre;approxdecode=(çıktı−1)/(soniçerik−ilkiçerik). MTPmulti-tokenchunk nedeniyleapproxdecode tokenlatency ölçümü değil. UTCtimestamp Türkiye'de13Ekim01:45+ saatlerine karşılık gelir.
'''
out+=f"\nRaporlanan **{s['prompt_tokens']}girdi+{s['completion_tokens']}çıktı={s['total_tokens']}token**;12akıştoplamı **{s['total_model_http_s']:.6f}sn**. Reddedilen06 için eksikkullanım/süre uydurulmadı. Codextokenı,insan/ajanincelemesi,testler,plot/build/git/toplamgeliştirmeduvarsaat,enerji/amortisman bu toplama dahil değil. Parasal API faturası yok;yerel maliyet sıfıriddiası yok.\n"
out+='''
## İlk oyunla karşılaştırma

İlkoyun4istek,8723girdi/17856çıktı=26579token,108.597sn. Yeniproje13deneme/12yanıt,39399girdi/38623çıktı=78022token,231.217sn. İkisinde aynıQwenprofili ama kapsam,promptlar/modül sayısı/bütçeler farklı. İlkoyuntestleri ilküretimden sonra yazılmıştı;final12test. Yeni24kabultesti ilkistektenönce yazıldı;review/UIsonradan eklendi,final45test. Testoranları doğrudankalitepuanı olarakkarşılaştırılmadı. Tekörnek,tekraryok;kontrollümodelhız/kalitebenchmarkı değil,geliştirmeizikarşılaştırması.

![Tokenlar](tokens.png)
![Model süreleri](time.png)
![İki proje](comparison.png)

## Tekrar

Node22+ `node --test tools/engine.test.mjs tools/review.test.mjs tools/ui.test.mjs` ; senaryo `node tools/scenario.mjs` . `python3 -m http.server 18083 --bind 127.0.0.1`, http://127.0.0.1:18083 . ESmodules içinHTTP gerekir. Herbenchmarkturunda request.json tamgönderilenprompt, response.mdhamyanıt,events.jsonSSE,metrics.jsonusage/time. tools/generate.py kayıtları üzerineyazmayıreddeder. Yenideninferenceyeni turadıyla yapılmalı. Grafikler tools/plot.py (matplotlib),sayısalözettools/compare.py. PublicoyunruntimeınAPI/AIağçağrısı/haricidependency yok.
'''
(R/'benchmark/RESULTS.md').write_text(out)
(R/'README.md').write_text('''# zeka kule ✈️

Qwen3.8'e yönlendirmeyle yazdırılmış hava trafik kontrol oyunu.

[Oyna](https://zekayapar.github.io/qwen-hava-kontrol/) · [Geliştirme yazısı](https://zekayapar.com/yazi/qwen-hava-kontrol) · [Tam ölçüm/hata kaydı](benchmark/RESULTS.md)

Uçağı seçip rotasını çiz, doğru pistin yaklaşma oku yönünde indir. İki pist, üç uçak türü, yakıt, yakınlık/çarpışma, seedli trafik, fırtına/pist kapanışı, kayıt/yükleme ve JSON aktarımı. P duraklat,1/2/4hız,Ryenidenbaşlat. Mobilde dokunmatikrota.

Oyunun HTML/CSS/engine/controller kodu Qwen üretti; Codex kapsam,prompt,inceleme,test/ölçüm araçları,grafik ve entegrasyon yaptı. Bütün promptlar/yanıtlar,kesilen ve hatalıturlar dahil benchmark/ içinde. 13istekdenemesi,12usageyanıtı;78.022token,231.2snmodelHTTP. Final45kontrolgeçti, genelkalitegarantisi değil.

![Oyun](benchmark/game-desktop.png)
![Karşılaştırma](benchmark/comparison.png)

Çalıştır: `python3 -m http.server 18083 --bind 127.0.0.1`. Aç: http://127.0.0.1:18083 . Node22+: `node --test tools/engine.test.mjs tools/review.test.mjs tools/ui.test.mjs` . Runtimeharicidependency/APIyok;MIT.
''')
