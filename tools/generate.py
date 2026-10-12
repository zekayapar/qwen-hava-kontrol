"""Record a real local Qwen coding round, including exact prompt/response and timings."""
import json,time,urllib.request,hashlib,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(round_name,system,prompt,max_tokens=4096,write_html=True):
 assert not (ROOT/'benchmark'/round_name).exists(), 'Never overwrite historical round'
 payload={'model':'Qwen/Qwen3.8-27B','messages':[{'role':'system','content':system},{'role':'user','content':prompt}],'max_tokens':max_tokens,'temperature':0.2,'seed':42,'stream':True,'stream_options':{'include_usage':True},'chat_template_kwargs':{'enable_thinking':False}}
 p=ROOT/'benchmark'/round_name;p.mkdir(exist_ok=True)
 (p/'request.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();start=time.perf_counter();first=last=None;chunks=[];events=[];usage=None;finish=None
 req=urllib.request.Request('http://127.0.0.1:8000/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=180) as response:
  for line in response:
   if not line.startswith(b'data: '):continue
   b=line[6:].strip()
   if b==b'[DONE]':break
   event=json.loads(b);events.append(event)
   if event.get('usage'):usage=event['usage']
   for c in event.get('choices',[]):
    if c.get('finish_reason'):finish=c['finish_reason']
    text=c.get('delta',{}).get('content','')
    if text:
     now=time.perf_counter();first=first or now;last=now;chunks.append(text)
 elapsed=time.perf_counter()-start;answer=''.join(chunks)
 (p/'response.md').write_text(answer)
 (p/'events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
 assert usage and first,'Missing usage/content'
 report={'round':round_name,'started_at_utc':started,'finish_reason':finish,'usage':usage,'ttft_ms':(first-start)*1000,'total_s':elapsed,'generation_window_s':last-first,'e2e_tokens_per_s':usage['completion_tokens']/elapsed,'decode_tokens_per_s':(usage['completion_tokens']-1)/(last-first) if last>first else None,'response_sha256':hashlib.sha256(answer.encode()).hexdigest(),'temperature':.2,'seed':42,'thinking':False,'max_tokens':max_tokens,'endpoint_scope':'localhost vLLM, production TP2/MTP3; no gateway/HTTPS','content_chunks':len(chunks)}
 (p/'metrics.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
 assert finish!='length','Truncated output; do not deploy'
 if not write_html:return report
 content=answer.split('```html',1)[1].split('```',1)[0].strip() if '```html' in answer else answer.strip().removeprefix('```').removesuffix('```')
 assert '<html' in content.lower() and '</html>' in content.lower(),'Not complete HTML'
 (ROOT/'index.html').write_text(content+'\n');return report

