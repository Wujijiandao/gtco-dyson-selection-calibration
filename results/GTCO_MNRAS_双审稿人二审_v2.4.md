# GTCO / MNRAS 双审稿人模拟二审报告 v2.4

> 模拟对象：`GTCO_MNRAS_submission_draft_v2_4_PREZENODO`  
> 稿件标题：*From Dyson-sphere candidates to population constraints: calibrating selection and conditional real-image response in Gaia--2MASS--WISE searches*  
> 性质：投稿前敌对式二审，不是实际期刊审稿意见。  
> 二审目标：不重新发明批评点，而是逐项检查第一轮 Major Revision 是否真正解决；只有发现新的实质性科学硬伤才重新升级为 Major。

---

# 一、模拟编辑二审总判定

第一轮模拟审稿得到：

- Referee A（统计 / selection function）：**Major Revision**；
- Referee B（WISE / technosignature）：**Major Revision，接近 Reject-and-Resubmit 边界**。

第一轮的四个 P0 问题是：

1. WISE template saturation / W2 correction 语义；
2. baseline host metadata 被过度解释成 counterfactual host completeness；
3. 注入后仍沿用 baseline photometric errors；
4. matched injection/scoring PSF 形成 image-response 的结构性自洽。

v2.4 已经逐项用真实重跑或 claim 降格处理，并额外补上 WISE broad-band colour-correction sensitivity 与 validation saturation conditioning。

**模拟编辑二审决定：**

\[
\boxed{\textbf{Minor Revision / publishable after minor editorial completion}}
\]

这里的 “Minor Revision” 主要不是要求再做新的科学实验，而是完成永久 DOI、软件引用、利益冲突/资助声明确认，以及最终提交元数据。

本轮没有发现新的 P0 级科学 blocker。

---

# 二、Referee A 二审：selection-function / statistics

## Recommendation

\[
\boxed{\textbf{Minor Revision}}
\]

我认为作者已经实质回应了第一轮的主要统计学意见。稿件现在对“测到了什么”和“没有测到什么”的区分明显更清楚，不再把部分响应函数包装成 end-to-end completeness。

## A1. baseline host gate 不是 counterfactual host completeness

### 第一轮问题

原稿容易让 0.414222 被理解为：

\[
P(\mathrm{photometric+host\ pass}\mid \mathrm{injected\ DS}).
\]

但 RUWE、Gaia classification probability、\(G_{\rm var}\)、Hα availability 等仍来自原始观测 catalogue row，并没有随 Dyson phenotype 重新生成。

### 二审状态：**Resolved**

v2.4 已明确把该量定义为：

> injected photometric response 与 **baseline observed host gate** 的 same-source coupling。

并明确声明它不是：

\[
P(\mathrm{host\ pass}\mid \mathrm{injected\ DS}).
\]

这是正确的修正。完整 counterfactual host completeness 仍作为未测项保留，不影响当前方法学论文成立。

---

## A2. 0.414 与 0.402 的差别有没有统计分辨率？

### 第一轮问题

固定 random seed 只能证明计算可复现，不能证明：

\[
\Delta C=C_{\rm same-source}-C_{\rm factorized}
\]

相对于 host sampling uncertainty 显著非零。

### 二审状态：**Resolved**

作者新增 20,000 次 source-ID cluster bootstrap：

\[
C_{\rm coupling}=0.414222,
\]

\[
\Delta C=0.011765,
\]

并得到：

\[
\boxed{95\%\ {\rm CI}(\Delta C)=[0.008859,\,0.014732]}.
\]

在冻结的 3,000-host validation population 下，该 source-level dependence 已被统计分辨。

我同意作者仍将其描述为 coupling diagnostic，而非新的普适 selection law。

---

## A3. baseline error 不是完整 heteroscedastic forward model

### 第一轮问题

注入后 MIR flux 增强、optical flux 变暗，但原始版本仍使用 baseline uncertainty，误差没有显式随 counterfactual flux 改变。

### 二审状态：**Resolved for the present claim boundary**

