# 🏈 The Deceleration Engine: Quantifying Route Separation Through Combine Braking Dynamics

<p align="center">
  <img src="https://img.shields.io/badge/Competition-NFL%20Big%20Data%20Bowl%202027-013369?style=for-the-badge&logo=nfl&logoColor=white" alt="NFL Big Data Bowl 2027" />
  <img src="https://img.shields.io/badge/Track-Analytics%20%26%20Scouting-107C41?style=for-the-badge" alt="Analytics Track" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License: MIT" />
</p>

<p align="center">
  <em>"Speed gets you noticed; deceleration gets you open."</em>
</p>

---

## 📌 Executive Summary (For Scouts & Front Offices)

Traditional scouting at the **NFL Scouting Combine** has historically over-indexed on straight-line acceleration and 40-yard dash times. However, our empirical audit of 10Hz sensor tracking reveals that while maximum speed translates from drills to games ($r \approx 0.95$), static start metrics carry shockingly low predictive power ($r \approx 0.28$).

**The Deceleration Engine** bridges the gap between RFID sensor tags at the Combine and in-game **Next Gen Stats (NGS)** across over 100,000 route plays. We demonstrate that elite wide receivers generate open throwing windows not by outrunning defensive backs, but by **braking faster and more abruptly** at route inflection points.

### 🔑 Key Takeaways:
1. **The 40-Yard Dash Fallacy:** On breaking routes (*Hitch, Out, In, Slant*)—which constitute over **70% of NFL passing plays**—the 40-yard dash time exhibits negligible correlation with target separation ($r = -0.245$).
2. **Deceleration Is Predictive:** Our proprietary kinematic metric, **`BRK+` (Braking Rate Plus)**, strongly correlates with in-game separation ($r = -0.475$).
3. **Draft Sleeper Arbitrage:** Players with mediocre 40 times (e.g., 4.55–4.65s) but elite `BRK+` (>125) are systematically undervalued by consensus draft boards, yet create top-tier separation in the NFL.

---

## 📊 Core Empirical Visualizations

### 1. The Translation Proved: Combine Braking (BRK+) vs. In-Game Route Separation
Validating across 104 qualified NFL players that higher Combine deceleration efficiency directly predicts wider throwing windows on game day:

<p align="center">
  <img src="reports/figures/brk_plus_vs_ingame_separation.png" alt="BRK+ vs In-Game Separation" width="85%" />
</p>

### 2. Route Break Kinematic Heatmap
Visualizing the exact moment when the wide receiver initiates peak braking ($a_t < -6 \text{ yd/s}^2$), causing the defensive back to overshoot due to mechanical reaction latency:

<p align="center">
  <img src="reports/figures/field_route_break_overlay.png" alt="Route Break Overlay" width="85%" />
</p>

### 3. WR Deceleration vs. Created Separation Over Time
Synchronized time series capturing the ~250ms defensive reaction lag and the opening of the target window:

<p align="center">
  <img src="reports/figures/separation_dynamics_curve.png" alt="Separation Dynamics" width="85%" />
</p>

---

## 🏆 Top BRK+ Performers & Scout Case Studies

| Player | Position | 40-yd Dash | **BRK+ Index** | In-Game Mean Separation | Breaking Routes Sample |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Xavier Restrepo** | WR | — | **132.5** | **3.05 yds** | 14 |
| **Pat Bryant** | WR | 4.61 s | **130.7** | **3.19 yds** | **161** |
| **Jacolby George** | WR | — | **130.4** | **3.64 yds** | 5 |
| **Luther Burden** | WR | 4.41 s | **127.9** | **2.96 yds** | **145** |
| **Chimere Dike** | WR | 4.34 s | **127.4** | **3.00 yds** | **133** |
| **Tai Felton** | WR | 4.37 s | **126.2** | **2.87 yds** | 23 |
| **Isaiah Bond** | WR | 4.39 s | **123.7** | **3.41 yds** | **113** |
| **Rome Odunze** | WR | 4.45 s | **Top Peak Decel (-34.6 yd/s²)** | **3.10 yds** | **150+** |

