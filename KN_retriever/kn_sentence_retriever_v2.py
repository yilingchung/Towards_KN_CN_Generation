# From documents retrieved for each pair of HS/CN in the dataset as input.
# Compute top N sentences related to HS and CN keyphrases, using RougeL as measures.
# The output is a txt and a jsonl file with each line stored the sorted top N sentences relevant to a pair of HS/CN.

import spacy
import re
import json
import pandas
import argparse
from rouge_score import rouge_scorer
from spacy.language import Language

boundary = re.compile('^[0-9]$')
endings = (".", "!", "?", '."', '!"', '?"', '.”', '?”', '!”')
false_starts = ("*", ":", "'", "”", "：", "|", "\\", ";", "-", "(", ")", ",")  #

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default="data/conan_hscnkp_retrieved.csv")
    parser.add_argument('--num_setence_selector', type=int, default=5, help='number of setences to be selected')
    parser.add_argument('--num_document_selector', type=int, default=25, help='number of documents to be selected')
    parser.add_argument('--metric_type', type=str, default='rougeL', help="'rougeL' or 'rouge1'")
    parser.add_argument('--kp_type', type=str, default='keyphrase', help="'keyphrase', 'hscn")
    parser.add_argument('--write_knowl_path', type=str, default="data/retrieved_KN_sentence/hscnkp")
    parser.add_argument('--outputfile', type=str, default="data/conan_hscnkp_top5kn.csv")
    parser_args = parser.parse_args()
    return parser_args

def clean_text(text):
    t = text.replace("’", "'").replace("“", "").replace("”", "").replace("@", "").replace("\n", "").replace("–", "-")
    t = t.replace("‑", "-").replace("…", "...").replace("•", "").replace("‘", "'")
    t = t.replace("â\x80\x99", "").replace("â\x80\x9d", '"')
    t = t.replace("<unk>", "")
    t = t.replace("@-@", "-").replace("@,@", ",").replace("@.@", ".").strip()
    t = bytes(t, 'utf-8').decode('utf-8', 'ignore')
    return " ".join(t.split())

@Language.component("component")
def custom_seg(doc):
    prev = doc[0].text
    length = len(doc)
    for index, token in enumerate(doc):
        if (token.text == '.' and boundary.match(prev) and index != (length - 1)):
            doc[index + 1].sent_start = False
        prev = token.text
    return doc

def get_rouge(sent, hskpcn, metric_type):
    """get ROUGE1 ('rouge1' or 'rougeL) -F1 between selected sentences and 'HS+KP+CN' """
    scorer_rouge = rouge_scorer.RougeScorer([metric_type], use_stemmer=True)
    scores = scorer_rouge.score(sent, hskpcn)
    return scores[metric_type][2]  # ROUGE1-F1

def top_n_important_sentence_selector(doc, hskpcn, n, metric_type):
    score = []
    for sent in doc:
        if not sent.strip().startswith(false_starts) and sent.strip().endswith(endings) and "unk" not in sent:
            sent_list = sent.strip().split()
            if len(sent_list) > 10:
                score.append(get_rouge(sent, hskpcn, metric_type))
            else:
                score.append(-10000)
        else:
            score.append(-10000)
    top_n_important_sentences = sorted(zip(score, doc), reverse=True)[:n]  # could be greedily maximizing the ROUGE1-F1 between selected sentences
    top_n_sentences = ""
    i = 0
    for ele in top_n_important_sentences:
        if ele[1] not in top_n_sentences and i < (n + 1):
            top_n_sentences += ele[1] + " <EOS> "
            i += 1
    return top_n_sentences

def main(df, knowl_path, outputfile, kp_type, num_document_selector, num_setence_selector, metric_type):
    f_Know = open(f'{knowl_path}.txt', "w")
    josnl_outfile = open(f'{knowl_path}.jl', 'w')       
    
    for index, row in df.iterrows():
        print("Current id: ", row['cn_id'])
        doc_know = {}
        doc_know['cn_id'] = row['cn_id']
        doc_know['hateSpeech'] = row['hateSpeech'] 
        doc_know['counterSpeech'] = row['counterSpeech']
        doc_text = ""
        if row['num_doc_retrieved'] > 0:
            if kp_type != "keyphrase":
                query = row['hateSpeech'] + ", " + row['counterSpeech']
            else:
                query = row['hs_keyword'] + row['cn_keyword']

            with open('data/retrieved_KN/'+str(row['cn_id'])+'.json') as f:
                data = json.load(f)
            knowl = ""
            sentences_in_all_knowl = []
            i = 0
            for ele in data:
                title = clean_text(ele["title"][0]) if "title" in ele.keys() else ""
                summary = clean_text(ele["summary"][0]) if "summary" in ele.keys() else ""
                text = clean_text(ele["text"][0])
                if title not in knowl and i < num_document_selector:
                    knowl += text
                    i += 1
                else:
                    break
                sentences_in_all_knowl += set(sentence_spliter(text))
            topn = top_n_important_sentence_selector(sentences_in_all_knowl, query, num_setence_selector, metric_type)
            doc_text += topn
            f_Know.write(str(doc_text) + "\n")
            f.close()
        else:
            f_Know.write("\n")
        doc_know['kn_sentence'] = doc_text
        df.loc[index,'kn_sentence_hscnkp'] = doc_text
        json.dump(doc_know, josnl_outfile)
        josnl_outfile.write('\n')
    df.to_csv(outputfile, index=False)
    f_Know.close()
    josnl_outfile.close()

def sentence_spliter(text):
    doc = nlp(text, disable=['ner'])  # , 'parser'
    sentence_list = []
    for sentence in doc.sents:
        sentence_list.append(sentence.text)
    return sentence_list


if __name__ == '__main__':

    args = parse_args()

    nlp = spacy.load("en_core_web_sm")

    nlp.max_length = 1500000
    boundary = re.compile('^[0-9]$')
    
    nlp.add_pipe("component", before='parser')
    
    df = pandas.read_csv(args.input_path)
    main(df, args.write_knowl_path, args.outputfile, args.kp_type, args.num_document_selector, args.num_setence_selector, args.metric_type)