新增 conservative bracket：

\[
\sigma_{\rm cf}
=\sigma_0\sqrt{\max(1,F_{\rm cf}/F_0)}.
\]

baseline recovery：

\[
0.910537,
\]

conservative bracket：

\[
\boxed{0.910309}.
\]

变化仅约：

\[
-2.28\times10^{-4}.
\]

因此 0.91 这一条件响应对这一合理的 flux-dependent noise stress test 稳定。作者也没有把该 bracket 冒充完整 detector likelihood，表述恰当。

---

## A4. host-level Clopper--Pearson 语义

### 第一轮问题

23 hosts 的 valid phenotype cells 数量并不完全相同，因此简单 common-\(p\) Bernoulli interpretation 过强。

### 二审状态：**Substantially resolved**

v2.4 已把 W3 lower bound 明确限制成：

> 23 个 tested baseline-clean hosts 在 stated challenge family 下的 host-level summary。

重复 \((T,\gamma)\) cells 不再被解释为独立 Bernoulli trials，也不外推到 arbitrary WISE environments。

这足以支持当前窄结论。若未来要估计 population morphology completeness，应使用 representative host sampling 和 hierarchical/cluster model；当前论文已经这样表述。

---

## A5. 0.910 是否仍容易被误读为 survey completeness？

### 二审状态：**Resolved**

稿件已经统一使用：

\[
\boxed{\text{conditional SED-recognition response}}
\]

并单独暴露：

- 250,909 CMD-MS parent；
- 72,716 strict ten-band analysis-supporting pool（28.98%）；
- 3,000 validation sample；
- 54-cell arithmetic grid average。

正文明确说明 0.910 不是 all-parent availability、不是 final Hephaistos-II operator completeness，也不是 population-marginalized scalar。

---

## Referee A 剩余 Minor comments

1. Zenodo DOI 应在提交前进入 Data Availability，并最好作为 software citation 加入 References。
2. 最终 repository release 应冻结与提交稿完全一致的代码/结果，而不是 main branch 的可变状态。
3. 利益冲突与 funding statement 需要作者本人确认，不能由分析流程代填。
4. 论文中的 bootstrap interval 是 conditional on the frozen validation design；现在的措辞已经基本反映这一点，无需新增实验。

### Referee A 最终意见

论文已从第一轮的“统计定义尚不完整”提升为：

\[
\boxed{\text{selection semantics are adequately bounded for publication}}.
\]

我不再要求新的 Major scientific revision。

---

# 三、Referee B 二审：WISE / infrared / technosignature

## Recommendation

\[
\boxed{\textbf{Minor Revision / Accept after minor corrections}}
\]

第一轮我最担心的是 image experiment 的 matched-PSF self-consistency、template saturation semantics 与 broad-band WISE response。作者没有用文字防御，而是进行了会真正推翻旧结论的 stress tests。这显著提高了我对稿件的信任。

---

## B1. injection PSF 与 scoring PSF 同构导致“自证”

### 第一轮问题

原 matched-PSF 实验中：

\[
I_{\rm inj}=I_{\rm real}+\Delta A P,
\]

而 morphology score 又相对于同一个 \(P\) 计算，因此“增加 point-like flux 后更像 point source”部分是结构性预期。

### 二审状态：**Resolved, and the scientific conclusion changed appropriately**

作者新增：

- disjoint empirical injection/scoring PSF；
- PSF broadening；
- 0.1/0.25/0.5 Atlas-pixel injection offsets。

W3：所有 tested challenges 下 grid-cell retention 均保持 1.000。

W4：

- matched：1.000；
- mild blur：0.451342；
- moderate blur：0.171141；
- 0.1-pixel offset：0.362416；
- disjoint empirical-PSF split：约 0.030。

作者因此**主动删除**旧的 robust W4 / W3+W4 completeness headline，只保留 W3 tested-challenge lower bound，并将 W4 解释为 PSF/operator-sensitive result。

这是我期望看到的正确审稿响应。

---

## B2. 代表性环境项 \(C_{\rm environment}\) 没测

