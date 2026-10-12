# zeka kule: önceden belirlenen kapsam ve ölçüm

13 Ekim2026. İlk Qwen çağrısından önce 24Node kabul testi yazıldı. Trafik kontrolü1000×700alan, iki pist/tür uyumu ve pist doluluğu, rota çizme/yakıt, separation/collision, seedli trafik, hava durumu, zorluk, pause/hız, save/load. Engine/UI modülleri ayrı gerçek isteklerle Qwen'e üretilecek; Codex coreoyunkodu yazmayacak. Hatalar Qwen'e test/review çıktısıyla geri verilecek. Her request/response/SSE/usage/time korunacak.

Önceki küçük uçak oyunu27B/NVFP4 TP2/MTP3 profili korunur. Yeni testleri önceki projeye geriye dönük uydurma yok. İlk oyunun testleri ilk koddan sonra yazılmıştı; yenisinde24kabultest önce tanımlandı. Farklıkapsam/prompt/tokenbudgets nedeniyle kontrollü model/hız karşılaştırması değildir. Karşılaştırma istek sayısı,girdi/çıktıtoken,modelHTTP toplamı,ilk ve son test durumu,düzeltmeler; Codex tokenı/ajan hazırlık/test/toplamduvarsaat ve enerji ayrı ya da ölçülmedi.

Gerçek müşteri verisi yok. Modelservisi restart edilmez; üretim/cache/başkatrafik kontrol edilmediği not edilir. Çıktıbudget8192,context16384; yerelvLLMdirect request, müşteriAPIlimitleri değiştirilmez. Oyun randomseedliyken modelseed42aynıanlamdeğil.
