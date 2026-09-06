<div align="center">

# 🖋️ CipherInk

### Interpretable Stylometric Authorship Attribution & Unknown-Author Detection

[![Python](https://img.shields.io/badge/Python-Backend-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Stylometry](https://img.shields.io/badge/Stylometry-70_Function--Word_Features-6C63FF?style=for-the-badge)](#)
[![Statistical Model](https://img.shields.io/badge/Model-Poisson_Log--Likelihood-00B894?style=for-the-badge)](#)

<br>

[![Live Demo](https://img.shields.io/badge/🔴_Live_Demo-Enter_CipherInk-FF0000?style=for-the-badge)](https://cipherink.onrender.com/)

<br>

*Interpretable Stylometry • Poisson Log-Likelihood • LLR-Based Verification • Unknown-Author Detection*

</div>

---

## 📌 Overview

**CipherInk** is an interpretable forensic stylometry framework designed to perform:

- **Multi-author attribution**
- **Authorship verification**
- **Unknown-author / Outsider detection**
- **Function-word-based linguistic analysis**

Rather than relying on large language models or opaque text embeddings, CipherInk models an author's stylistic profile using the frequencies of **70 high-frequency function words**. These words are comparatively less dependent on topic and can capture recurring patterns in an author's writing style.

The framework uses **Laplace-smoothed Poisson models** to estimate author-specific function-word distributions. It then evaluates an input text using **log-likelihood scores** and compares the strongest known-author hypothesis against an **Outsider reference profile** using a Log-Likelihood Ratio (LLR). 

CipherInk is designed as a lightweight and explainable prototype. Its predictions can be traced back to explicit linguistic features and probabilistic evidence rather than hidden neural representations.

> ⚠️ **Scope:** CipherInk is a controlled proof-of-concept system and should not be used as the sole basis for high-stakes authorship, academic misconduct, legal, or identity-related decisions.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **Multi-Author Profiling** | Builds separate stylometric profiles for multiple known authors using function-word frequency patterns. |
| **70 Function-Word Features** | Uses a fixed inventory of high-frequency function words to reduce direct dependence on topic-specific vocabulary. |
| **Poisson Log-Likelihood Modeling** | Models observed function-word counts using author-specific Poisson rate estimates. |
| **LLR-Based Unknown-Author Detection** | Compares the strongest known-author hypothesis against an Outsider reference profile using a Log-Likelihood Ratio. |
| **Interpretable Predictions** | Provides the predicted author, confidence information, likelihood evidence, and feature-level analysis. |
| **Real-Time Text Analysis** | Allows users to submit text through an interactive web interface and receive an immediate attribution result. |
| **Forensic Evidence Breakdown** | Displays expected and observed function-word behaviour to make predictions easier to inspect. |
| **Classical Baseline Evaluation** | Includes comparison against a Burrows' Delta stylometric baseline under a matched evaluation setting. |
| **Robustness Analysis** | Examines the effect of different Laplace smoothing values on evaluation performance. |

---

## 🧠 Methodology

### 1. Author Profile Construction

For each known author, CipherInk extracts counts for a fixed set of 70 function words from the author's training documents. 

Additive (Laplace) smoothing with a parameter of $\alpha=1$ is applied to avoid zero-valued expected rates. The expected baseline rate per 1,000 words is formally defined as:

$$Rate_{1000} = \frac{C_w + 1}{N_{training}} \times 1000$$

where $C_w$ is the raw observed count of a specific function word, and $N_{training}$ is the total token count of the author's corresponding training texts. 

During inference, the expected rate $\lambda$ is dynamically scaled to the input text length:

$$lm = \frac{N_{query}}{1000}$$

$$\lambda = Rate_{1000} \times lm$$

---

### 2. Poisson Log-Likelihood

For an input document, observed function-word counts are evaluated under each author's profile using the Poisson distribution. To prevent computational underflow, CipherInk computes the corresponding likelihoods in log space:

$$\log P(k\vert{}\lambda) = k \log(\lambda) - \lambda - \log(\Gamma(k+1))$$

The total author score is obtained by summing feature-level log-likelihood contributions across all $F = 70$ function words:

$$\log P(text\vert{}H) = \sum_{w=1}^{F} \log P(k_w\vert{}\lambda_{H,w})$$

The known author with the highest score is selected as the leading attribution candidate.

---

### 3. LLR-Based Outsider Detection

CipherInk compares the strongest known-author score with an Outsider reference profile, calculating a Log-Likelihood Ratio (LLR):

$$LLR(H_i) = \log P(text\vert{}H_i) - \log P(text\vert{}H_{Out})$$

The decision rule is:
- **LLR > 0:** classify the text as the strongest known author.
- **LLR ≤ 0:** classify the text as an **Outsider**.

---

### 4. Confidence Estimation

CipherInk applies temperature-scaled softmax to convert raw log-likelihood scores into interpretable, normalized display probabilities:

$$P(H_i) = \frac{\exp(\frac{\log P(text\vert{}H_i) - m_{ax}}{T})}{\sum_j \exp(\frac{\log P(text\vert{}H_j) - m_{ax}}{T})}$$

where $m_{ax}$ is the maximum log-likelihood among all hypotheses (for numerical stability) and $T = 8.5$ is the empirical temperature parameter. This scaling is purely presentational and mathematically preserves the exact rank ordering of classification decisions.

---

## 🔬 Evaluation Highlights

CipherInk was evaluated in a controlled setting involving:
- **5 known author profiles**
- **308 evaluation queries**
- **250 known-author evaluation samples**
- **58 Outsider evaluation samples**
- **70 function-word features**

### Evaluation Results

| Evaluation Task | Metric | Result |
| :--- | :--- | ---: |
| **Known vs. Outsider Detection** | Accuracy | **95.45%** |
| **Known vs. Outsider Detection** | Precision | **90.74%** |
| **Known vs. Outsider Detection** | Recall | **84.48%** |
| **Known vs. Outsider Detection** | F1-Score | **87.50%** |
| **Known vs. Outsider Detection** | AUC-ROC | **91.89%** |
| **Six-Class Attribution** | Accuracy | **67.21%** |
| **Six-Class Attribution** | Macro F1-Score | **0.663** |

> The binary known-vs-Outsider metrics and the six-class attribution metrics represent different evaluation tasks and should not be interpreted interchangeably.

### Comparison with Burrows' Delta

| Metric | CipherInk | Burrows' Delta |
| :--- | ---: | ---: |
| Six-Class Accuracy | **67.21%** | 55.84% |
| Six-Class Macro F1 | **0.663** | 0.566 |
| Binary Accuracy | **95.45%** | 88.96% |
| Binary F1-Score | **87.50%** | 67.31% |

Under the matched experimental setting, CipherInk outperformed the Burrows' Delta baseline across all reported evaluation metrics.

---

## 🖥️ Platform Interface

### 🧪 Enter the CipherInk Lab

<div align="center">
  <img
    src="Screenshots/CipherInk_Landing_Page.jpg"
    alt="CipherInk Landing Page"
    width="850"
  />
</div>

<br>

### 📝 Text Input & Analysis Dashboard

<div align="center">
  <img
    src="Screenshots/Manuscript_input.jpg"
    alt="CipherInk Manuscript Input Dashboard"
    width="850"
  />
</div>

---

## 🏗️ Project Architecture

```text
CipherInk
│
├── Data/
│   ├── Students/
│   │   ├── A/
│   │   ├── B/
│   │   ├── C/
│   │   ├── D/
│   │   └── E/
│   │
│   └── test/
│
├── Screenshots/
│
├── app.py
├── index.html
├── README.md
├── LICENSE
└── .gitignore
```
## Workflow
```text
Training Texts
      │
      ▼
Function-Word Feature Extraction
      │
      ▼
Laplace-Smoothed Author Profiles
      │
      ▼
Poisson Log-Likelihood Scoring
      │
      ├──────────────► Known Author Ranking
      │
      ▼
LLR Comparison with Outsider Profile
      │
      ▼
Known Author / Outsider Decision
      │
      ▼
Interactive Result & Forensic Breakdown
```
## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python |
| **Statistical Modeling** | Poisson Distribution, Log-Likelihood Analysis, LLR |
| **Stylometric Features** | 70 High-Frequency Function Words |
| **Frontend** | HTML, CSS, JavaScript |
| **Visualization** | Interactive Probability and Evidence Displays |
| **Research Baseline** | Burrows' Delta |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or later
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/ananyajoshi-cseai/CipherInk.git
cd CipherInk
```
### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
### 3. Run CipherInk

```bash
python app.py
```
## 📊 Reproducing the Evaluation

The repository includes the dataset and experimental resources used to evaluate CipherInk.

The evaluation workflow includes:

1. Loading the five known-author profiles
2. Processing known-author and Outsider evaluation samples
3. Generating author predictions
4. Applying the LLR-based Outsider decision rule
5. Computing binary and multiclass performance metrics
6. Exporting prediction results
7. Generating the confusion matrix

> The evaluation results in this repository represent a controlled experimental setting. They should not be treated as evidence of general performance across arbitrary authors, domains, languages, or writing styles.

---

## ⚠️ Limitations

CipherInk is a research prototype with several important limitations:

- The evaluation involves only **five known authors**.
- The author corpora are unequal in size and source diversity.
- The system has been evaluated only on **English-language text**.
- Performance may vary across genres and domains.
- Very long documents can accumulate small profile mismatches and produce overconfident predictions.
- The current evaluation does not establish performance on a broad benchmark.
- The system has not been independently evaluated on AI-generated text.
- The model assumes conditional independence among selected function-word counts.

---

## 🔮 Future Work

Potential directions for future development include:

- Evaluating on larger and more diverse authorship datasets
- Adding cross-domain and cross-genre evaluation
- Incorporating additional stylometric features
- Comparing against more classical and machine-learning baselines
- Adding confidence intervals and statistical significance analysis
- Developing length-aware confidence adjustment
- Sub-chunking very long documents before attribution
- Evaluating performance on AI-generated and human-AI hybrid text
- Supporting multilingual authorship analysis

---

## ⚖️ Ethical Use

CipherInk is intended for:

- Stylometry research
- Educational demonstrations
- Exploratory authorship analysis
- Transparent experimentation with probabilistic text models

It should **not** be used as the sole basis for:

- Academic misconduct allegations
- Legal or forensic conclusions
- Employment decisions
- Identity verification
- Punitive action against an individual

Any real-world use should include human review, supporting evidence, uncertainty analysis, and appropriate ethical oversight.

---

## 👥 Engineered By

<div align="center">

### **Team CipherInk**

| Contributor | Role & Affiliation |
| :--- | :--- |
| **[Ananya Joshi](https://portfolio-ananya-joshi.vercel.app/)** | Computer Science & Artificial Intelligence<br>Indira Gandhi Delhi Technical University for Women (IGDTUW) |
| **[Utkarsh Bharadwaj](https://utkarshbharadwaj.github.io/)** | Statistics, Mathematical Modeling & Backend Development<br>Indian Statistical Institute (ISI), Delhi |

<br>

*Designed and developed through collaborative work in interpretable stylometry, probabilistic modeling, and forensic text analysis.*

</div>

---

<div align="center">

### ⭐ If you found CipherInk interesting, consider starring the repository!

**Built with Python, probability, stylometry, and a focus on interpretable AI.**

</div>
