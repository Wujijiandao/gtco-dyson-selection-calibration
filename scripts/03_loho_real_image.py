#!/usr/bin/env python3
"""
Submission-grade leave-one-host-out real AllWISE injection check.
The held-out host is excluded from empirical PSF construction and from the
calibration envelope used to classify that host.
"""
from pathlib import Path
import sys, gzip, re, numpy as np, pandas as pd
from scipy.ndimage import map_coordinates, shift

DATA=Path(sys.argv[1]).resolve()
OUT=Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True,exist_ok=True)

def raw(path):
    b=Path(path).read_bytes()
    return gzip.decompress(b) if b[:2]==b"\x1f\x8b" else b
def pv(s):
    s=s.strip()
    if s.startswith("'"):
        j=s.find("'",1); return s[1:j] if j>=0 else s.strip("'")
    s=s.split("/")[0].strip()
    if s=="T": return True
    if s=="F": return False
    try: return float(s) if any(c in s for c in ".Ee") else int(s)
    except: return s
def fits(path):
    b=raw(path); h={}; end=None
    for off in range(0,len(b),80):
        c=b[off:off+80].decode("ascii","replace"); k=c[:8].strip()
        if k=="END": end=off+80; break
        if len(c)>=10 and c[8:10]=="= ": h[k]=pv(c[10:])
    dataoff=((end+2879)//2880)*2880
    dt={-32:">f4",-64:">f8",16:">i2",32:">i4",8:"u1"}[int(h["BITPIX"])]
    a=np.frombuffer(b,dtype=np.dtype(dt),count=int(h["NAXIS1"])*int(h["NAXIS2"]),offset=dataoff)
    a=a.reshape(int(h["NAXIS2"]),int(h["NAXIS1"])).astype(float)
    return h,a*float(h.get("BSCALE",1))+float(h.get("BZERO",0))
def w2p(h,ra_deg,dec_deg):
    ra0=np.deg2rad(float(h["CRVAL1"])); d0=np.deg2rad(float(h["CRVAL2"]))
    ra=np.deg2rad(ra_deg); d=np.deg2rad(dec_deg); dra=ra-ra0
    l=np.cos(d)*np.sin(dra)
    m=np.sin(d)*np.cos(d0)-np.cos(d)*np.sin(d0)*np.cos(dra)
    xdeg,ydeg=np.rad2deg(l),np.rad2deg(m)
    th=np.deg2rad(float(h.get("CROTA2",0)))
    xr=xdeg*np.cos(th)+ydeg*np.sin(th); yr=-xdeg*np.sin(th)+ydeg*np.cos(th)
    return float(h["CRPIX1"])+xr/float(h["CDELT1"])-1, float(h["CRPIX2"])+yr/float(h["CDELT2"])-1
def sample(a,x0,y0,n=61,order=1):
    c=(n-1)/2; yy,xx=np.mgrid[0:n,0:n]
    return map_coordinates(a,np.array([y0+(yy-c),x0+(xx-c)]),order=order,mode="constant",cval=np.nan)

seed=pd.read_csv(DATA/"gtco_e17a_real_image_seed_sample.csv",dtype={"source_id":"string"})
master=pd.read_csv(DATA/"gtco_e12_real_100pc_master_with_msflags.csv.gz",
                   usecols=["source_id","ra","dec","pmra","pmdec","w3mpro","w4mpro"],
                   dtype={"source_id":"string"})
val=pd.read_csv(DATA/"gtco_e12c_validation_sample_3000.csv",
                usecols=["source_id","Fbol_fit_Wm2"],dtype={"source_id":"string"})
seed=seed.drop(columns=[c for c in ["ra","dec","w3mpro","w4mpro"] if c in seed.columns])
seed=seed.merge(master,on="source_id",validate="one_to_one").merge(val,on="source_id",validate="one_to_one")
dt=-5.5
seed["dec_wise"]=seed.dec+seed.pmdec.fillna(0)*dt/3.6e6
seed["ra_wise"]=seed.ra+seed.pmra.fillna(0)*dt/(3.6e6*np.cos(np.deg2rad(seed.dec)))
seed=seed.set_index("source_id")

# Locate FITS folder.
candidates=[
    DATA/"GTCO_E17_WISE_cutouts",
    DATA/"e17i_real_fits_full"/"GTCO_E17_WISE_cutouts",
]
IMG=next((p for p in candidates if p.exists()),None)
if IMG is None:
    raise SystemExit("WISE FITS folder not found")
prod={}
for p in IMG.glob("*"):
    m=re.match(r"(\d+)_w([34])_(int|unc|cov)\.fits(?:\.gz)?$",p.name)
    if m: prod[(m.group(1),"W"+m.group(2),m.group(3))]=p

N=61; yy,xx=np.mgrid[0:N,0:N]; c0=30.; rad=np.hypot(xx-c0,yy-c0)
cut={}
for sid,s in seed.iterrows():
    for band in ("W3","W4"):
        h,im0=fits(prod[(sid,band,"int")]); _,u0=fits(prod[(sid,band,"unc")])
        xp,yp=w2p(h,s.ra_wise,s.dec_wise)
        cut[(sid,band)]={"img":sample(im0,xp,yp),"unc":sample(u0,xp,yp)}

def bg(im): return float(np.nanmedian(im[(rad>=22)&(rad<=28)&np.isfinite(im)]))
def align(im,band):
    y=im-bg(im); rc=7 if band=="W3" else 11
    pos=np.where((rad<=rc)&np.isfinite(y),np.clip(y,0,None),0)
    return ((pos*xx).sum()/pos.sum(),(pos*yy).sum()/pos.sum()) if pos.sum()>0 else (c0,c0)
def psf(train,band):
    st=[]
    for sid in train:
        im=cut[(sid,band)]["img"]; xb,yb=align(im,band)
        a=shift(im-bg(im),shift=(c0-yb,c0-xb),order=1,mode="constant",cval=np.nan)
        rap=9 if band=="W3" else 14
        f=np.nansum(a[(rad<=rap)&np.isfinite(a)])
        if f>0: st.append(a/f)
    p=np.nanmedian(np.stack(st),axis=0); p=np.where(np.isfinite(p),p,0); p=np.clip(p,0,None)
    p[rad>22]=0; p/=p.sum(); return p
def features(sid,band,p,img=None):
    d=cut[(sid,band)]; im=d["img"] if img is None else img; u=d["unc"]; y=im-bg(im)
    rf=11 if band=="W3" else 17
    m=(rad<=rf)&np.isfinite(y)&np.isfinite(u)&(u>0)&(p>0); w=1/u[m]**2
    A=np.sum(w*y[m]*p[m])/np.sum(w*p[m]**2); r=y-A*p
    chi=np.sum((r[m]/u[m])**2)/max(1,m.sum()-1)
    res=np.nansum(np.abs(r[(rad<=rf)&np.isfinite(r)]))/max(abs(A),1e-12)
    rc=10 if band=="W3" else 15
    pos=np.where((rad<=rc)&np.isfinite(y),np.clip(y,0,None),0)
    xb=(pos*xx).sum()/pos.sum(); yb=(pos*yy).sum()/pos.sum()
    cent=np.hypot(xb-c0,yb-c0)*1.375
    dx=xx-xb; dy=yy-yb
    mxx=(pos*dx*dx).sum()/pos.sum(); myy=(pos*dy*dy).sum()/pos.sum(); mxy=(pos*dx*dy).sum()/pos.sum()
    ev=np.linalg.eigvalsh([[mxx,mxy],[mxy,myy]]); axis=np.sqrt(max(ev[-1],1e-12)/max(ev[0],1e-12))
    return np.array([np.log1p(chi),np.log1p(res),cent,np.log(axis)]),float(A)
def score(x,trainX):
    med=np.nanmedian(trainX,axis=0); mad=1.4826*np.nanmedian(np.abs(trainX-med),axis=0); mad=np.where(mad>1e-8,mad,1)
    return float(np.nanmax((x-med)/mad))

ZP={"W3":29.045,"W4":8.2839}; LAM={"W3":12.,"W4":22.}
H=6.62607015e-34; C=299792458.; KB=1.380649e-23; SB=5.670374419e-8; JY=1e-26
def bb(lam,T):
    lam*=1e-6; nu=C/lam; x=H*nu/(KB*T)
    return np.pi*(2*H*nu**3/C**2)/np.expm1(x)/(SB*T**4)
def jy(m,zp): return zp*10**(-.4*m)

Tgrid=[100,150,200,250,300]; Ggrid=[.03,.05,.08,.10,.14,.16]
sids=list(seed.index); rows=[]
for band in ("W3","W4"):
    for test in sids:
        train=[s for s in sids if s!=test]; p=psf(train,band)
        trainX=np.stack([features(s,band,p)[0] for s in train])
        trainS=np.array([score(x,trainX) for x in trainX]); thr=float(trainS.max())
        x0,A0=features(test,band,p); s0=score(x0,trainX); bpass=s0<=thr+1e-12
        st=seed.loc[test]; mag=float(st.w3mpro if band=="W3" else st.w4mpro)
        Fs=jy(mag,ZP[band]); Fbol=float(st.Fbol_fit_Wm2)
        for T in Tgrid:
            Fd=Fbol*bb(LAM[band],T)/JY
            for g in Ggrid:
                boost=((1-g)*Fs+g*Fd)/Fs; imag=mag-2.5*np.log10(boost)
                sat=imag<(3.8 if band=="W3" else -0.4)
                xi,_=features(test,band,p,cut[(test,band)]["img"]+max(boost-1,0)*A0*p)
                si=score(xi,trainX)
                rows.append(dict(source_id=test,band=band,T_DS_K=T,gamma=g,baseline_pass=bpass,
                                 catalog_saturation_risk=sat,injected_pass=si<=thr+1e-12,
                                 baseline_score=s0,injected_score=si,score_change=si-s0))
df=pd.DataFrame(rows)
df.to_csv(OUT/"loho_real_image_injections.csv.gz",index=False,compression="gzip")
for band in ("W3","W4"):
    d=df[(df.band==band)&df.baseline_pass&~df.catalog_saturation_risk]
    print(band,"independent hosts",d.source_id.nunique(),"valid injections",len(d),"retention",d.injected_pass.mean())