### 第一轮问题

24 个 fields 被刻意选为 bright, low-confusion，因此不能代表真正的 WISE confusion/background population。

### 二审状态：**Accepted scope limitation**

v2.4 已不再把 image stage 压缩成 survey-wide scalar，而写成：

\[
C_{\rm image}
=P(E)P(L\mid E)P(M\mid E,L,\mathcal O_{\rm image}).
\]

其中 representative \(P(E)\) 明确未测。

近期 Hephaistos follow-up 恰恰显示 line-of-sight background galaxies 是实际主导问题之一，所以把环境项独立出来具有明确的观测意义。

我不再认为必须在本稿中完成 representative \(P(E)\) 才能发表；它可以合理成为下一篇/下一阶段实验。

---

## B3. 265-template saturation / W2 correction semantics

### 第一轮问题

冻结模板中存在大量 W1/W2 nominal-onset-bright sources，与 Hephaistos-II Appendix A 对 saturation/W2 correction 的描述不能完全对应。

### 二审状态：**Resolved as an explicitly bounded emulation**

作者现在公开报告：

- frozen baseline：0.910537；
- frozen templates + W2 correction：0.911086；
- correction-aware reselected templates：0.916605；
- literal four-band onset hard-cut stress test：0.696488。

同时指出最后一种硬切会把 bright \(M_G\) template coverage 大幅删除，因此不能无条件视为原 pipeline 的正确重建。

这个处理比假装 exact reproduction 更合理。

---

## B4. validation sample 里 W1/W2 nominal saturation

### 二审状态：**Resolved as a conditioning sensitivity**

3,000 validation stars 中：

- W1 brighter than nominal onset：1542 / 3000 = 51.4%；
- W2：436 / 3000 = 14.53%；
- W3：3 / 3000 = 0.1%；
- W4：0。

将 validation 限制到四个 WISE bands 都比 nominal onset 更暗的 1,458 stars 后：

\[
C_{\rm phot}=0.947213.
\]

作者正确地没有把 0.947 当作“修正后的真值”，因为这个 cut 同时改变 luminosity/host distribution；它被报告为 conditioning sensitivity。这一表述我接受。

---

## B5. WISE broad-band colour correction / passband concern

### 第一轮问题

100--700 K blackbody 在 W3/W4 宽波段内并非平谱，单纯在 reference wavelength 评价 \(B_\nu\) 可能产生偏差，尤其 W3。

### 二审状态：**Resolved sufficiently for this emulation paper**

作者使用公开 WISE blackbody colour-correction system 做完整 220,745-model / 54-cell rerun。

官方表中 100-K blackbody 的 W3 colour-correction factor 高达：

\[
f_c({\rm W3},100\,K)=2.6588.
\]

尽管单波段修正很大，完整 grid-average 结果为：

- frozen reference wavelengths + WISE colour correction：0.912309；
- WISE isophotal wavelengths + colour correction：
  \[
  \boxed{0.911568}.
  \]

相对 baseline 0.910537 仅改变约 0.001。

这不是 full RSR integration，但已经直接检验了我第一轮担心的“宽波段校正会不会推翻 0.91”问题。答案是在当前 response statistic 下不会。

因此我不再要求为了本稿重建完整 proprietary/full-pipeline synthetic photometry。

---

## B6. W4 image-sample quality信息不足

### 二审状态：**Resolved**

稿件现在给出：

- W3 = 4.46--8.48 mag；
- W4 = 4.41--7.94 mag；
- median approximate S/N ≈ 63.9（W3）和 11.3（W4）；
- median central coverage ≈ 17.9 和 19.2 frames。

这足以让读者理解为何 W4 PSF/operator uncertainty 比 W3 更值得警惕。

---

## Referee B 剩余 Minor comments

