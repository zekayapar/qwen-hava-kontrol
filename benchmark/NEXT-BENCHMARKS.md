# Sonraki örnek projeler ve benchmark adayları

Henüz uygulanmadı; sonuç yok. Üretim modelleri/şirket izinleri değiştirilmeyecek. Kullanıcı13Ekim mevcutcoder veembedding ile de örnekproje istedi; gelişmişoyunsonrasına.

1. **Coder7B ve Qwen27B ile aynı küçük uygulama:** CSVanaliz projesinin aynı dar parser/filter/export görevleri, aynı girdiler ve önceden testler. İlkgeçiş/finaltest, düzeltmeisteği, token/TTFT/süre. Birprojeden genelcoding sıralaması yok; en az3bağımsızgörev ve tekrar.
2. **Embedding ile belge arama:** tamamen sentetik50belge ve önceden20soru/ilgilibelgegold. 1024boyutembedding+cosinesimilarity; top1/top5isabet/MRR,1/8/32batch gecikmesi ve metin/sn. Arayüz soru→ilgilibelgeler; RAGyanıt üretimi ayrıcaQweneklenebilir, retrievalbaşarısıilechatdoğruluğuayrı. GerçekşirketSQL/verileri yok.
3. **JSONçıkarma:** aynı sentetikmetinler/alanlar, prompt-only ve JSONschema constrained ayrı. JSONparse/schema/geçerli alanvalue doğruluğu birbirinden ayrı;20örnek×3tekrar,TTFT/toplamzaman/token. MevcutvLLMresmibelge https://docs.vllm.ai/en/latest/examples/features/structured_outputs/ . JSONgeçerli olması içerikdoğru demekdeğil.
4. **Uzunprompt ve prefixreuse:**1k/4k/8kgirdi içinde kontrollü kanıt sorusu, benzersizveortakprefix ayrı, cacheisolationtestnamespace; başkalarınıncache'iniresetleme. TTFTp50/p95,cevapkanıtdoğruluğu,toplamHTTP/decode/throughput ayrı. Resmimetodoloji https://docs.vllm.ai/en/stable/benchmarking/cli/ ; repeatedcache throughputşişirebilir.

CSV ve miniSQL önerileri backlog; bu turda geliştirilmedi. Sosyalpaylaşımlar kaynakrapor/grafik sonrasıX/Instagram/Threadsüçlü taslak ve açıkonayla; otomatikyarınyayın/scheduling yok.
