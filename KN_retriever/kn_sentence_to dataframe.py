"""
Extract top-5 knowldge sentences and add them to CONAN data.
"""

import pandas, linecache

def parse_args():
    """Parses Command Line Args"""
    parser = argparse.ArgumentParser(description="Retrieve knowledge articles from solr")
    parser.add_argument('--data_split', type=str, default="train", help='train, valid, test')
    parser.add_argument('--kn_dir', type=str, default="retrieved_KN_sentence/top40_KN_sentences_first25_doc_hscnkp.txt", help='directory to knowledge file')
    parser.add_argument('--input_filename', type=str, default = "data/conan_hscnkp.csv", help = "help='file name for input data")
    parser.add_argument('--output_filename', type=str, default="data/conan_hscnkp_kn_retrieved.csv", help='file name for output data')
    parser.add_argument('--num_setence', type=int, default=5, help='number of setence to be selected')
    parser_args = parser.parse_args()
    return parser_args

def read_data(filename, index):
    line = linecache.getline(filename, index+1)
    return line.replace("\n", "").replace("â\x80\x9c", "")

def main(cn_id, kn_file, num_setence):
    text = read_data(kn_file, cn_id).split(" <EOS> ")
    KN = ""
    i = 1
    if text != ['']:
        if len(text) >= num_setence:
            for ele in text:
                if i < num_setence+1:
                    if ele != '':
                        KN += ele + " <EOS> "
                        i += 1
                else:
                    return pandas.Series([KN, num_setence])
        else:
            print(id, ": ", text)
            for ele in text:
                if ele != '':
                    KN += ele + " <EOS> "
            return pandas.Series([KN, len(text)])
    else:
        return pandas.Series(["", 0])

if __name__ == '__main__':
    args = parse_args()
    
    df = pandas.read_csv(args.input_filename)
    # df = df[df['split'] == args.data_split]
    df[['KN', 'num_KN']] = df.apply(lambda x: main(x['cn_id'], args.kn_dir, args.num_setence), axis=1)
    df.to_csv(args.output_filename, index=False)

