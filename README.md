Towards Knowledge-Grounded Counter Narrative Generation for Hate Speech
====================

This work aims at generating knowledge-bound counter narratives.

#### Requirements:
Java 1.8+
Python
Keyphrase digger
Solr
transformers

## Knowledge Retrieval Module

In our experiments, we focus on pairs that are annotated with just one counter narrative type. The data partition used in our experiments can be found under ```./data/```. For more details on data partition procedure, please see our paper submitted.
The data is stored in csv format, with 3 columns: __sentence1__ respresenting hate speech, __sentence2__ as corresponding counter narrative, and __label__ as counter narrative type.

Under ```./data/```, we provide final CONAN dataset paired with corresponding silver knowledge. 
The multiple-hate-target knowledge-grounded hate countering dataset can be found in [this repository](https://github.com/yilingchung/CONAN#Multi-hate-target-knowledge-grounded-hate-countering-dataset).
If you wish to prepare your own knowledge repository, please check the steps below.

### Data

We use the following datasets for creating relevant knowledge.

#### Hate countering dataset
__CONAN__: [CONAN - COunter NArratives through Nichesourcing: a Multilingual Dataset of Responses to Fight Online Hate Speech](https://github.com/marcoguerini/CONAN).

#### Knowledge Repository
__Newsroom__: [Newsroom: A Dataset of 1.3 Million Summaries with Diverse Extractive Strategies](https://lil.nlp.cornell.edu/newsroom/index.html).

__WikiText-103__: [Pointer sentinel mixture models](https://www.salesforce.com/products/einstein/ai-research/the-wikitext-dependency-language-modeling-dataset/).


### Query extraction

We use [Keyphrase Digger](https://github.com/dhfbk/KD) to extract keyphrases queries for both hate speech and counter narratives in CONAN dataset.

* create a txt file for each HS and CN in CONAN, using "create_HSCNtext_to_file.py"
* Move output folder from 1 to KD/KD-Runner/target
* Retrieve keyphrases for HS and CN using Keyphrase Digger with KD/KD-Runner/target/run_kd.sh
* Extract retrieved keyphrases from 3 and add them in CONAN data using extract_KP_from_file.py

### Query generation
We use transformer

### Knowledge Sentence Selection

[Solr](https://solr.apache.org/) is used to index articles in knowledge repository and retrieve relevant knowledge given a query. 

- How to launch solr:
	run `solr-8.8.1/bin/solr restart`
	or `./bin/solr restart`

- How to index data (e.g., index all articles under ```datasets/wikitext/``` to knowledge repository called knowledgecollection):
    `bin/post -c knowledgecollection -p 8989 datasets/wikitext/*`

- An example of searching information about islamic faith in the field content from knowledge repository called knowledgecollection:
    `curl "http://localhost:8989/solr/knowledgecollection/select?q=(content:islamic faith)&rows=10&wt=json"`

Check [this tutorial](https://solr.apache.org/guide/8_10/solr-tutorial.html) on how to install solr, index data and advanced methods for searching data in detail.

#### Main Features:

If you want to create your own knowledge repository, please follow the following steps. 
Otherwise, you can directly use our final retrieved knowledge data in FOLDER.
  
Knowledge retrieval 
* Retrieve relevant knowledge for each entry using Solr by running retrieve_KN.py
* Apply knowledge sentence selector to get the top-N knowledge sentences and save it in a single file, 1 entry per line, using KN_sentence_retriever.py
* Extract top-5 sentences from 6 and add them in CONAN data using KN_sentence_to dataframe.py

## Counter Narrative Generation Module
* Transformer
* GPT2
* [XNLG](https://github.com/CZWin32768/XNLG) 
* [Candela](https://github.com/XinyuHua/arggen-candela)