1. W3 的稳健性必须继续表述为“tested challenge family on clean unsaturated hosts”，不能升级为 survey-wide W3 completeness；现稿已经如此。
2. W4 mismatch table 应继续明确是 **grid-cell retention**，而不是数百个独立 astronomical trials；v2.4 已修正。
3. Ren et al. 2026 已被 MNRAS 接收，应写作 `MNRAS, in press`；Korn et al. 2026 与 Zackrisson et al. 2026 仍应给出 arXiv IDs。v2.4 已更新。
4. 未来真正值得做的是 representative environment calibration 和 source-specific W4 PSF，不建议为了当前投稿再无止境追加 image stress tests。

### Referee B 最终意见

第一轮我处于 Major / Reject-and-Resubmit 边界；v2.4 后我将意见降为：

\[
\boxed{\textbf{Minor Revision / Accept after minor corrections}}.
\]

关键原因不是作者“证明旧结论正确”，而是当 W4 旧结论经不起独立挑战时，作者让论文结论随证据改变。

---

# 四、模拟 Scientific Editor 二审决定

综合两位 referee：

| 项目 | 第一轮 | v2.4 二审 |
|---|---|---|
| Host counterfactual semantics | Major | Resolved by claim correction |
| 0.414 vs 0.402 uncertainty | Major | Resolved by source-cluster bootstrap |
| Noise model | Major | Robustness quantified |
| Template saturation/W2 | Major | Explicit sensitivity / bounded emulation |
| WISE broad-band response | Major/strong concern | Quantified; 0.91 stable |
| PSF self-consistency | Major | Resolved; W4 conclusion downgraded |
| Representative environment | Major significance concern | Accepted scope limitation |
| Reproducibility | Strong | Stronger; standalone + hardening scripts |
| Current recommendation | Major Revision | **Minor Revision** |

因此模拟编辑决定为：

\[
\boxed{\textbf{MINOR REVISION}}
\]

或者在部分编辑体系中可等价理解为：

> scientifically acceptable in principle, pending final technical/editorial completion.

---

# 五、二审后仍然不能声称的东西

v2.4 变强的一个原因，是它明确不再试图回答以下尚未测量的问题：

1. 全体恒星的 Dyson-sphere occurrence rate；
2. Hephaistos-II seven-candidate final operator 的 end-to-end completeness；
3. counterfactual Gaia/WISE host-quality completeness；
4. representative WISE field-environment completeness；
5. robust W4 morphology-completeness scalar；
6. arbitrary technosphere spectra 的 completeness；
7. 100-pc calibration 对 300-pc final-candidate population 的无条件外推。

这些现在属于**边界清晰的 future work**，而不是 hidden methodological defects。

---

# 六、提交前只剩的真正待办

## 必须完成，但不需要新科学实验

1. 将 v2.4 hardening scripts/results/manuscript 同步到 GitHub；
2. 冻结 GitHub release `v1.0.0-submission`；
3. Zenodo 生成永久 DOI；
4. DOI 回填 Data Availability、README、CITATION.cff，并增加正式 software citation；
5. 作者本人确认 conflict-of-interest 状态；
6. 作者本人确认 funding 状态；
7. 最终 ScholarOne-generated PDF 人工检查。

## 不建议现在继续增加的实验

- 不为追求“绝对无漏洞”而继续增加 E18；
- 不为了当前论文强行构造 counterfactual Gaia pipeline；
- 不为了让 W4 数字变漂亮而继续调 morphology operator；
- 不把 representative environment calibration 塞进当前稿件导致 scope 再次膨胀。

---

# 七、最终二审评价

当前稿件已经从：

\[
\text{interesting but vulnerable methods manuscript}
\]

经过第一轮 Major Revision hardening，转变为：

\[
\boxed{\textbf{defensible and publishable MNRAS methods submission candidate}}.
\]

这不等于“保证 MNRAS 接收”。真实编辑仍可能对 significance 作主观判断，也可能要求 additional validation。

但从目前能主动识别的技术一致性、统计语义、WISE photometry、image-operator robustness 和 reproducibility 风险看，**已经没有发现需要在投稿前继续阻断提交的 P0 科学硬伤**。

下一阶段应从“继续研究”切换到“冻结、引用、提交”。
