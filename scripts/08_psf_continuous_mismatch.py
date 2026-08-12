from pathlib import Path
import sys
src=Path(__file__).with_name('07_psf_disjoint_split_challenge.py').read_text()
prefix=src.split('\nrows=[]',1)[0]
ns={}; exec(prefix,ns)
np=ns['np']; pd=ns['pd']; gaussian_filter=ns['gaussian_filter']; shift=ns['shift']; psf=ns['psf']; feat=ns['feat']; score=ns['score']; cut=ns['cut']; seed=ns['seed']; Ts=ns['Ts']; Gs=ns['Gs']; sids=ns['sids']; ZP=ns['ZP']; LAM=ns['LAM']; bb=ns['bb']; jy=ns['jy']; OUT=ns['OUT']
# Controlled mismatch: scoring PSF uses all 23 non-test hosts; injection PSF is a perturbed copy.
variants={
 'matched':('none',0.0),
 'blur_mild':('blur',None),
 'blur_moderate':('blur2',None),
 'offset_0p1pix':('offset',0.1),
 'offset_0p25pix':('offset',0.25),
 'offset_0p5pix':('offset',0.5),
}
def makeq(p,band,var):
 q=p.copy()
 if var=='blur_mild':
  sig=0.35 if band=='W3' else 0.60
  q=gaussian_filter(q,sig)
 if var=='blur_moderate':
  sig=0.70 if band=='W3' else 1.20
  q=gaussian_filter(q,sig)
 if var.startswith('offset_'):
  pix={'offset_0p1pix':0.1,'offset_0p25pix':0.25,'offset_0p5pix':0.5}[var]
  q=shift(q,shift=(0.0,pix),order=1,mode='constant',cval=0.0)
 q=np.clip(q,0,None); q/=q.sum(); return q
rows=[]
for band in ('W3','W4'):
 for test in sids:
  train=[s for s in sids if s!=test]; pscore=psf(train,band)
  trainX=np.stack([feat(s,band,pscore)[0] for s in train]); trainS=np.array([score(x,trainX) for x in trainX]); thr=float(trainS.max())
  x0,A0=feat(test,band,pscore); s0=score(x0,trainX); bpass=s0<=thr+1e-12; st=seed.loc[test]; mag=float(st.w3mpro if band=='W3' else st.w4mpro); Fs=jy(mag,ZP[band]); Fbol=float(st.Fbol_fit_Wm2)
  for var in variants:
   q=makeq(pscore,band,var)
   for T in Ts:
    Fd=Fbol*bb(LAM[band],T)/ns['JY']
    for g in Gs:
     boost=((1-g)*Fs+g*Fd)/Fs; imag=mag-2.5*np.log10(boost); sat=imag<(3.8 if band=='W3' else -0.4); new=cut[(test,band)]['img']+max(boost-1,0)*A0*q; xi,_=feat(test,band,pscore,new); si=score(xi,trainX)
     rows.append({'source_id':test,'band':band,'variant':var,'T_DS_K':T,'gamma':g,'baseline_pass':bpass,'saturation_risk':sat,'injected_pass':si<=thr+1e-12,'score_change':si-s0})
df=pd.DataFrame(rows); valid=df[df.baseline_pass&~df.saturation_risk]
summary=[]
for (band,var),d in valid.groupby(['band','variant']):
 h=d.groupby('source_id').injected_pass.all(); summary.append({'band':band,'variant':var,'N_hosts':d.source_id.nunique(),'N_valid':len(d),'retention':d.injected_pass.mean(),'host_allpass_fraction':h.mean(),'hosts_with_any_failure':int((~h).sum()),'median_score_change':d.score_change.median()})
summary=pd.DataFrame(summary)
df.to_csv(OUT/'psf_continuous_mismatch_cases.csv.gz',index=False,compression='gzip'); summary.to_csv(OUT/'psf_continuous_mismatch_summary.csv',index=False)
print(summary.to_string(index=False))