### 🔍 Case Study: Pat Bryant (The 4.61s Route Technician)
* **The Traditional Consensus:** A 4.61s forty-yard dash would typically drop a wide receiver into late-round or priority free agent status.
* **The Kinematic Reality:** Bryant ranks **#2 overall in BRK+ (130.7)**. Across 161 breaking routes in the regular season, he consistently generates **3.19 yards of separation**, demonstrating elite deceleration mechanics that overcome straight-line speed limitations.

---

## 🧮 Mathematical & Kinematic Formulations

### 1. Tangential Acceleration ($a_t$) & Braking Isolation
To isolate true longitudinal braking force from centripetal turning force:

$$a_t = \frac{\vec{v} \cdot \vec{a}}{\|\vec{v}\|} = \frac{v_x a_x + v_y a_y}{\sqrt{v_x^2 + v_y^2}}$$

* **$a_t > 0$:** Acceleration / Propulsive phase
* **$a_t < -1.5 \text{ yd/s}^2$:** Active deceleration / Braking threshold

### 2. Centripetal Turning Acceleration ($a_n$) & Path Curvature ($\kappa$)

$$a_n = \frac{|v_x a_y - v_y a_x|}{\sqrt{v_x^2 + v_y^2}}, \quad \kappa = \frac{|v_x a_y - v_y a_x|}{(v_x^2 + v_y^2)^{3/2}}$$

### 3. Standardized Metric: `BRK+` (Braking Rate Plus)
Conditioned on player body mass ($m$), entry speed ($v_{entry}$), and route angle:

$$\text{BRK+} = 100 + 15 \times \left( \frac{\mu_{\text{league}} - a_{t, \text{player}}}{\sigma_{\text{league}}} \right)$$

* **$\text{BRK+} \ge 115$:** **Elite Tier** (Top 10% separation creators)
* **$100$:** **League Average Baseline**
* **$\text{BRK+} < 85$:** **Sluggish Cutter** (Heavy recovery risk against press coverage)

---

## 📁 Repository Structure

```
nfl-big-data-bowl-2027/
├── data/
│   ├── raw/               # Downloaded Kaggle competition files
│   └── processed/         # Master translation table (master_deceleration_translation.csv)
├── notebooks/
│   └── the_deceleration_engine.ipynb   # Complete Kaggle submission notebook (<2,000 words)
├── reports/
│   └── figures/           # Publication-quality charts and field diagrams
├── scripts/
│   ├── analyze_real_combine.py          # 10Hz Combine 3-Cone kinematics extractor
│   └── build_deceleration_engine_dataset.py  # End-to-end master merge & scoring
├── src/
│   ├── data/
│   │   └── loader.py      # Data loading, filtering & synthetic mock generators
│   ├── features/
│   │   ├── kinematics.py  # 10Hz Savitzky-Golay filtering, a_t, a_n, jerk, curvature
│   │   └── separation.py  # Dynamic WR-DB separation & reaction latency
│   ├── models/
│   │   └── metrics.py     # BRK+ baseline model & scoring logic
│   └── visualization/
│       ├── field.py       # Publication-grade authentic NFL field renderer
│       └── plots.py       # Analytical plotting routines
├── run_pipeline.py        # One-click execution pipeline
├── requirements.txt       # Dependencies
└── README.md
```

---

## 🚀 Quickstart & Reproduction

### 1. Clone the repository
```bash
git clone https://github.com/egorfm/nfl-big-data-bowl-2027.git
cd nfl-big-data-bowl-2027
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the complete pipeline
```bash
python scripts/build_deceleration_engine_dataset.py
```
Generated figures will be saved in `reports/figures/`.

---

## 🤝 Authors & Credits
* Developed by **[@egorfm](https://github.com/egorfm)** for the **NFL Big Data Bowl 2027 Analytics Track**.
* Built using Python, NumPy, Pandas, SciPy, Matplotlib, Seaborn, and Scikit-Learn.
