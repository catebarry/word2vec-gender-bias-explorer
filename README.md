# Word2Vec Political Bias Explorer

An interactive Streamlit app for visualizing political associations encoded in pretrained word embeddings from Google News.

## Overview

Word embeddings form the foundation of many AI systems, learning relationships between words from their co-occurrence in large text corpora. However, these representations can also absorb human biases present in the training data, including political ideology. This project reveals how even widely used embeddings like [GoogleNews Word2Vec](https://code.google.com/archive/p/word2vec/) encode partisan associations in language.

Prior research shows that various bias dimensions in word embeddings trained on a corpus of text can be identified by constructing a vector/subspace from paired examples and projecting words onto it. For instance, [Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings](https://proceedings.neurips.cc/paper/2016/file/a486cd07e4ac3d270571622f4f316ec5-Paper.pdf) explores gender bias, and [Studying Political Bias via Word Embeddings](https://dl.acm.org/doi/pdf/10.1145/3366424.3383560) explores political bias in word embeddings. 

Inspired by [Word2Vec Gender Bias Explorer](https://chanind.github.io/word2vec-gender-bias-explorer), this version adapts the same PCA-based methodology to explore political bias. It projects words onto a binary axis (Democrat <-> Republican), while acknowledging that real-world bias is more complex than two binary extremes.


## Quick Start

### Installation

```bash
git clone https://github.com/<your-username>/word2vec-political-bias-explorer.git
cd word2vec-political-bias-explorer

python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

### Place the model file
Download [GoogleNews-vectors-negative300.bin](https://code.google.com/archive/p/word2vec/) and move it into the data/ folder. If you have a reduced .npz version of the embeddings, you can use that instead.
```bash
data/GoogleNews-vectors-negative300.bin
```

### Generate biases
Run the precomputation script once to create a bias lookup file.
```bash
python precalculate_biases.py
```

### Running the App

```bash
streamlit run app.py
```

Then open the URL displayed in your terminal (default: http://localhost:8501).

## How It Works

**Load Pre-trained Embeddings**
The GoogleNews Word2Vec dataset is loaded for word vector lookup.

**Define Political Seed Pairs**
Defining political dimension pairs is not as straightforward as defining gender pair antonyms (such as he/her, man/woman, guy/gal, etc.). Anchors were chosen based on the methodology in [Studying Political Bias via Word Embeddings](https://dl.acm.org/doi/pdf/10.1145/3366424.3383560) that analyzes the frequencies of words in known Republican/Democratic sources that describe the same or parallel concepts. Some chosen pairs include (democrat, republican), (liberal, conservative), (Dems, GOP), and (CNN, Fox).

**Compute Political Axis with PCA**
For each seed pair, we compute the difference vector and apply PCA. The first principal component defines the political axis.

**Score and Visualize Words**
Each word is projected onto the political axis and scaled to roughly [-1, 1]:
- Negative scores indicate left/Democrat-leaning association (blue)
- Positive scores indicate right/Republican-leaning association (red)

**Interactive Exploration**
Use the Streamlit interface to type in words or short phrases to see the bias score, a per-token breakdown, and additional analysis.

## Project Structure

```
word2vec-political-bias-explorer/
├── PcaBiasCalculator.py         # PCA-based bias computation
├── PrecalculatedBiasCalculator.py
├── precalculate_biases.py       # Generates data/biases.json
├── parse_sentence.py            # spaCy parser for compound tokens
├── app.py                       # Streamlit web interface
├── requirements.txt             # Dependencies
├── README.md
└── data/
    ├── GoogleNews-vectors-negative300.bin   # Word2Vec model (large file)
    └── biases.json                         # Word → bias mapping
```

## Setup Notes

**First Run:** Execute `precalculate_biases.py` once to generate the `biases.json.` before launching the app.

**Memory Use:** The full GoogleNews model is 3GB+. For slower machines, you can pre-reduce the vocabulary (e.g., keep top 40k words).


## References

Bolukbasi, T. et al. (2016). Man is to Computer Programmer as Woman is to Homemaker? https://arxiv.org/abs/1607.06520

Chanind (2020). Word2Vec Gender Bias Explorer. https://github.com/chanind/word2vec-gender-bias-explorer

Gordon, J. et al. (2020). Studying Political Bias via Word Embeddings. https://dl.acm.org/doi/10.1145/3366424.3383560

Mikolov, T. et al. (2013). Efficient Estimation of Word Representations in Vector Space. https://arxiv.org/abs/1301.3781

Caliskan, A., Bryson, J., & Narayanan, A. (2017). Semantics derived automatically from language corpora contain human-like biases. Science 356(6334): 183–186.

Badilla, P. et al. (2025). WEFE: A Python Library for Measuring and Mitigating Bias in Word Embeddings. https://www.jmlr.org/papers/v26/22-1133.html
