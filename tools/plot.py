from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];s=json.loads((ROOT/'benchmark/SUMMARY.json').read_text());c=json.loads((ROOT/'benchmark/COMPARISON.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':17,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False})
bg='#f5f8fc';ink='#18334e';blue='#3b82f6';orange='#e9a23b';teal='#19a7a0'
def finish(fig,name):
 fig.text(.06,.94,'zeka kule · Qwen3.8 geliştirme kayıtları',fontsize=28,weight='bold',color=ink)
 fig.text(.06,.88,'2 × RTX 5090 / 32 GB · NVFP4 · TP2 / MTP3',fontsize=19,color='#566b80')
 fig.text(.06,.05,'Kesilen yanıtlar dahil · model HTTP akışı · tüm geliştirme süresi değil',fontsize=16,color='#566b80')
 fig.text(.94,.05,'@zekayapar',ha='right',fontsize=17,color=ink)
 fig.savefig(ROOT/'benchmark'/name,dpi=100,facecolor=bg);plt.close(fig)
labels=[f"{int(r['round'].split('-')[0])}. tur" for r in s['rounds']];inputs=[r['usage']['prompt_tokens'] for r in s['rounds']];outputs=[r['usage']['completion_tokens'] for r in s['rounds']]
fig,ax=plt.subplots(figsize=(16,9),facecolor=bg);fig.subplots_adjust(left=.12,right=.92,top=.76,bottom=.18);ax.set_facecolor(bg)
ax.barh(labels,inputs,color=blue,label='Girdi');ax.barh(labels,outputs,left=inputs,color=orange,label='Çıktı');ax.invert_yaxis();ax.set_xlabel('Token');ax.legend(loc='lower right');ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
for i,(a,b) in enumerate(zip(inputs,outputs)):ax.text(a+b+150,i,f'{a+b:,}'.replace(',','.'),va='center',fontsize=17)
ax.set_xlim(0,max(a+b for a,b in zip(inputs,outputs))*1.18);finish(fig,'tokens.png')
fig,ax=plt.subplots(figsize=(16,9),facecolor=bg);fig.subplots_adjust(left=.12,right=.92,top=.76,bottom=.18);ax.set_facecolor(bg);times=[r['total_s'] for r in s['rounds']];ax.barh(labels,times,color=teal);ax.invert_yaxis();ax.set_xlabel('Model yanıt süresi · saniye');ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
for i,t in enumerate(times):ax.text(t+.5,i,f'{t:.2f}'.replace('.',','),va='center')
ax.set_xlim(0,max(times)*1.18);finish(fig,'time.png')
fig,axes=plt.subplots(1,2,figsize=(16,9),facecolor=bg);fig.subplots_adjust(left=.09,right=.94,top=.74,bottom=.23,wspace=.28)
for ax,key,title in zip(axes,['total_tokens','total_model_http_s'],['Toplam Qwen tokenı','Model çağrıları · saniye']):
 vals=[c['first_game'][key],c['air_traffic'][key]];ax.set_facecolor(bg);ax.bar(['Uçak oyunu','Hava kontrol'],vals,color=[blue,teal],width=.55);ax.set_title(title,pad=20);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True);ax.set_ylim(0,max(vals)*1.22)
 for i,v in enumerate(vals):ax.text(i,v+max(vals)*.035,f'{v:,.0f}'.replace(',','.') if key=='total_tokens' else f'{v:.1f}'.replace('.',','),ha='center',fontsize=23,weight='bold',color=ink)
fig.text(.06,.94,'İki oyunun geliştirme kayıtları',fontsize=30,weight='bold',color=ink);fig.text(.06,.87,f"{c['calls'][0]} istek → {c['calls'][1]} istek · aynı Qwen profili, farklı kapsam ve promptlar",fontsize=20,color='#566b80');fig.text(.06,.07,'Kesilen yanıtlar dahil · kontrollü hız/kalite karşılaştırması değil',fontsize=17,color='#566b80');fig.text(.94,.07,'@zekayapar',ha='right',fontsize=17,color=ink);fig.savefig(ROOT/'benchmark/comparison.png',dpi=100,facecolor=bg)
