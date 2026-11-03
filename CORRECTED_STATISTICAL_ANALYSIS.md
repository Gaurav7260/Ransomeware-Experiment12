# CanarySentinel — Corrected Statistical Analysis Report
**Document ID:** CS-AUDIT-STAT-2026-CORR-01  
**Author:** Independent Experimental Research & Statistical Analysis Team  
**Evaluation Target:** Canary-Triggered Behavioral Corroboration for Early Ransomware Detection  
**Status:** FINAL VERIFIED & RECONCILED  
**Date:** November 2, 2026  

---

## 1. Executive Summary & Audit Context

This document provides the **corrected, rigorous statistical analysis** of detection latency, detection accuracy, and damage reduction for the CanarySentinel research evaluation.

### Methodological Correction
In previous preliminary reports, detection latency was evaluated across a pooled cohort of all generated alerts ($n=30$ for Baseline, $n=20$ for Canary-Only, $n=10$ for Hybrid). That pooled analysis improperly aggregated **true positive attack detections** with **benign false positive alarms** (specifically, 10 compiler build / bulk renaming false positives for Baseline that triggered at $pprox 271$ ms, and 10 benign file cleanup false positives for Canary-Only that triggered at $pprox 13.5$ ms).

**Audit Correction Implemented:**
1. **Strict Decoupling:** True positive attack detection latency is evaluated **strictly on attack scenarios** (S5 and S6). Benign false positive latencies are reported in a separate dedicated section.
2. **Matched Scenario S5 Comparison:** Direct head-to-head comparison across all three detection configurations on the exact same workload ($n=10$ repetitions each) where canaries were interacted with.
3. **Formal Statistical Testing:** For every comparison, independent two-sample tests (Welch's $t$-test with Satterthwaite degrees of freedom and Mann-Whitney $U$ rank-sum test) are reported with exact test statistics, two-tailed $p$-values, effect sizes (Cohen's $d$), and 95% confidence intervals. Because trial runs across detector configurations carry independent unique trial IDs and random seeds, pairing trials by row order is statistically invalid and not assumed.

---

## 2. Experimental Design & Population Definitions

The benchmark evaluation dataset comprises $N = 180$ controlled trials executed in the isolated sandbox environment:
- **Configurations ($k=3$):**
  - **Configuration A (Baseline Behavioral):** Monitors file modification velocity, entropy, and burst thresholds without decoy awareness.
  - **Configuration B (Canary-Only Decoy):** Pure decoy tripwires; triggers immediate containment upon any modification or rename of a canary file.
  - **Configuration C (Hybrid Corroborated):** Corroborates decoy interactions with short-window contextual filesystem velocity to eliminate isolated benign touches.
- **Workload Scenarios ($m=6$):**
  - **B1 (Normal File Editing):** Single document modification and rename ($n=10$ per detector, Ground Truth: Benign).
  - **B2 (Bulk File Copying):** Rapid creation of multiple backup copies ($n=10$ per detector, Ground Truth: Benign).
  - **B3 (Canary Touch Benign):** Routine maintenance script / administrative cleanup touching a canary decoy without subsequent velocity ($n=10$ per detector, Ground Truth: Benign).
  - **B4 (Bulk Renaming / Build):** Software build process rapidly renaming files ($n=10$ per detector, Ground Truth: Benign).
  - **S5 (Fast Sequential Ransomware):** Rapid burst encryption traversing directory structure and touching decoy files ($n=10$ per detector, Ground Truth: Suspicious / Attack).
  - **S6 (Targeted / Evasive Ransomware):** Targeted encryption specifically avoiding decoy names/locations ($n=10$ per detector, Ground Truth: Suspicious / Attack).

---

## 3. Matched Scenario S5 Latency Analysis ($n=10$ per Detector)

Scenario S5 represents standard ransomware that traverses directories and interacts with deployed canary decoys. All three detectors successfully detected S5 in 100% of trials ($10/10$ true positives each).

### 3.1 Raw Latency Data (ms)

The 10 repetitions of Scenario S5 (`Canary Touch + Rapid Bulk Modifications`) across all three detectors from `RAW_EXPERIMENT_DATA_180.csv` yielded the following verified latency values:

