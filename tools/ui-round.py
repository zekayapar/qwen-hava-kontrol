from generate import run,ROOT
p=(ROOT/'tools/ui-prompt.txt').read_text()+(ROOT/'engine.js').read_text()
run('02-interface','Sen deneyimli JavaScript oyun ve UI geliştiricisisin. Tam index.html dosyasını tek html kod bloğunda üret; açıklama yok, harici bağımlılık yok.',p,8192,True)
