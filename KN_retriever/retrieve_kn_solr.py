"""retrieve relevant documents using keyphrases as queries with Solr"""

import argparse, pandas, json
import urllib.request

def parse_args():
    """Parses Command Line Args"""
    parser = argparse.ArgumentParser(description="Retrieve knowledge articles from solr")
    parser.add_argument('--data_split', type=str, default="train", help='train, valid, test')
    parser.add_argument('--output_dir', type=str, default="data/retrieved_KN_solr", help='directory to knowledge retrieved from solr')
    parser.add_argument('--input_filename', type=str, default = "data/conan_hscnkp_keyphrase.csv", help = "help='file name for input data")
    parser.add_argument('--output_filename', type=str, default="data/conan_hscnkp_keyphrase_kn_num.csv", help='file name for output data')
    parser.add_argument('--kp_type', type=str, default="hscn", help='types of keyphrase: hs, gen, hsgen, hscn')
    parser_args = parser.parse_args()
    return parser_args

def form_query(queries, boolean):
    query = ""
    for q in queries:
        if q == queries[-1]:
            query += 'text:"' + q + '"'
        else:
            query += 'text:"' + q + '" ' + boolean + ' '
    query = query.strip().replace('"', '%22').replace(" ", "%20").replace("&&", "%26%26").replace("||", "%7C%7C")
    link = "http://localhost:8989/solr/knowledgecollection/select?q=" + query + "&rows=25&wt=json"
    return link

def call_solr(hs_kp, cn_kp, boolean, kp_type):
    if kp_type == 'hscn':
        keyphrase = hs_kp + cn_kp
    elif kp_type == 'hs':      
        keyphrase = hs_kp
    query = form_query(keyphrase, boolean)
    connection = urllib.request.urlopen(query)
    response = json.load(connection)
    return response

def process_keyphrase(text):
    # clean special characters in keyphrases
    t = text.replace("'", "").replace("#", "").replace("@", "").replace("!", "")
    t = t.replace("’", "'").replace("“", "").replace("”", "").replace("?","?")
    t = t.replace("\xe8","e").replace("è","e")
    return t

def main(hs_kp, cn_kp, hs, cs, cn_id, output_dir, kp_type):

    if len(cs.split()) < 10:
        return 0

    print("Current id: ", cn_id)
    kn_output_path = f'{output_dir}/{cn_id}.json'

    # retrieve relevant document using keyphrases as queries with Solr
    if len(hs_kp) > 0 and len(cn_kp) > 0:
        json_list = []
        hskp = process_keyphrase(hs_kp).split(", ")
        cnkp = process_keyphrase(cn_kp).split(", ")
        boolean = "||"
        response = call_solr(hskp, cnkp, boolean, kp_type)
        while response['response']['numFound'] == 0:
            if len(hskp) > 0 and len(cnkp) > 0:
                if len(hskp) > len(cnkp):
                    hskp.pop()
                else:
                    cnkp.pop()
            elif len(hskp) > 0 and len(cnkp) == 0:
                hskp.pop()
            elif len(cnkp) > 0 and len(hskp) == 0:
                cnkp.pop()
            else:
                hskp = hs
                cnkp = cs
                boolean = "||"
            response = call_solr(hskp, cnkp, boolean, kp_type)
            
        # return retrieved document in json, one json file contains all the retrieved documents.
        # Each json is a list of dictionary containing "title", "text" and "summary" (if exists)
        # as keys and corresponding content as values
        for document in response['response']['docs']:
            element = {}
            if "title" in document.keys():
                element["title"] = document["title"]
            element["text"] = document["text"]
            if "summary" in document.keys():
                element["summary"] = document["summary"]
            json_list.append(element)
        with open(kn_output_path, 'w', encoding='utf-8') as f:
            json.dump(json_list, f)
        return response['response']['numFound']
    return 0

if __name__ == '__main__':
    
    args = parse_args()
    df = pandas.read_csv(args.input_filename, encoding='utf8')
    df = df.astype({"hs_keyword": str, "cn_keyword": str})
    # df = df[df['split'] == args.data_split]
    # df['num_doc_retrieved'] = df.apply(lambda x: main(x['hs_keyword'], x['generated_cn_keywords'], x['hateSpeech'], x['counterSpeech'], x['cn_id'], args.output_dir, args.kp_type), axis=1)
    df['num_doc_retrieved'] = df.apply(lambda x: main(x['hs_keyword'], x['cn_keyword'], x['hateSpeech'], x['counterSpeech'], x['cn_id'], args.output_dir, args.kp_type), axis=1)
    df.to_csv(args.output_filename, index=False)
    
    
