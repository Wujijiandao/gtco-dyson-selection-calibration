#!/usr/bin/env python3
"""
GTCO submission-grade E12c/E17f standalone reconstruction.

Reconstructs from frozen real-source inputs:
  1) 265-template x 49-temperature x 17-gamma = 220,745 partial-Dyson library;
  2) 54-cell injection/recovery on 3,000 independent real validation stars;
  3) same-source joint photometric + deterministic host selection.

The script is intentionally independent of the frozen E17f result tables. It may
optionally compare its outputs against those tables if they are present.

Key frozen implementation choices:
- 10 bands: Gaia G/BP/RP, 2MASS J/H/Ks, AllWISE W1/W2/W3/W4;
- single-temperature blackbody waste heat;
- flux-space Gaussian noise with per-source catalogue uncertainties;
- seed = 20261005;
- catalogue survival includes realised positive flux in all 10 bands,
  G <= 21, expected J/H/Ks SNR > 2, expected W3/W4 SNR > 3.5;
- nearest model in unweighted 10-magnitude Euclidean space;
- accepted if nearest-model RMSE <= 0.2 mag;
- host gate uses pass_hostcuts_w1000.
"""
from pathlib import Path
import argparse, json, math
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

SEED = 20261005
T_LIBRARY = np.linspace(100.0, 700.0, 49)
G_LIBRARY = np.linspace(0.1, 0.9, 17)
T_TRUTH = np.array([100,150,200,250,300,400,500,600,700], dtype=float)
G_TRUTH = np.array([0.1,0.2,0.3,0.5,0.7,0.9], dtype=float)

BANDS = ["G","BP","RP","J","H","Ks","W1","W2","W3","W4"]
MAGCOLS = [
    "phot_g_mean_mag","phot_bp_mean_mag","phot_rp_mean_mag",
    "j_m","h_m","ks_m","w1mpro","w2mpro","w3mpro","w4mpro"
]
# Effective wavelengths in micron used by the frozen reconstruction.
LAMBDA_UM = np.array([0.673,0.532,0.797,1.235,1.662,2.159,3.4,4.6,12.0,22.0])
# Vega zero-magnitude flux densities in Jy used by the frozen reconstruction.
ZERO_JY = np.array([3228.75,3552.01,2554.95,1594.0,1024.0,666.7,309.54,171.787,29.045,8.2839])

H = 6.62607015e-34
C = 299792458.0
KB = 1.380649e-23
SIGMA_SB = 5.670374419e-8
JY = 1e-26
MAGERR_TO_FRACFLUX = 0.4*np.log(10.0)
FLUXSNR_TO_MAGERR = 2.5/np.log(10.0)


def bb_shape_nu(lam_um, T):
    lam = np.asarray(lam_um, dtype=float)*1e-6
    nu = C/lam
    x = H*nu/(KB*T)
    Bnu = (2*H*nu**3/C**2)/np.expm1(x)
    return np.pi*Bnu/(SIGMA_SB*T**4)  # Hz^-1; integral over nu is unity


def absolute_mags(df):
    m = df[MAGCOLS].to_numpy(float)
    dm = 5*np.log10(df["distance_invparallax_pc"].to_numpy(float)/10.0)
    return m-dm[:,None]


def ds_absolute_mags(df, T, gamma):
    Mstar = absolute_mags(df)
    Fstar10 = ZERO_JY[None,:]*10**(-0.4*Mstar)
    d = df["distance_invparallax_pc"].to_numpy(float)
    Fbol10 = df["Fbol_fit_Wm2"].to_numpy(float)*(d/10.0)**2
    Fds10 = Fbol10[:,None]*bb_shape_nu(LAMBDA_UM,T)[None,:]/JY
    F = (1-gamma)*Fstar10 + gamma*Fds10
    return -2.5*np.log10(F/ZERO_JY[None,:])


def baseline_flux_and_sigma(df):
    m = df[MAGCOLS].to_numpy(float)
    F = ZERO_JY[None,:]*10**(-0.4*m)
    sig = np.empty_like(F)
    sig[:,0] = F[:,0]/df["phot_g_mean_flux_over_error"].to_numpy(float)
    sig[:,1] = F[:,1]/df["phot_bp_mean_flux_over_error"].to_numpy(float)
    sig[:,2] = F[:,2]/df["phot_rp_mean_flux_over_error"].to_numpy(float)
    errcols=["j_msigcom","h_msigcom","ks_msigcom","w1mpro_error","w2mpro_error","w3mpro_error","w4mpro_error"]
    for j,c in enumerate(errcols,start=3):
        sig[:,j] = F[:,j]*MAGERR_TO_FRACFLUX*df[c].to_numpy(float)
    return F,sig


