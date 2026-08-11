# REFEREE-HARDENING RESPONSE — v2.3

This internal pre-submission note records how the manuscript changed after adversarial simulated peer review.

## Baseline host metadata are not counterfactual host completeness
Accepted. The manuscript now calls the quantity a baseline-observed host gate. The 0.414222 result demonstrates source-level dependence between injected SED recovery and observed host state; it is not relabelled as `P(host pass | injected DS)`.

## 0.414 versus 0.402 needs uncertainty
Accepted and tested. Source-ID cluster bootstrap, 20,000 replicates:

\[
\Delta C = 0.011765,\qquad 95\%=[0.008859,0.014732].
\]

## Fixed baseline errors are not a complete heteroscedastic forward model
Accepted. A conservative bracket

\[
\sigma_{\rm cf}=\sigma_0\sqrt{\max(1,F_{\rm cf}/F_0)}
\]

gives recovery 0.910309 versus 0.910537 baseline. More extreme noise prescriptions are retained only as stress bounds.

## Template saturation semantics differ from the intended emulation
Accepted. W2-correction-aware variants give 0.911–0.917 recovery. A literal four-band saturation-onset cut gives 0.696 but removes the bright end of the intended template sequence; it is treated as a severe stress test.

## Matched injection/scoring PSF partly self-validates image retention
Accepted and decisive. The injection PSF was altered while the LOHO scoring operator was held fixed.

W3 is robust across the tested challenge family. W4 is not. The manuscript removes the earlier robust W4/joint lower-bound headline and reports W4 as PSF-model dependent.

## Representative environment completeness remains unmeasured
Accepted as a scope limitation. The paper writes the image stage conditionally as

\[
C_{\rm image}=P(E)P(L\mid E)P(M\mid E,L,\mathcal O_{\rm image}),
\]

rather than assigning a survey-wide image-completeness scalar.

## Current position
The hardening work changed the scientific conclusion rather than merely defending the old one. The revised image result is narrower and more defensible:
- robust tested W3 conditional morphology response;
- W4 PSF/operator sensitivity;
- representative environment completeness remains future work.
