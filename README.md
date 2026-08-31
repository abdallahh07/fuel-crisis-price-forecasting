<!-- ════════════════ HEADER ════════════════ -->
<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=210&color=0:1F283E,50:2B3653,100:1F283E&text=Abdallah%20Hashad&fontColor=F4F4F4&fontSize=52&fontAlignY=36&desc=Quantitative%20Finance%20%C3%97%20Machine%20Learning&descColor=EDCC80&descAlignY=58&descSize=18&animation=fadeIn" width="100%" />

<!-- typing effect -->
<a href="https://github.com/abdallahh07">
<img src="https://readme-typing-svg.demolab.com?font=Space+Grotesk&weight=600&size=24&duration=2800&pause=900&color=EDCC80&center=true&vCenter=true&width=620&lines=Machine+Learning+Engineer;Data+Scientist;CFA-level+Valuation+meets+Modern+ML;Building+models+that+answer+economic+questions" alt="Typing intro" />
</a>

<br/>

<img src="https://komarev.com/ghpvc/?username=abdallahh07&style=for-the-badge&color=2B3653&label=PROFILE+VIEWS" alt="Profile views" />

</div>

---

## <img src="https://media.giphy.com/media/WUlplcMpOCEmTGBtBW/giphy.gif" width="30"> About me

```python
class AbdallahHashad:
    role        = "Machine Learning Engineer & Data Scientist"
    location    = "Cairo, Egypt 🇪🇬"
    edge        = "CFA-level valuation + DCF modelling + professional appraisal work"

    def building(self):
        return ["end-to-end ML pipelines", "leakage-proof feature engineering",
                "tuned gradient boosting models", "quantitative finance tooling"]

    def current_focus(self):
        return {"learning": ["Hands-On ML (Géron)", "Linear Algebra (Strang)", "SQL"],
                "goal": "models that answer real economic questions, not just minimise loss"}
```

# Fuel Crisis Price Forecasting

**Forecasting US crude oil prices during the 2026 Iran War fuel crisis, 
using real, sourced data.**

---

## The Story (Non-Technical)

In early 2026, a war broke out that led to the closure of the Strait of 
Hormuz — a narrow shipping route through which nearly 20% of the world's 
oil passes. This single event triggered a sharp global fuel crisis: oil 
prices roughly doubled in a matter of weeks, gas prices at the pump spiked 
across the United States (topping $5–6 per gallon in several states), and 
the effects rippled through everyday life for months.

This project uses real, publicly-sourced data — oil futures prices, U.S. 
gas prices by region, refinery activity, and even public discussion on 
Reddit — to understand what happened during the crisis and build a model 
that predicts oil prices based on the patterns in that data.

### Why real data, not made-up numbers

Every number in this dataset is traceable to an actual source — crude oil 
prices from Yahoo Finance, gas and refinery data from the U.S. government's 
Energy Information Administration, a timeline of crisis events built from 
Wikipedia's own citations and official energy reports, and real Reddit 
discussion threads. Where a piece of data genuinely couldn't be found (one 
country's diesel price was missing from the source), that gap is left 
honestly blank rather than guessed at.

### What the project actually does

1. **Explores the data** — looking at how prices moved before, during, and 
   after the crisis, and figuring out what was most connected to the 
   changes (which US regions were hit hardest, how different fuels 
   reacted differently).
2. **Builds a prediction model** — trains a model that learns from 
   historical patterns to forecast oil prices, and rigorously checks 
   whether its predictions can actually be trusted.
3. **Is honest about the model's limits** — rather than just reporting a 
   good-looking accuracy score, the project digs into *why* the model 
   makes the predictions it does, and catches a real bias problem that a 
   surface-level accuracy check would have missed entirely.

### Why this matters

Fuel prices affect nearly everyone — transportation, heating, the price of 
goods at the store. Understanding how a major global event moves prices, 
and being able to model that impact honestly (including its flaws), is a 
genuinely useful way to make sense of a real crisis using real data.

---

## The Technical Process

### 1. Exploratory Data Analysis