| Repetition | Baseline Trial ID | Baseline Latency (ms) | Canary-Only Trial ID | Canary-Only Latency (ms) | Hybrid Trial ID | Hybrid Latency (ms) |
|:---:|---|:---:|---|:---:|---|:---:|
| 1 | `baseline_canary_plus_rapid_bulk_eb4ab4` | 29.22 | `canary_only_canary_plus_rapid_bulk_0891a8` | 27.54 | `hybrid_canary_plus_rapid_bulk_bd9f32` | 25.89 |
| 2 | `baseline_canary_plus_rapid_bulk_294735` | 27.86 | `canary_only_canary_plus_rapid_bulk_3a2ab8` | 26.36 | `hybrid_canary_plus_rapid_bulk_6cbf50` | 22.86 |
| 3 | `baseline_canary_plus_rapid_bulk_18e328` | 20.72 | `canary_only_canary_plus_rapid_bulk_eaba57` | 26.63 | `hybrid_canary_plus_rapid_bulk_bd3aa1` | 25.67 |
| 4 | `baseline_canary_plus_rapid_bulk_9df2c9` | 29.08 | `canary_only_canary_plus_rapid_bulk_856948` | 25.90 | `hybrid_canary_plus_rapid_bulk_0df6f6` | 46.85 |
| 5 | `baseline_canary_plus_rapid_bulk_756ec5` | 27.30 | `canary_only_canary_plus_rapid_bulk_ba8bd0` | 19.83 | `hybrid_canary_plus_rapid_bulk_6c124f` | 26.11 |
| 6 | `baseline_canary_plus_rapid_bulk_9fddd0` | 18.85 | `canary_only_canary_plus_rapid_bulk_d9057a` | 21.69 | `hybrid_canary_plus_rapid_bulk_faf2ea` | 28.75 |
| 7 | `baseline_canary_plus_rapid_bulk_664ee6` | 25.95 | `canary_only_canary_plus_rapid_bulk_c345d3` | 15.48 | `hybrid_canary_plus_rapid_bulk_054323` | 16.93 |
| 8 | `baseline_canary_plus_rapid_bulk_cececf` | 24.66 | `canary_only_canary_plus_rapid_bulk_82557b` | 38.10 | `hybrid_canary_plus_rapid_bulk_43b2a0` | 15.76 |
| 9 | `baseline_canary_plus_rapid_bulk_cde394` | 27.19 | `canary_only_canary_plus_rapid_bulk_744251` | 15.85 | `hybrid_canary_plus_rapid_bulk_10bf4a` | 25.63 |
| 10 | `baseline_canary_plus_rapid_bulk_3ab3f6` | 27.15 | `canary_only_canary_plus_rapid_bulk_6d56bf` | 25.46 | `hybrid_canary_plus_rapid_bulk_846c70` | 26.61 |

*Note: Each detector run has an independent unique trial ID and fresh random sandbox jitter. Because trials were not linked by a common pairing identifier, pairing trials by row order is statistically invalid. All comparisons below are conducted as independent two-sample tests.*

