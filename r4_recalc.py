import json, math, os
base="paper_workflow_kb/results"
def load(n):
    with open(os.path.join(base,n),encoding="utf-8") as f: return json.load(f)
def wilson(x,n,z=1.96):
    if n==0: return (0,0)
    p=x/n; d=1+z*z/n; c=p+z*z/(2*n)
    m=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return ((c-m)/d,(c+m)/d)

out={}
# Table 1 checks: pull from unified + per-stratum files
ece=load("ece_unified.json")
print("== ece_unified strata ==")
for k,v in ece.get("strata",{}).items():
    print(k, v)
print("== tempscale_equalwidth ==", ece.get("tempscale_equalwidth"))
print("== isotonic_equalwidth ==", ece.get("isotonic_equalwidth"))

# hetero
het=load("r18_heteromodel.json"); heta=load("r18_heteromodel_adjudication.json")
print("\n== hetero raw ==", het)
print("== hetero adj ==", heta)
# accuracy check: 21/60=0.35, 32/60 raw guarded? 29/60 adj
print("21/60=",21/60,"32/60=",32/60,"29/60=",29/60,"8/60=",8/60,"11/60=",11/60)

# r18 loose rep
r18=load("r18_loose_rep.json"); r18a=load("r18_adjudication.json")
print("\n== r18 raw ==", r18)
print("== r18 adj ==", r18a)
print("15/60=",15/60,"42/60=",42/60,"39/60=",39/60,"24/60=",24/60,"27/60=",27/60)

# gold100
g100=load("gold100_agreement.json")
print("\n== gold100 ==", g100)
print("wilson 86/100:", wilson(86,100))
print("wilson 88/100:", wilson(88,100))
print("wilson 58/62:", wilson(58,62))
print("wilson 71/79:", wilson(71,79))
print("wilson 24/25:", wilson(24,25))

# holm
holm=load("holm.json")
print("\n== holm ==", json.dumps(holm,ensure_ascii=False)[:3000])
# recompute exact McNemar p = 2/2^b for c=0
for b in [27,24,20,11,9,5,4,2,1,0]:
    if b==0: p=1.0
    else: p=2/2**b
    print(f"b={b} p={p:.10g}")
# verify ordering
tests = holm.get("tests", holm.get("family", []))
print("holm keys:", list(holm.keys()))

# merged
m=load("merged_1062.json")
print("\n== merged ==", m)
print("830/1062=",830/1062,"922/1062=",922/1062,"92/1062=",92/1062)

# n157
n157=load("tempiso_n157.json")
print("\n== n157 ==", json.dumps(n157,ensure_ascii=False)[:3000])

# guard synth
gs=load("guard_synth.json")
print("\n== guard_synth ==", json.dumps(gs,ensure_ascii=False)[:3000])

# powrep arms for table
pr=load("powrep.json")
print("\n== powrep ==", json.dumps(pr,ensure_ascii=False)[:2500])
xd=load("xdomain.json")
print("\n== xdomain ==", json.dumps(xd,ensure_ascii=False)[:2500])
