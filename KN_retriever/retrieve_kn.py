"""retrieve relevant documents using keyphrases as queries with Solr"""

import argparse, pandas, json
import urllib.request

def parse_args():
    """Parses Command Line Args"""
    parser = argparse.ArgumentParser(description="Retrieve knowledge articles from solr")
    parser.add_argument('--data_split', type=str, default="train", help='train, valid, test')
    parser.add_argument('--output_dir', type=str, default="retrieved_KN", help='directory to knowledge retrieved from solr')
    parser.add_argument('--input_filename', type=str, default = "CONAN_hscnkp.csv", help = "help='file name for input data")
    parser.add_argument('--output_filename', type=str, default="CONAN_hscnkp_retrieved.csv", help='file name for output data')
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

def call_solr(hs_kp, cn_kp, gen_kp, boolean, kp_type):
    if kp_type == 'hscn':
        keyphrase = hs_kp + cn_kp
    elif kp_type == 'hsgen':
        keyphrase = hs_kp + gen_kp
    elif kp_type == 'hs':      
        keyphrase = hs_kp
    elif kp_type == 'gen':
        keyphrase = cn_kp
    query = form_query(keyphrase, boolean)
    connection = urllib.request.urlopen(query)
    response = json.load(connection)
    return response

def process_keyphrase(text):
    # clean special characters in keyphrases
    return text.replace("#", "").replace("@", "").replace("!", "").replace("’", "'").replace("“", "").replace("”", "").replace("?","?")

def main(num_hskp, num_cnkp, hs_kp, cn_kp, gen_kp, cn_id, output_dir, kp_type):
    print("Current id: ", cn_id)
    kn_output_path = f'{output_dir}/{str(id)}.json'

    # retrieve relevant document using keyphrases as queries with Solr
    if str(num_hskp) != "0" and str(num_cnkp) != "0":
        json_list = []
        hskp = process_keyphrase(hs_kp).split(", ")
        cnkp = process_keyphrase(cn_kp).split(", ")
        genkp = process_keyphrase(gen_kp).split(", ")
        boolean = "||"
        response = call_solr(hskp, cnkp, genkp, boolean, kp_type)
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
                hskp = process_keyphrase(hs_kp).split(", ")
                cnkp = process_keyphrase(cn_kp).split(", ")
                boolean = "||"
            response = call_solr(hskp, cnkp, genkp, boolean, kp_type)
            
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
        # return response['response']['numFound']

if __name__ == '__main__':
    args = parse_args()
    df = pandas.read_csv(args.input_filename)
    # df = df[df['split'] == args.data_split]
    df.apply(lambda x: main(x['num_HS_keyword'], x['num_CN_keyword'], x['HS_keyword'], x['CN_keyword'], x['generated_cn_keywords'], x['cn_id'], args.output_dir, args.kp_type), axis=1)
    # df.to_csv(args.output_filename)
