# CanarySentinel — Statistical Hypothesis Testing Report

**Sample Size:** $N = 180$ trials (60 per detector configuration)  
**Significance Level:** $\alpha = 0.05$  

---

## 1. Corrected Decoupled Hypothesis Tests

| Hypothesis / Comparison | Statistical Test | Degrees of Freedom / n | Test Statistic | p-value | Significance | Conclusion |
|---|---|:---:|:---:|:---:|:---:|---|
| **Matched S5: Hybrid vs Baseline** | Welch Two-Sample $t$-test | $n_1=10, n_2=10, df=11.95$ | $t = 0.1067$ | $0.9168$ | Not Significant | **No Significant Latency Difference Detected**: Hybrid corroboration adds only $+0.30$ ms on attacks touching decoys ($p = 0.9168$; equivalence not established). |
| **Matched S5: Non-parametric Rank** | Mann-Whitney $U$ Test | $n_1=10, n_2=10$ | $U = 37.0$ | $p = 0.3447$ | Not Significant | Non-parametric rank sum detects no statistically significant difference in latency distributions on matched Scenario S5 attacks ($p = 0.3447$; equivalence not established). |
| **Matched S5: Hybrid vs Canary-Only** | Welch Two-Sample $t$-test | $n_1=10, n_2=10, df=17.03$ | $t = 0.5379$ | $0.5976$ | Not Significant | Corroborating canary touch with filesystem context adds $+1.82$ ms ($p = 0.5976$; equivalence not established). |
| **Matched S5: Canary Non-parametric** | Mann-Whitney $U$ Test | $n_1=10, n_2=10$ | $U = 54.0$ | $p = 0.7913$ | Not Significant | Non-parametric rank sum detects no statistically significant difference in latency rank distributions on S5 ($p = 0.7913$; equivalence not established). |
| **False Alarm Elimination (vs Baseline)** | Fisher Exact Test ($2 \times 2$) | $n_1=40, n_2=40$ | Odds Ratio: $0.0$ | $0.00102966$ | $p = 0.00103$ ** | **Statistically Significant**: Hybrid corroboration eliminated benign false positives in tested trials ($0/40$ vs $10/40$). |
| **False Alarm Elimination (vs Canary)** | Fisher Exact Test ($2 \times 2$) | $n_1=40, n_2=40$ | Odds Ratio: $0.0$ | $0.00102966$ | $p = 0.00103$ ** | **Statistically Significant**: Hybrid corroboration eliminated benign canary probe alarms in tested trials ($0/40$ vs $10/40$). |
| **Attack Coverage (Recall)** | Fisher Exact Test ($2 \times 2$) | $n_1=20, n_2=20$ | Odds Ratio: $\infty$ | $0.00043592$ | $p < 0.001$ *** | **Statistically Significant**: Baseline achieves higher overall recall ($20/20$ vs $10/20$) by detecting canary-blind attacks. |

> [!NOTE]
> **Methodological Latency Clarification:**
> 1. **Decoupled Attack Latency:** Attack detection latency must not be pooled with benign false-alarm latency. Baseline recorded 10 benign false alarms in Scenario B4 (mean $271.30$ ms); pooling these with true-positive attacks creates an artificial $147.05$ ms average.
> 2. **Scenario Composition Asymmetry:** Comparing overall attack latency ($84.92$ ms vs $26.10$ ms) does not demonstrate that Hybrid is faster. Baseline detected 20 attacks across both S5 ($25.80$ ms) and S6 ($144.05$ ms). Hybrid detected 10 attacks on S5 ($26.10$ ms) and completely missed S6 (0% recall). Hybrid's lower overall mean reflects the omission of difficult, slow-to-detect attacks rather than faster algorithmic speed. When matched on identical Scenario S5 attacks, Baseline ($25.80$ ms) and Hybrid ($26.10$ ms) show no statistically significant latency difference ($p = 0.9168$; equivalence not established).
> 3. **Independent Samples:** Trials between detector configurations were executed as independent randomized trials; paired tests are not assumed.

---

## 2. Rigorous Confidence Intervals
- **Matched Scenario S5 Latency ($n=10$ each; Quantile Method: Standard Linear Interpolation / Type 7):**
  - Baseline Behavioral: $25.80 \pm 3.47$ ms ($95\%$ CI: $[23.32, 28.28]$ ms); Median = $27.17$ ms, $\text{IQR} = 2.74$ ms ($Q_1=24.98, Q_3=27.72$; nearest-rank $\text{IQR}=3.20$ ms)
  - Canary-Only Decoy: $24.28 \pm 6.59$ ms ($95\%$ CI: $[19.56, 28.99]$ ms); Median = $25.68$ ms, $\text{IQR} = 6.27$ ms ($Q_1=20.30, Q_3=26.56$; nearest-rank $\text{IQR}=6.80$ ms)
  - Hybrid Corroborated: $26.10 \pm 8.43$ ms ($95\%$ CI: $[20.07, 32.13]$ ms); Median = $25.78$ ms, $\text{IQR} = 2.93$ ms ($Q_1=23.55, Q_3=26.49$; nearest-rank $\text{IQR}=3.75$ ms)
- **Overall True-Positive Attack Latency (Reflecting Scenario Composition):**
  - Baseline ($n=20$ detected across S5 and S6): $84.92 \pm 60.86$ ms ($95\%$ CI: $[58.25, 111.59]$ ms)
  - Canary-Only ($n=10$ detected on S5 only): $24.28 \pm 6.59$ ms ($95\%$ CI: $[19.56, 28.99]$ ms)
  - Hybrid ($n=10$ detected on S5 only): $26.10 \pm 8.43$ ms ($95\%$ CI: $[20.07, 32.13]$ ms)
- **Benign False-Positive Latency (Decoupled):**
  - Baseline B4 ($n=10$): $271.30 \pm 4.48$ ms ($95\%$ CI: $[268.09, 274.51]$ ms)
  - Canary-Only B3 ($n=10$): $13.48 \pm 4.17$ ms ($95\%$ CI: $[10.50, 16.46]$ ms)
  - Hybrid: Zero observed false positives in the tested benign trials