def expected_snr(df, flux_ratio):
    snr=np.empty_like(flux_ratio)
    snr[:,0]=df["phot_g_mean_flux_over_error"].to_numpy(float)*flux_ratio[:,0]
    snr[:,1]=df["phot_bp_mean_flux_over_error"].to_numpy(float)*flux_ratio[:,1]
    snr[:,2]=df["phot_rp_mean_flux_over_error"].to_numpy(float)*flux_ratio[:,2]
    errcols=["j_msigcom","h_msigcom","ks_msigcom","w1mpro_error","w2mpro_error","w3mpro_error","w4mpro_error"]
    for j,c in enumerate(errcols,start=3):
        snr[:,j]=(FLUXSNR_TO_MAGERR/df[c].to_numpy(float))*flux_ratio[:,j]
    return snr


def locate(data, name):
    p=data/name
    if not p.exists():
        raise FileNotFoundError(p)
    return p


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("data_root", type=Path)
    ap.add_argument("output_dir", type=Path)
    ap.add_argument("--host-flags", type=Path, default=None,
                    help="Generated hostcut_flags.csv.gz; falls back to frozen gtco_e17e_hostcut_flags_v2.csv.gz")
    args=ap.parse_args()
    data=args.data_root.resolve(); out=args.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)

    templates=pd.read_csv(locate(data,"gtco_e12c_265_real_templates.csv"),dtype={"source_id":"string"})
    val=pd.read_csv(locate(data,"gtco_e12c_validation_sample_3000.csv"),dtype={"source_id":"string"})
    if len(templates)!=265 or len(val)!=3000:
        raise RuntimeError(f"Unexpected template/validation sizes: {len(templates)}, {len(val)}")

    host_path=args.host_flags
    if host_path is None:
        cands=[out/"hostcut_flags.csv.gz", data/"gtco_e17e_hostcut_flags_v2.csv.gz"]
        host_path=next((p for p in cands if p.exists()),None)
    if host_path is None or not host_path.exists():
        raise FileNotFoundError("No host flags found. Run 02_hostcuts_source_level.py first or supply --host-flags.")
    host=pd.read_csv(host_path,dtype={"source_id":"string"})
    if "pass_hostcuts_w1000" not in host.columns:
        raise RuntimeError("Host flags lack pass_hostcuts_w1000")
    hp=(val[["source_id"]].merge(host[["source_id","pass_hostcuts_w1000"]],on="source_id",how="left")
        ["pass_hostcuts_w1000"].fillna(False).to_numpy(bool))

    # Build the 220,745-model library in absolute 10-band magnitude space.
    blocks=[]; meta=[]
    for T in T_LIBRARY:
        for g in G_LIBRARY:
            blocks.append(ds_absolute_mags(templates,T,g).astype(np.float32))
            meta.extend((T,g,i) for i in range(len(templates)))
    library=np.vstack(blocks)
    if library.shape!=(220745,10):
        raise RuntimeError(f"Library shape mismatch: {library.shape}")
    tree=cKDTree(library)

    Fbase,sigmaF=baseline_flux_and_sigma(val)
    dm=5*np.log10(val["distance_invparallax_pc"].to_numpy(float)/10.0)
    rng=np.random.default_rng(SEED)

    cell_rows=[]; case_rows=[]
    for T in T_TRUTH:
        for g in G_TRUTH:
            Mtrue=ds_absolute_mags(val,T,g)
            mtrue=Mtrue+dm[:,None]
            Ftrue=ZERO_JY[None,:]*10**(-0.4*mtrue)
            ratio=Ftrue/Fbase
            snr=expected_snr(val,ratio)
            expected_gate=(
                np.isfinite(mtrue).all(axis=1) &
                (mtrue[:,0] <= 21.0) &
                (snr[:,3:6] > 2.0).all(axis=1) &
                (snr[:,8:10] > 3.5).all(axis=1)
            )

            # Frozen reconstruction perturbs in linear flux, not magnitude.
            Fobs=Ftrue+rng.normal(size=Ftrue.shape)*sigmaF
            positive=(Fobs>0).all(axis=1)
            survival=expected_gate & positive

            mobs=np.full_like(Fobs,np.nan)
            mask=Fobs>0
            zpb=np.broadcast_to(ZERO_JY,Fobs.shape)
            mobs[mask]=-2.5*np.log10(Fobs[mask]/zpb[mask])
            Mobs=mobs-dm[:,None]

            rmse=np.full(len(val),np.inf)
            best_index=np.full(len(val),-1,dtype=int)
            q=survival & np.isfinite(Mobs).all(axis=1)
            if q.any():
                dist,idx=tree.query(Mobs[q],k=1,workers=-1)
                rmse[q]=dist/np.sqrt(10.0)
                best_index[q]=idx
            recovered=survival & (rmse<=0.2)
            joint=recovered & hp

            cell_rows.append({
                "T_DS_K":T,"gamma":g,"N":len(val),
                "catalog_survival":float(survival.mean()),
                "photometric_recovery_all":float(recovered.mean()),
                "host_pass_all":float(hp.mean()),
                "joint_photometry_and_host_pass":float(joint.mean()),
                "factorized_joint_estimate":float(recovered.mean()*hp.mean()),
                "joint_over_factorized":float(joint.mean()/(recovered.mean()*hp.mean())) if recovered.mean()>0 else np.nan,
                "median_best_RMSE_mag_survivors":float(np.median(rmse[survival])) if survival.any() else np.nan,
            })
            # Case-level audit is useful for exact source-level joins downstream.
            for i,sid in enumerate(val["source_id"].astype(str)):
                case_rows.append((sid,T,g,bool(survival[i]),bool(recovered[i]),bool(hp[i]),bool(joint[i]),float(rmse[i]),int(best_index[i])))

    surface=pd.DataFrame(cell_rows)
    cases=pd.DataFrame(case_rows,columns=["source_id","T_DS_K","gamma","catalog_survival","photometric_recovered","host_pass_w1000","joint_recovered_host","best_RMSE_mag","best_library_index"])

    summary=pd.DataFrame([{
        "N_templates":len(templates),"N_library_models":len(library),"N_validation":len(val),
        "N_truth_cells":len(surface),"seed":SEED,
        "mean_catalog_survival":surface.catalog_survival.mean(),
        "mean_photometric_recovery":surface.photometric_recovery_all.mean(),
        "host_pass_fraction":hp.mean(),
        "mean_joint_photometry_plus_host":surface.joint_photometry_and_host_pass.mean(),
        "factorized_mean_product":surface.factorized_joint_estimate.mean(),
        "mean_joint_over_factorized_ratio":surface.joint_photometry_and_host_pass.mean()/surface.factorized_joint_estimate.mean(),
    }])

    # Compare to frozen headline values if available. This comparison is not used to create the result.
    frozen={
        "mean_catalog_survival":0.9863086419753088,
        "mean_photometric_recovery":0.9105432098765432,
        "host_pass_fraction":0.442,
        "mean_joint_photometry_plus_host":0.4142222222222222,
        "factorized_mean_product":0.4024600987654321,
    }
    audit=[]
    for k,v in frozen.items():
        got=float(summary.iloc[0][k])
        audit.append({"metric":k,"reconstructed":got,"frozen_reference":v,"absolute_difference":abs(got-v)})
    audit=pd.DataFrame(audit)

    surface.to_csv(out/"e12c_e17f_reconstructed_surface.csv",index=False)
    cases.to_csv(out/"e12c_e17f_reconstructed_cases.csv.gz",index=False,compression="gzip")
    summary.to_csv(out/"e12c_e17f_reconstructed_summary.csv",index=False)
    audit.to_csv(out/"e12c_e17f_reconstruction_audit.csv",index=False)
    (out/"e12c_e17f_reconstruction_constants.json").write_text(json.dumps({
        "seed":SEED,"bands":BANDS,"lambda_um":LAMBDA_UM.tolist(),"zero_jy":ZERO_JY.tolist(),
        "T_library":T_LIBRARY.tolist(),"gamma_library":G_LIBRARY.tolist(),
        "T_truth":T_TRUTH.tolist(),"gamma_truth":G_TRUTH.tolist(),
        "catalog_gate":{"G_max":21.0,"JHK_expected_snr_min":2.0,"W3W4_expected_snr_min":3.5,"realized_flux_positive_all_10bands":True},
        "recognition":{"metric":"unweighted 10-band magnitude RMSE to nearest library model","threshold_mag":0.2}
    },indent=2),encoding="utf-8")

    print(summary.to_string(index=False))
    print("\nAudit against frozen headline values:")
    print(audit.to_string(index=False))
    if audit.absolute_difference.max()>5e-4:
        raise SystemExit("Reconstruction differs from a frozen headline metric by >5e-4")
    print("\nPASS: E12c/E17f standalone reconstruction matches frozen headline metrics within 5e-4.")

if __name__=="__main__":
    main()