### 3.2 Summary Statistics for Scenario S5
*(Quantile Convention: Primary IQR values are computed using standard linear interpolation [Type 7, default in NumPy, SciPy, and Pandas]. For complete methodological transparency, values under the nearest-rank / Tukey's hinges convention are also explicitly provided in brackets.)*

- **Baseline Behavioral:**
  - Sample Size: $n = 10$
  - Mean $\pm$ SD: $25.80 \pm 3.47$ ms
  - Median: $27.17$ ms
  - Interquartile Range (IQR): **$2.74$ ms** ($Q_1 = 24.98$ ms, $Q_3 = 27.72$ ms via linear interpolation; or $\text{IQR} = \mathbf{3.20\text{ ms}}$ via nearest-rank where $Q_1 = 24.66$ ms, $Q_3 = 27.86$ ms)
  - 95% Confidence Interval: $[23.32, 28.28]$ ms
- **Canary-Only Decoy:**
  - Sample Size: $n = 10$
  - Mean $\pm$ SD: $24.28 \pm 6.59$ ms
  - Median: $25.68$ ms
  - Interquartile Range (IQR): **$6.27$ ms** ($Q_1 = 20.30$ ms, $Q_3 = 26.56$ ms via linear interpolation; or $\text{IQR} = \mathbf{6.80\text{ ms}}$ via nearest-rank where $Q_1 = 19.83$ ms, $Q_3 = 26.63$ ms)
  - 95% Confidence Interval: $[19.57, 29.00]$ ms
- **Hybrid Corroborated:**
  - Sample Size: $n = 10$
  - Mean $\pm$ SD: $26.10 \pm 8.43$ ms
  - Median: $25.78$ ms
  - Interquartile Range (IQR): **$2.93$ ms** ($Q_1 = 23.55$ ms, $Q_3 = 26.49$ ms via linear interpolation; or $\text{IQR} = \mathbf{3.75\text{ ms}}$ via nearest-rank where $Q_1 = 22.86$ ms, $Q_3 = 26.61$ ms)
  - 95% Confidence Interval: $[20.07, 32.14]$ ms

### 3.3 Comparative Hypothesis Testing on Scenario S5

#### Comparison 1: Hybrid vs Baseline Behavioral
- **Research Question:** Does the Hybrid corroboration pipeline introduce a statistically significant latency overhead compared to pure baseline behavioral detection on attacks touching decoys?
- **Baseline Behavioral S5 Latency ($n=10$):** $25.80 \pm 3.47$ ms ($95\%$ CI: $[23.32, 28.28]$ ms)
- **Hybrid Corroborated S5 Latency ($n=10$):** $26.10 \pm 8.43$ ms ($95\%$ CI: $[20.07, 32.13]$ ms)
- **Mean Difference:** $+0.30$ ms (Hybrid is $0.30$ ms slower on S5)
- **Welch's Two-Sample $t$-test (Independent):** $t(11.95) = 0.1067$, $p = 0.9168$
- **Mann-Whitney $U$ test (Non-parametric Independent):** $U = 37.0$, $p = 0.3447$
- **Standardized Effect Size (Cohen's $d$):** $d = 0.0477$ (Negligible effect)
- **Interpretation:** The mean latency difference between Hybrid and Baseline on matched S5 is $+0.30$ ms. Both independent parametric and non-parametric tests yield $p > 0.34$. There is **no statistically significant S5 latency difference detected** between Hybrid and Baseline on matched Scenario S5 attacks. **Equivalence was not established**; formal equivalence testing (such as two one-sided tests [TOST] within pre-specified equivalence bounds) was not performed, and confidence intervals $[-4.98, 5.58]$ ms are consistent with small differences in either direction.

#### Comparison 2: Hybrid vs Canary-Only Decoy
- **Research Question:** Does evaluating contextual filesystem burst behavior after a canary touch impose a significant time penalty relative to an instantaneous tripwire?
- **Canary-Only Decoy S5 Latency ($n=10$):** $24.28 \pm 6.59$ ms ($95\%$ CI: $[19.56, 28.99]$ ms)
- **Hybrid Corroborated S5 Latency ($n=10$):** $26.10 \pm 8.43$ ms ($95\%$ CI: $[20.07, 32.13]$ ms)
- **Mean Difference:** $+1.82$ ms (Hybrid context corroboration delay)
- **Welch's Two-Sample $t$-test (Independent):** $t(17.03) = 0.5379$, $p = 0.5976$
- **Mann-Whitney $U$ test (Non-parametric Independent):** $U = 54.0$, $p = 0.7913$
- **Standardized Effect Size (Cohen's $d$):** $d = 0.2406$ (Small, non-significant)
- **Interpretation:** Hybrid corroboration requires $+1.82$ ms on average compared to pure Canary-Only tripwires ($26.10$ ms vs $24.28$ ms). With $p > 0.59$, no statistically significant S5 latency difference was detected; equivalence was not established.

---

## 4. Overall True Positive Attack Detection Latency & Scenario Composition Asymmetry

Across all attack scenarios (S5 and S6), detection performance diverges:
- **Baseline Behavioral:** Detects both S5 ($n=10$) and S6 ($n=10$) for a total of $n=20$ true positive detections.
  - S5 Latency ($n=10$): $25.80 \pm 3.47$ ms
  - S6 Latency ($n=10$): $144.05 \pm 5.17$ ms (requires accumulating sufficient velocity across user files)
  - Combined Baseline Attack TP Latency ($n=20$): Mean $= 84.92 \pm 60.86$ ms (Median: $84.92$ ms, 95% CI: $[58.25, 111.59]$ ms)
- **Canary-Only Decoy:** Detects only S5 ($n=10$, latency: $24.28 \pm 6.59$ ms). S6 does not touch canaries and is completely missed ($10/10$ False Negatives).
- **Hybrid Corroborated:** Detects only S5 ($n=10$, latency: $26.10 \pm 8.43$ ms). S6 does not touch canaries and is completely missed ($10/10$ False Negatives).

### 4.1 Methodological Caveat: Scenario Composition Asymmetry
Comparing the pooled Baseline attack true positives ($n=20$, covering both S5 and S6, mean $84.92$ ms) to Hybrid true positives ($n=10$, covering S5 only, mean $26.10$ ms) does not constitute a valid proof of superior detector speed. 

- **Why the Pooled Comparison is Asymmetric:** Baseline's higher mean latency arises because it successfully detected the evasive S6 attacks (requiring $144.05$ ms of volume accumulation), whereas Hybrid completely missed S6 ($0\%$ recall).
- **The Valid Apples-to-Apples Comparison:** When compared on matched Scenario S5 attacks where both detectors triggered, Baseline ($25.80$ ms) and Hybrid ($26.10$ ms) show no statistically significant difference ($t = 0.1067, p = 0.9168$).
- Hybrid's lower overall mean reflects the omission of difficult, slow-to-detect attacks rather than faster algorithmic speed.

---

## 5. Decoupled Benign False Positive Latency Analysis

Benign false alarms represent non-malicious system operations misclassified by detectors. Because these arise from entirely different operational mechanisms, their latencies are reported separately here.

| Detector Configuration | Triggering Scenario | Sample Size | False Positive Latency (Mean $\pm$ SD) | Latency 95% CI |
|:---|:---|:---:|:---:|:---:|
| **Baseline Behavioral** | B4 (Bulk Renaming / Compiler Build) | $n = 10$ | $271.30 \pm 4.48$ ms | $[268.09, 274.51]$ ms |
| **Canary-Only Decoy** | B3 (Maintenance / Cleanup Touch) | $n = 10$ | $13.48 \pm 4.17$ ms | $[10.50, 16.46]$ ms |
| **Hybrid Corroborated** | None (Zero False Positives) | $n = 0$ | N/A (Perfect Suppression) | N/A |

### Key Findings on False Positives:
1. **Baseline False Positives (B4):** Occur late in the workload ($271.30$ ms) because the compiler build must execute dozens of rapid file renames before triggering the mass-rename heuristic. Conflating this $271.30$ ms figure into attack detection latency was an error in previous drafts.
2. **Canary-Only False Positives (B3):** Occur instantaneously ($13.48$ ms) upon the first benign file touch by an administrative script or search tool. Pure canaries cannot distinguish harmless maintenance from ransomware.
3. **Hybrid False Positive Immunity:** Hybrid completely eliminated all false alarms ($0/40$ benign trials), achieving an empirical Specificity of 100%.

---

## 6. Comprehensive Confusion Matrix & Quality Metrics

Across all 180 trials (60 per detector: 40 benign, 20 attack):

| Metric | Configuration A (Baseline) | Configuration B (Canary-Only) | Configuration C (Hybrid) | Formula / Definition |
|:---|:---:|:---:|:---:|:---|
| **True Positives (TP)** | 20 | 10 | 10 | Correctly detected attack runs |
| **False Positives (FP)** | 10 | 10 | 0 | Benign runs falsely alarmed |
| **True Negatives (TN)** | 30 | 30 | 40 | Clean benign runs passed |
| **False Negatives (FN)** | 0 | 10 | 10 | Attack runs missed |
| **Total Trials** | 60 | 60 | 60 | $TP + FP + TN + FN$ |
| **Sensitivity (Recall)** | **1.000 (100%)** | 0.500 (50.0%) | 0.500 (50.0%) | $TP / (TP + FN)$ |
| **Specificity** | 0.750 (75.0%) | 0.750 (75.0%) | **1.000 (100%)** | $TN / (TN + FP)$ |
| **Precision (PPV)** | 0.667 (66.7%) | 0.500 (50.0%) | **1.000 (100%)** | $TP / (TP + FP)$ |
| **Negative Predictive Value (NPV)** | **1.000 (100%)** | 0.750 (75.0%) | 0.800 (80.0%) | $TN / (TN + FN)$ |
| **False Positive Rate (FPR)** | 0.250 (25.0%) | 0.250 (25.0%) | **0.000 (0.0%)** | $FP / (FP + TN)$ |
| **F1-Score** | 0.800 | 0.500 | 0.667 | $2 \cdot (Prec \cdot Rec) / (Prec + Rec)$ |
| **Diagnostic Odds Ratio (DOR)** | $\infty$ | $3.00$ | $\infty$ | $(TP \cdot TN) / (FP \cdot FN)$ |

### Fisher's Exact Test on False Positive Rates
- **Hybrid (0/40 FP) vs Baseline (10/40 FP):** Two-tailed Fisher's Exact test $p = 0.00102966$ ($p < 0.01$).
- **Hybrid (0/40 FP) vs Canary-Only (10/40 FP):** Two-tailed Fisher's Exact test $p = 0.00102966$ ($p < 0.01$).
- **Conclusion:** Hybrid's reduction in false positive alarms from 25.0% to 0.0% is statistically significant at the 99% confidence level.

---

## 7. Damage Reduction & Containment Effectiveness

Damage is quantified by the number of user files encrypted or corrupted before the endpoint response manager halted the simulation.

| Workload Scenario | Metric | Baseline Behavioral | Canary-Only Decoy | Hybrid Corroborated |
|:---|:---|:---:|:---:|:---:|
| **S5 (Decoy Traversal Attack)** | Files Damaged (Mean $\pm$ SD) | $0.00 \pm 0.00$ | $0.10 \pm 0.32$ | $0.10 \pm 0.32$ |
| | Operations Prevented | $11.00 \pm 0.00$ | $10.90 \pm 0.32$ | $10.90 \pm 0.32$ |
| | Containment Trigger Rate | 100% (10/10) | 100% (10/10) | 100% (10/10) |
| **S6 (Evasive Attack)** | Files Damaged (Mean $\pm$ SD) | $6.10 \pm 0.32$ | $10.00 \pm 0.00$ | $10.00 \pm 0.00$ |
| | Operations Prevented | $3.90 \pm 0.32$ | $0.00 \pm 0.00$ | $0.00 \pm 0.00$ |
| | Containment Trigger Rate | 100% (10/10) | 0% (0/10) | 0% (0/10) |

### Key Damage Findings & Metric Clarification:
1. **On Decoy-Touching Attacks (S5 — 99.09% User File Protection):**
   - Both Canary-Only and Hybrid achieve near-instantaneous containment, limiting file damage to an average of $0.10$ user files out of 11 targeted operations:
     $$\text{S5 User Data Damage Prevention} = \frac{11.0 - 0.10}{11.0} \times 100\% = \mathbf{99.09\% \approx 99.1\%}$$
   - The legacy $90.83\%$ figure arose from including the sacrificial canary file in the denominator ($\frac{10.9}{12.0}$). Because canaries are expendable deception tripwires, user file damage prevention is correctly retained at **99.09%**.
2. **Scenario-Level Unweighted Average (49.55%):**
   - In Scenario S6 (decoy evasion), Hybrid prevented 0.0% of operations ($0/10$ recall).
   - The unweighted average of scenario-level prevention percentages across the two attack scenarios is:
     $$\text{Scenario-Level Mean} = \frac{99.09\% (\text{S5}) + 0.00\% (\text{S6})}{2} = \mathbf{49.55\%}$$
   - (Note: This also matches the pooled operations ratio across all 20 suspicious trials: $\frac{10 \times 10.9 \text{ ops prevented}}{10 \times 12 + 10 \times 10 \text{ ops planned}} = \frac{109.0}{220.0} = \mathbf{49.55\%}$.)
3. **Underlying Formulation for the Operations-Based Figure (45.42%):**
   - The 45.42% metric represents the unweighted arithmetic mean of per-trial planned operations ratios across all 20 suspicious attack trials:
     - 10 trials in Scenario S5 where each achieved $\frac{10.9 \text{ prevented}}{12.0 \text{ planned}} = 90.8333\%$
     - 10 trials in Scenario S6 where each achieved $\frac{0.0 \text{ prevented}}{10.0 \text{ planned}} = 0.0000\%$
   - **Exact Formula:**
     $$\text{Per-Trial Mean Ratio} = \frac{\sum_{i=1}^{20} \text{ratio}_i}{20} = \frac{10 \times \left(\frac{10.9}{12.0}\right) + 10 \times \left(\frac{0.0}{10.0}\right)}{20} = \frac{9.08333}{20} = \mathbf{45.42\%}$$
   - **Underlying Numerator:** $\sum_{i=1}^{20} \text{ratio}_i = 9.08333$
   - **Underlying Denominator:** $20$ attack trials
4. **On Decoy-Evading Attacks (S6):** Baseline's pure behavioral heuristic caught the evasive attack after an average of $6.10$ files were damaged, saving the remaining $3.90$ files. Canary-Only and Hybrid failed to trigger on S6 because neither decoy files were touched, allowing all 10 files to be damaged.
5. **Academic Architectural Lesson:** Canary deception is an exceptional early-warning accelerant for attacks that traverse endpoints, but cannot serve as a solitary control against targeted or decoy-aware threats. An enterprise defense-in-depth architecture must pair decoy-triggered corroborate alarms with a fallback behavioral engine.

---

## 8. Summary Table of Statistical Comparisons

| Comparison Pair | Dependent Variable | Sample Sizes | Statistical Test | Test Statistic | $p$-value | Significance | Effect Size |
|:---|:---|:---:|:---|:---:|:---:|:---:|:---:|
| Hybrid vs Baseline (S5) | Detection Latency | $n_1=10, n_2=10$ | Welch's $t$-test | $t = 0.1067$ | $0.9168$ | Not Significant (Equivalence not established) | Cohen's $d = 0.048$ |
| Hybrid vs Baseline (S5) | Detection Latency | $n_1=10, n_2=10$ | Mann-Whitney $U$ | $U = 37.0$ | $0.3447$ | Not Significant (Equivalence not established) | Rank-biserial $= 0.26$ |
| Hybrid vs Canary (S5) | Detection Latency | $n_1=10, n_2=10$ | Welch's $t$-test | $t = 0.5379$ | $0.5976$ | Not Significant (Equivalence not established) | Cohen's $d = 0.241$ |
| Hybrid vs Canary (S5) | Detection Latency | $n_1=10, n_2=10$ | Mann-Whitney $U$ | $U = 54.0$ | $0.7913$ | Not Significant (Equivalence not established) | Rank-biserial $= 0.08$ |
| Hybrid vs Baseline (FPR) | False Positive Rate | $N_1=40, N_2=40$ | Fisher's Exact | Odds Ratio $= 0.0$ | $0.001030$ | $p < 0.01$ ** | $\phi = 0.378$ |
| Hybrid vs Canary (FPR) | False Positive Rate | $N_1=40, N_2=40$ | Fisher's Exact | Odds Ratio $= 0.0$ | $0.001030$ | $p < 0.01$ ** | $\phi = 0.378$ |
| Baseline vs Hybrid (Recall) | Attack Detection Rate | $N_1=20, N_2=20$ | Fisher's Exact | Odds Ratio $= \infty$ | $0.000436$ | $p < 0.001$ *** | $\phi = 0.577$ |

*Significance levels: \*\*\* $p < 0.001$, \*\* $p < 0.01$, \* $p < 0.05$. Note: Comparing overall pooled attack latency ($84.92$ ms vs $26.10$ ms) reflects scenario composition asymmetry (Baseline detected S6 evasive attacks; Hybrid did not) rather than intrinsic detector speed. No statistically significant S5 latency difference was detected; equivalence was not established.*
