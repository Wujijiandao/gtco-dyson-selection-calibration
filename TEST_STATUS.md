# TEST STATUS — v2.3 referee-hardened

Catalogue baseline:
- survival 0.986302
- conditional SED recovery 0.910537
- baseline observed host pass 0.442
- same-source coupling 0.414222
- factorized estimate 0.402457

Source-cluster bootstrap (20,000):
- coupling 95% [0.397740, 0.431167]
- joint-minus-factorized 0.011765, 95% [0.008859, 0.014732]

Template/W2 sensitivity:
- current templates + W2 correction 0.911086
- correction-aware variant 0.916605
- literal four-band hard-onset stress test 0.696488

Noise sensitivity:
- baseline 0.910537
- conservative floor+Poisson 0.910309
- Poisson-scaled extreme 0.955685
- constant-fractional extreme 0.701735

W3 PSF challenge:
- matched / mild blur / moderate blur / 0.1 / 0.25 / 0.5-pixel offsets / disjoint split: all 1.000

W4 PSF challenge:
- matched 1.000
- mild blur 0.451342
- moderate blur 0.171141
- 0.1-pixel offset 0.362416
- 0.25-pixel offset 0.135906
- 0.5-pixel offset 0.041946
- disjoint split ~0.030

Manuscript:
- 11 pages
- 28 cited references
- ~245-word abstract
- PDF preflight and visual render QA passed
