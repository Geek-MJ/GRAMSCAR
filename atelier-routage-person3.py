"""TD2 Person 3 routing simulator, adapted to Person 2's WhatsApp rule.
Standalone replacement: instructor's original atelier-routage.py was not supplied.
All quotas, deadlines and scenarios are synthetic demonstrations; no API calls.
"""
import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'GRAMSCAR-main'
MODEL_20 = 'groq:openai/gpt-oss-20b'
MODEL_120 = 'groq:openai/gpt-oss-120b'
MODEL_QWEN = 'groq:qwen/qwen3.8-27b'
# Family scores and preferences supplied by Person 2, not inferred from overlapping summary columns.
PERSON2 = {
    'F1': {'preferred': MODEL_20, 'scores': {MODEL_20: (13,13)}},
    'F2': {'preferred': MODEL_120, 'scores': {MODEL_120: (7,8)}},
    'F2b': {'preferred': MODEL_20, 'scores': {MODEL_20: (2,2), MODEL_120: (2,2), MODEL_QWEN: (2,2)}},
    'F3': {'preferred': MODEL_20, 'scores': {MODEL_20: (7,7)}},
    'combinations': {'preferred': MODEL_20, 'scores': {MODEL_20: (8,8)}},
}
# Other models are fallback candidates, using published TD1 summary for F1/F3/combinations.
# F2 and F2b fallback accuracy is intentionally NOT inferred from combined age_results.
SUMMARY_COLUMNS = {'F1':'period_results', 'F3':'product_results', 'combinations':'combined_results'}


def load_models():
    with (ROOT/'five-model-summary-en.csv').open(newline='',encoding='utf-8') as f:
        summary=list(csv.DictReader(f))
    with (ROOT/'model-question-comparison-en.csv').open(newline='',encoding='utf-8') as f:
        cells=list(csv.DictReader(f))
    resources=[]
    for row in summary:
        ident=f"{row['provider']}:{row['model_id']}"
        scores={}
        for family,col in SUMMARY_COLUMNS.items():
            fraction=row[col].split(' correct')[0]
            scores[family]=tuple(map(int,fraction.split('/')))
        for family,rule in PERSON2.items():
            if ident in rule['scores']:
                scores[family]=rule['scores'][ident]
        evidence={family:[c['case_id'] for c in cells if c['model_id']==ident and c['status']=='correct'] for family in scores}
        resources.append({'id':ident,'scores':scores,'evidence':evidence,'route':'free',
                          'cash':0.0,'allocation':0,'refill_minutes':20,'available':True,
                          'price_note':row['input_usd_per_million'],
                          'documented_paid_route':row['paid_route_same_model']})
    return resources

# Synthetic cases; NOT the instructor's seven scenarios.
SCENARIOS=[
 ('free_ready','F1','dashboard',30),
 ('subscription_ready','F3','dashboard',10),
 ('deferrable','F1','dashboard',40),
 ('deadline_too_soon','F1','dashboard',5),
 ('customer_checked','F3','customer',15),
 ('payout_checked','F2','payout',15),
 ('all_unavailable','F1','dashboard',15),
]

def configure(models,name):
    res=[dict(r,route='free',cash=0.0,allocation=0,refill_minutes=20,available=True) for r in models]
    by_id={r['id']:r for r in res}
    if name=='free_ready': by_id[MODEL_20]['allocation']=3
    elif name=='subscription_ready':
        by_id[MODEL_20]['refill_minutes']=30
        by_id[MODEL_120].update(route='subscription',allocation=2)
    elif name=='deferrable':
        by_id[MODEL_20]['refill_minutes']=10
        by_id[MODEL_120].update(route='subscription',allocation=2)
    elif name=='deadline_too_soon':
        for r in res:r.update(refill_minutes=30,available=False)
    elif name=='customer_checked':
        by_id[MODEL_20]['allocation']=2
        by_id[MODEL_120].update(route='subscription',allocation=2)
    elif name=='payout_checked':
        by_id[MODEL_120]['allocation']=2
    elif name=='all_unavailable':
        for r in res:r.update(available=False,refill_minutes=30)
    return res


def choose(resources,family,use,deadline,prefer_wait=False):
    """Return (action, resource, verification, reason). Routing is NOT validation."""
    if family not in PERSON2:raise ValueError('unknown question family')
    if use not in ('dashboard','customer','payout'):raise ValueError('unknown use')
    preferred=PERSON2[family]['preferred']
    candidates=[]
    for r in resources:
        score=r['scores'].get(family)
        if score is None or score[0]==0:continue
        correct,total=score
        # Person 2's checking rules are mandatory, including for 100% models on high-stakes uses.
        if use=='payout':check='deterministic SQL validation or human review'
        elif use=='customer':check='3-of-5 quorum or deterministic validation'
        elif correct==total and r['route']=='free':check='none'
        else:check='3-of-5 quorum or deterministic validation'
        # Verified means the simulator knows the requirement; it does not execute it.
        candidates.append((r,check,correct,total))
    if not candidates:return ('abstain','-','-',f'{family}: no TD1-supported eligible model')
    # Prefer Person 2's family choice, then observed full-family success and free access.
    candidates.sort(key=lambda x:(x[0]['id']!=preferred,x[2]!=x[3],x[0]['route']!='free',x[0]['id']))
    now_free=[x for x in candidates if x[0]['available'] and x[0]['route']=='free' and x[0]['allocation']>0]
    now_sub=[x for x in candidates if x[0]['available'] and x[0]['route']=='subscription' and x[0]['allocation']>0]
    wait=[x for x in candidates if x[0]['available'] and x[0]['route']=='free' and x[0]['refill_minutes']<=deadline]
    def pack(action,x,why):
        r,check,correct,total=x
        ids=', '.join(r['evidence'].get(family,[])[:5]) or 'family IDs pending Person 1'
        return (action,r['id'],check,f'{family}: {correct}/{total} correct (Person 2); '
                f'example correct TD1 cells (not family-filtered): {ids}; {why}; validation is NOT executed')
    if now_free:return pack('run',now_free[0],'free quota available now')
    if prefer_wait and wait:
        return pack('defer',min(wait,key=lambda x:x[0]['refill_minutes']),
                    'nonurgent: free refill within deadline; preserve included subscription capacity')
    if now_sub:return pack('run',now_sub[0],'included subscription capacity available immediately')
    if wait:return pack('defer',min(wait,key=lambda x:x[0]['refill_minutes']),
                        'eligible free quota refills before deadline')
    return ('abstain','-','-',f'{family}: no eligible route available within deadline')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--scenario',choices=[s[0] for s in SCENARIOS])
    parser.add_argument('--prefer-wait',action='store_true')
    args=parser.parse_args()
    models=load_models()
    print('TD2 Person 3 — adapted to Person 2 routing policy')
    print('WARNING: standalone replacement; all seven scenarios/quotas are illustrative, not instructor originals.')
    print('F2b tie: GPT-OSS-20B provisionally chosen among free 2/2 models; no verified cost ranking.')
    print('RUN means a model route is selected; required quorum/SQL/human checks are NOT performed.')
    for name,family,use,deadline in SCENARIOS:
        if args.scenario and name!=args.scenario:continue
        action,resource,check,reason=choose(configure(models,name),family,use,deadline,args.prefer_wait)
        print(f'\n{name}: {action.upper()} | {resource}\n  check: {check}\n  reason: {reason}')

if __name__=='__main__':main()
