Towards Knowledge-Grounded Counter Narrative Generation for Hate Speech
====================


![pipeline_new](https://user-images.githubusercontent.com/9419045/163219818-9b290d44-7597-4b66-a135-9479650b8c6e.png)



This work aims at generating knowledge-bound counter narratives, using 2 moudles, knowledge retrieval module and counter narrative generation module.

#### Requirements:
```
Java 1.8+
Solr
Keyphrase digger

transformers
rouge_score
```

## Knowledge Retrieval Module

Under ```[./KN_retriever/data/KN_CONAN_final_data](https://github.com/yilingchung/Towards_KN_CN_Generation/tree/main/KN_retriever/data/KN_CONAN_final_data)```, we provide final CONAN dataset paired with corresponding silver knowledge. If you wish to prepare your own knowledge repository, check the steps below. Otherwise, skip this section.

1. Download CONAN dataset and knowledge repository 
2. Prepare queries
3. Retrieve relevant knowledge
4. Select knowledge sentences

### 1. Download Data

#### 1.1 Hate countering dataset
* __CONAN__: [CONAN - COunter NArratives through Nichesourcing: a Multilingual Dataset of Responses to Fight Online Hate Speech](https://github.com/marcoguerini/CONAN).

#### 1.2. Knowledge Repository

We use the following datasets for creating relevant knowledge.

* __Newsroom__: [Newsroom: A Dataset of 1.3 Million Summaries with Diverse Extractive Strategies](https://lil.nlp.cornell.edu/newsroom/index.html).

* __WikiText-103__: [Pointer sentinel mixture models](https://www.salesforce.com/products/einstein/ai-research/the-wikitext-dependency-language-modeling-dataset/).

### 2. Prepare Queries

#### 2.1. Query extraction

We use [Keyphrase Digger](https://github.com/dhfbk/KD) to extract keyphrase queries for both hate speech and counter narratives in CONAN.

* 1. create a txt file for each HS and CN in CONAN, run [create_text_file.py](https://github.com/yilingchung/Towards_KN_CN_Generation/blob/main/KN_retriever/create_text_file.py)
* 2. Make sure that the resulting files from i. are stored under ```KD/KD-Runner/target``` in your keyphrase Digger reporsitory after compiling
* 3. Retrieve keyphrases for HS and CN using Keyphrase Digger, store [run_kd.sh](https://github.com/yilingchung/Towards_KN_CN_Generation/blob/main/KN_retriever/run_kd.sh) under ```KD/KD-Runner/target``` and run ```./run_kd.sh``` under ```KD/KD-Runner/target```
* 4. Extract retrieved keyphrases from iii. and add them in CONAN data using [extract_keyphrase.py](https://github.com/yilingchung/Towards_KN_CN_Generation/blob/main/KN_retriever/extract_keyphrase.py)

#### 2.2. Query generation
We use [transformer implementation](https://github.com/cuicaihao/examples-TF/blob/master/community/en/transformer_chatbot.ipynb) to train and generate keyphrase queries.

### 3. Retrieve relevant knowledge
Retrieve relevant knowledge using Solr, run [retrieve_kn.py](https://github.com/yilingchung/Towards_KN_CN_Generation/blob/main/KN_retriever/retrieve_kn.py)
 
[Solr](https://solr.apache.org/) is used to index articles in knowledge repository and retrieve relevant knowledge given a query. 

Some solr commands:
- Launch solr:
	run `solr-8.8.1/bin/solr restart`
	or `./bin/solr restart`

- Index data (e.g., index all articles under ```datasets/wikitext/``` to knowledge repository called knowledgecollection):
    `bin/post -c knowledgecollection -p 8989 datasets/wikitext/*`

- An example of searching information about islamic faith in the field content from knowledge repository called knowledgecollection:
    `curl "http://localhost:8989/solr/knowledgecollection/select?q=(content:islamic faith)&rows=10&wt=json"`

Check [this tutorial](https://solr.apache.org/guide/8_10/solr-tutorial.html) on how to install solr, index data and advanced methods for searching data in detail.

### 4. Select knowledge sentences

1. Apply knowledge sentence selector to get the top-N knowledge sentences and save it in a single file, 1 entry per line, run [kn_sentence_retriever.py](https://github.com/yilingchung/Towards_KN_CN_Generation/blob/main/KN_retriever/kn_sentence_retriever.py)
2. Create train, valid, and test data, run [create_modelling_data.py](https://github.com/yilingchung/Towards_KN_CN_Generation/blob/main/KN_retriever/create_modelling_data.py).

## Counter Narrative Generation Module
* [Transformer](https://github.com/cuicaihao/examples-TF/blob/master/community/en/transformer_chatbot.ipynb)
* GPT2 (check [CN_generation](https://github.com/yilingchung/Towards_KN_CN_Generation/tree/main/CN_generation))
* [XNLG](https://github.com/CZWin32768/XNLG) 
* [Candela](https://github.com/XinyuHua/arggen-candela)

## Citation

For more details on data partition procedure, please see our paper.

```bibtex
@inproceedings{chung-etal-2021-towards,
    title = "Towards Knowledge-Grounded Counter Narrative Generation for Hate Speech",
    author = "Chung, Yi-Ling  and
      Tekiro{\u{g}}lu, Serra Sinem  and
      Guerini, Marco",
    booktitle = "Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.findings-acl.79",
    doi = "10.18653/v1/2021.findings-acl.79",
    pages = "899--914",
}
```