Before any modeling, the EDA had to answer basic data-quality questions: 
missing values (one, documented and intentional — not filled in), and 
outliers (present, but they turned out to *be* the crisis itself — the 
actual price shock — not data errors to remove).

The correlation analysis surfaced the single most important structural 
fact in this dataset: **WTI and Brent crude columns correlate 0.96–0.99 
with each other.** That one finding drove every downstream modeling 
decision.

Time series plots confirmed the shape directly — a stable pre-crisis 
baseline, a sharp climb through March, a peak in early April, and a 
gradual decline back down by July. Natural gas moved differently: a 
brief, sharp spike in late January, unrelated in timing to crude oil's 
slower build-up — and, notably, *negatively* correlated with crude oil 
throughout.

### 2. Why These Models, Specifically

Model choice was a direct response to two things the EDA had already 
revealed:

- **Severe multicollinearity** (WTI/Brent at 0.96–0.99) meant the model 
  needed to handle redundant, near-duplicate features gracefully.
- **A very small dataset** (126 rows) meant a model prone to memorizing 
  noise instead of learning real patterns was a genuine risk.

This pointed toward **regularized linear models** — Lasso and Ridge, 
since their built-in penalty terms directly counteract both problems: 
they shrink coefficients to control complexity, and Lasso specifically can 
zero out redundant features entirely. **KNN and SVR** were tested too — 
KNN as a deliberate contrast (a model with *no* mechanism to handle 
multicollinearity), SVR as a reasonable middle ground.

This reasoning was documented *before* training, not after — the 
prediction was that Lasso would win because of its feature-selection 
property, not because it happened to score highest after the fact.

### 3. What Actually Happened

| Model | R² | 
|---|---|
| **Lasso** | **0.9129** |
| SVR | 0.8414 |
| Ridge | 0.8046 |
| KNeighborsRegressor | **-0.6316** |

Lasso won, as predicted. KNN's negative R² — worse than just guessing the 
average — was the clearest possible demonstration of why distance-based 
models struggle with highly correlated, small datasets.

### 4. Deeper Tuning — and a Genuine Course Correction

A wider hyperparameter search found a marginally better score (0.9148 vs 
0.9129) at `alpha=1e-05` — almost no regularization at all. Rather than 
accepting the "best" score blindly, checking the model's actual behavior 
mattered more: feature importance and SHAP values showed the model 
assigning large, *opposite-signed* coefficients to near-identical 
WTI/Brent columns — a classic sign of an under-regularized model 
compensating for multicollinearity rather than resolving it.

Residual analysis confirmed something the R² score alone completely hid: 
**the model was systematically underpredicting** on the test set — nearly 
every residual was positive, not randomly scattered around zero. A high 
R² measures whether predictions track the right *direction*; it says 
nothing about whether they're consistently *biased*.

**Decision:** the production model uses the more conservative `alpha=0.001` 
— explicitly trading a small amount of CV score for a properly regularized, 
more stable model. This is a deliberate, documented choice, not a 
compromise made silently.

### 5. Production Structure

```
forecasting/
├── config/          # all settings — paths, target, model params
├── processing/       # data loading, merging, feature/target creation
├── pipeline.py        # the full training sequence, as a reusable class
├── train_pipeline.py  # runs training, saves the model artifact
└── predict.py          # loads the saved model, makes new predictions

app/
├── schemas.py          # API request/response shape
├── api.py               # route definitions
└── main.py               # FastAPI service
```

Config-driven throughout — changing the target column, model 
hyperparameters, or data paths never requires touching the actual logic.

## Key Takeaways

- Multicollinearity and small sample size, both identified during EDA 
  *before* any model was trained, correctly predicted which model would win.
- A high R² is not the same as a trustworthy model — residual analysis 
  caught a real, systematic bias R² alone completely hid.
- The "best" hyperparameter by CV score wasn't automatically the right 
  choice for production — regularization strength was chosen deliberately.

## Repository Structure

```
├── data/raw/           # sourced, cited data files
├── notebooks/           # EDA and modeling notebooks
├── forecasting/           # production ML pipeline
├── app/                     # FastAPI prediction service
├── Dockerfile
└── requirements.txt
```
