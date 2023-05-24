> Originally forked from [MS20190155/Measuring-Corporate-Culture-Using-Machine-Learning](https://github.com/MS20190155/Measuring-Corporate-Culture-Using-Machine-Learning)

**Find the original description below the line**

# Measuring corporations' CSR and ESG initiatives by constructing an index using word-embeddings and machine learning.

Python code based on a pipeline to measure corporate culture, but modified to accommodate for corporations' CSR and ESG initiatives, including DEI values. This repository is built on the work you can find in the original fork, the code has been modified to accomodate for CSR and ESG reports, as well as transcripts of earnings calls. Major additions so far: (1) a preprocessor module to handle pdf files (earnings calls transcripts and reports). 

<!-- Planned: (2) a visualizer module for a better overview of the results. -->

## Setup from scratch, on Windows 10 (tl;dr)

* Install Anaconda (https://www.anaconda.com/)
* Install an IDE (e.g. Visual Studio Code - https://code.visualstudio.com/)
* Install Git (https://git-scm.com/download/win)
* Install Java (Windows Offline 64-bit - https://www.java.com/en/download/manual.jsp)
* Install Stanford CoreNLP v3.9.2 (http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip) by manually placing the uncompressed folder somewhere, e.g. C:\Users\user\AppData\Local\stanford-corenlp-full-2018-10-05
* Clone code repository to your working directory: git clone https://github.com/partigabor/index-construction.git
* Create an environment called "index": `conda create -n index python=3.9`
* Activate this environment: `conda activate index`
* Add Anaconda to Windows Path environment variables so that VSCode terminal will recognize and use Anaconda prompt (add these two lines "C:\Users\user\AppData\Local\Anaconda3\Scripts" and "C:\Users\user\AppData\Local\Anaconda3") 
* Add a Python interpreter to VSCode from this new conda environment. If not offered, you can probably find it at: C:\Users\user\AppData\Local\anaconda3\envs\index\python.exe
* Install required python packages: `pip install -r requirements.txt`
* Add Stanford CoreNLP path to global_options.py: os.environ["CORENLP_HOME"] = "C:/Users/user/AppData/Local/stanford-corenlp-full-2018-10-05/"
* Test with command: `python -m culture.preprocess`; if success, you should see:

	Starting server with command: java -Xmx16G -cp C:/Users/gparti/AppData/Local/stanford-corenlp-full-2018-10-05//* edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 60000 -threads 1 -maxCharLength 100000 -quiet True -serverProperties corenlp_server-8922256f13d24a46.props -preload tokenize, ssplit, pos, lemma, ner, depparse
	(['when[pos:WRB] I[pos:PRP] be[pos:VBD] a[pos:DT] child[pos:NN] in[pos:IN] [NER:LOCATION]Ohio[pos:NNP] ,[pos:,] I[pos:PRP] always[pos:RB] want[pos:VBD] to[pos:TO] go[pos:VB] to[pos:TO] [NER:ORGANIZATION]Stanford[pos:NNP]_University[pos:NNP] with[pos:IN]_respect[pos:NN]_to[pos:TO] higher[pos:JJR] education[pos:NN] .[pos:.] ', 'but[pos:CC] I[pos:PRP] go[pos:VBD] along[pos:IN] with[pos:IN] my[pos:PRP$] parent[pos:NNS] .[pos:.] '], ['None_0', 'None_1'])

* Tweak settings in global_options.py according to your machine (e.g. RAM, CPU cores, etc.)
* Setup complete, define `DATA_FOLDER` to train on your own data, adjust dimensions `DIMS` and `SEED_WORDS` to your own needs.

For prerequisites and system requirements, you can also follow the instructions of the original repository (see details below). In short, you need Python, Java, and Stanford CoreNLP 3.9.2.

## Usage notes
    
### 1. Place your documents into a directory, e.g. `data-test/raw`.

>Currently, `data-test` has been set up for you. If you want to work with a different directory or settings, make changes in `global-options.py`. Training the model on `data-test` (150 documents) should take 1 hour on an average system.

### 2. Run `main.py` to run everything, or run the modules one by one as below:

    python preprocess.py

This module takes in pdf files and accompanying xml metadata files from a dataset and processes the documents to be suitable for training, extracting their content and creating input files `documents.txt` and `document_ids.txt`.

    python parse.py

    python clean_and_train.py

    python create_dict.py

    python score.py

    python aggregate_firms.py

See explanations on the modules in the original README (below).

**If you encounter problems, you most likely need to:**

* Check if the packages' versions are compatible (you would get an error message)
* Check for correct settings of paths and parameters in `global_options.py`
* Check for documents with missing data (xml tree errors)
* Check for documents that are not in UTF-8 character encoding.
* Check for documents too large.
* Deprecation warnings can be ignored.

Gábor PARTI

***

***

***

# Measuring Corporate Culture Using Machine Learning

## Introduction
The repository implements the method described in the paper 

Kai Li, Feng Mai, Rui Shen, Xinyan Yan, [__Measuring Corporate Culture Using Machine Learning__](https://academic.oup.com/rfs/advance-article-abstract/doi/10.1093/rfs/hhaa079/5869446?redirectedFrom=fulltext), _The Review of Financial Studies_, 2020; DOI:[10.1093/rfs/hhaa079](http://dx.doi.org/10.1093/rfs/hhaa079) 
[[Available at SSRN]](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3256608)

The code is tested on Ubuntu 18.04 and macOS Catalina, with limited testing on Windows 10.  

## Requirements
The code requires 
- `Python 3.6+`
- The required Python packages can be installed via `pip install -r requirements.txt`
- Download and uncompress [Stanford CoreNLP v3.9.2](http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip). Newer versions may work, but they are not tested. Either [set the environment variable to the location of the uncompressed folder](https://stanfordnlp.github.io/stanfordnlp/corenlp_client.html), or edit the following line in the `global_options.py` to the location of the uncompressed folder, for example: 
> os.environ["CORENLP_HOME"] = "/home/user/stanford-corenlp-full-2018-10-05/"   

- If you are using Windows, use "/" instead of "\\" to separate directories.  
- Make sure [requirements for CoreNLP](https://stanfordnlp.github.io/CoreNLP/) are met. For example, you need to have Java installed (if you are using Windows, install [Windows Offline (64-bit) version](https://java.com/en/download/manual.jsp)). To check if CoreNLP is set up correctly, use command line (terminal) to navigate to the project root folder and run `python -m culture.preprocess`. You should see parsed outputs from a single sentence printed after a moment:

    (['when[pos:WRB] I[pos:PRP] be[pos:VBD] a[pos:DT]....

## Data
We included some example data in the `data/input/` folder. The three files are
- `documents.txt`: Each line is a document (e.g., each earnings call). Each document needs to have line breaks remvoed. The file has no header row. 
- `document_ids.txt`: Each line is document ID (e.g., unique identifier for each earnings call). A document ID cannot have `_` or whitespaces. The file has no header row. 
- (Optional) `id2firms.csv`: A csv file with three columns (`document_id`:str, `firm_id`:str, `time`:int). The file has a header row. 


## Before running the code
You can config global options in the `global_options.py`. The most important options are perhaps:
- The RAM allocated for CoreNLP
- The number of CPU cores for CoreNLP parsing and model training
- The seed words
- The max number of words to include in each dimension. Note that after filtering and deduplication (each word can only be loaded under a single dimension), the number of words will be smaller. 


## Running the code
1. Use `python parse.py` to use Stanford CoreNLP to parse the raw documents. This step is relatvely slow so multiple CPU cores is recommended. The parsed files are output in the `data/processed/parsed/` folder:
    - `documents.txt`: Each line is a *sentence*. 
    - `document_sent_ids.txt`: Each line is a id in the format of `docID_sentenceID` (e.g. doc0_0, doc0_1, ..., doc1_0, doc1_1, doc1_2, ...). Each line in the file corresponds to `documents.txt`. 
    
    Note about performance: This step is time-consuming (~10 min for 100 calls). Using `python parse_parallel.py` can speed up the process considerably (~2 min with 8 cores for 100 calls) but it is not well-tested on all platforms. To not break things, the two implementations are separated. 

2. Use `python clean_and_train.py` to clean, remove stopwords, and named entities in parsed `documents.txt`. The program then learns corpus specific phrases using gensim and concatenate them. Finally, the program trains the `word2vec` model. 

    The options can be configured in the `global_options.py` file. The program outputs the following 3 output files:
    - `data/processed/unigram/documents_cleaned.txt`: Each line is a *sentence*. NERs are replaced by tags. Stopwords, 1-letter words, punctuation marks, and pure numeric tokens are removed. MWEs and compound words are concatenated. 
    - `data/processed/bigram/documents_cleaned.txt`: Each line is a *sentence*. 2-word phrases are concatenated.  
    - `data/processed/trigram/documents_cleaned.txt`: Each line is a *sentence*. 3-word phrases are concatenated. This is the final corpus for training the word2vec model and scoring. 

   The program also saves the following gensim models:
   - `models/phrases/bigram.mod`: phrase model for 2-word phrases
   - `models/phrases/trigram.mod`: phrase model for 3-word phrases
   - `models/w2v/w2v.mod`: word2vec model
   
3. Use `python create_dict.py` to create the expanded dictionary. The program outputs the following files:
    - `outputs/dict/expanded_dict.csv`: A csv file with the number of columns equal to the number of dimensions in the dictionary (five in the paper). The row headers are the dimension names. 
    
    (Optional): It is possible to manually remove or add items to the `expanded_dict.csv` before scoring the documents. 

4. Use `python score.py` to score the documents. Note that the output scores for the documents are not adjusted by the document length. The program outputs three sets of scores: 
    - `outputs/scores/scores_TF.csv`: using raw term counts or term frequency (TF),
    - `outputs/scores/scores_TFIDF.csv`: using TF-IDF weights, 
    - `outputs/scores/scores_WFIDF.csv`: TF-IDF with Log normalization (WFIDF). 

    (Optional): It is possible to use additional weights on the words (see `score.score_tf_idf()` for detail).  

5. (Optional): Use `python aggregate_firms.py` to aggregate the scores to the firm-time level. The final scores are adjusted by the document lengths. 

