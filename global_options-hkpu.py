"""Global options for analysis
"""
import os
from pathlib import Path
from typing import Dict, List, Optional, Set

# Hardware options
N_CORES: int = 4  # max number of CPU cores to use
RAM_CORENLP: str = "16G"  # max RAM allocated for parsing using CoreNLP; increase to speed up parsing
PARSE_CHUNK_SIZE: int = 100 # number of lines in the input file to process uing CoreNLP at once. Increase on workstations with larger RAM (e.g. to 1000 if RAM is 64G)  

# Directory locations
os.environ["CORENLP_HOME"] = "C:/Users/hkpu/Programs/stanford-corenlp-full-2018-10-05/"  # location of the CoreNLP models; use / to seperate folders
DATA_FOLDER: str = "data/"
MODEL_FOLDER: str = "models/" # will be created if does not exist
OUTPUT_FOLDER: str = "outputs/" # will be created if does not exist; !!! WARNING: existing files will be removed !!!

# Parsing and analysis options
STOPWORDS: Set[str] = set(
    Path("resources", "StopWords_Generic.txt").read_text().lower().split()
)  # Set of stopwords from https://sraf.nd.edu/textual-analysis/resources/#StopWords
PHRASE_THRESHOLD: int = 10  # threshold of the phraser module (smaller -> more phrases)
PHRASE_MIN_COUNT: int = 10  # min number of times a bigram needs to appear in the corpus to be considered as a phrase
W2V_DIM: int = 300  # dimension of word2vec vectors
W2V_WINDOW: int = 5  # window size in word2vec
W2V_ITER: int = 20  # number of iterations in word2vec
N_WORDS_DIM: int = 500  # max number of words in each dimension of the dictionary
DICT_RESTRICT_VOCAB = None # change to a fraction number (e.g. 0.2) to restrict the dictionary vocab in the top 20% of most frequent vocab

# Inputs for constructing the expanded dictionary
DIMS: List[str] = ["diversity", "equity", "inclusion"]
SEED_WORDS: Dict[str, List[str]] = {
    "diversity": [
        "diversity",
        "diverse",
        "diverse_workplace",
        "diverse_employees",
        "diverse_board",
        "diverse_management",
        "ethnic",
        "ethnic_diversity",
        "ethnicity",
        "race",
        "racial",
        "color",
        "age",
        "age_diversity",
        "gender",
        "gender_diversity",
        "sexual_orientation",
        "lgbtq"
        "religion",
        "religious_background",
        "political_views",
        "marital_status",
        "pregnancy",
        "pregnant",
        "parental_status",
        "disability",
        "disabilities",
        "disabled",
        "neurodiversity",
        "veteran",
        "military_service",
    ],
    "equity": [
        "equity",
        "equality",
        "equal",
        "equal_pay",
        "equal_salary",
        "equal_opportunities",
        "equal_resources",
        "equitable",
        "fair",
        "fair_treatment",
        "fair_employment_practices"
        "fairness",
        "pay_gap",
        "gender_pay_gap",
    ],
    "inclusion": [
        "inclusion",
        "inclusive",
        "inclusive_culture",
        "interpersonal_integration",
        "involvement",
        "involvement_decision_making",
        "contribute",
        "respect",
        "respected",
        "respectful",
    ],
}

# Create directories if not exist
Path(DATA_FOLDER, "processed", "parsed").mkdir(parents=True, exist_ok=True)
Path(DATA_FOLDER, "processed", "unigram").mkdir(parents=True, exist_ok=True)
Path(DATA_FOLDER, "processed", "bigram").mkdir(parents=True, exist_ok=True)
Path(DATA_FOLDER, "processed", "trigram").mkdir(parents=True, exist_ok=True)
Path(MODEL_FOLDER, "phrases").mkdir(parents=True, exist_ok=True)
Path(MODEL_FOLDER, "phrases").mkdir(parents=True, exist_ok=True)
Path(MODEL_FOLDER, "w2v").mkdir(parents=True, exist_ok=True)
Path(OUTPUT_FOLDER, "dict").mkdir(parents=True, exist_ok=True)
Path(OUTPUT_FOLDER, "scores").mkdir(parents=True, exist_ok=True)
Path(OUTPUT_FOLDER, "scores", "temp").mkdir(parents=True, exist_ok=True)
Path(OUTPUT_FOLDER, "scores", "word_contributions").mkdir(parents=True, exist_ok=True)
