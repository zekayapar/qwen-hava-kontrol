from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
rows=[json.loads(f.read_text()) for f in sorted((ROOT/'benchmark').glob('*/metrics.json'))]
s={'rounds':rows,'prompt_tokens':sum(r['usage']['prompt_tokens'] for r in rows),'completion_tokens':sum(r['usage']['completion_tokens'] for r in rows),'total_tokens':sum(r['usage']['total_tokens'] for r in rows),'total_model_http_s':sum(r['total_s'] for r in rows),'source_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['engine.js','index.html','app.js'] if (ROOT/f).exists()}}
(ROOT/'benchmark/SUMMARY.json').write_text(json.dumps(s,indent=2)+'\n')
a=json.loads((ROOT.parent/'qwen-ucak-oyunu/benchmark/SUMMARY.json').read_text())
c={'first_game':{k:a[k] for k in ['prompt_tokens','completion_tokens','total_tokens','total_model_http_s']},'air_traffic':{k:s[k] for k in ['prompt_tokens','completion_tokens','total_tokens','total_model_http_s']},'calls':[len(a['rounds']),len(rows)],'scope':'Different projects and prompts; development trace comparison, not controlled speed or quality benchmark.'}
(ROOT/'benchmark/COMPARISON.json').write_text(json.dumps(c,indent=2)+'\n')
print({k:v for k,v in s.items() if k!='rounds'})
