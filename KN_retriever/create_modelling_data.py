"""
Extract top-5 sentences from 6 and add them to CONAN data.
"""

import pandas, linecache

def parse_args():
    """Parses Command Line Args"""
    parser = argparse.ArgumentParser(description="Retrieve knowledge articles from solr")
    parser.add_argument('--input_filename', type=str, default = "conan_hscnkp_kn_retrieved.csv", help = "help='file name for input data")
    parser.add_argument('--train_filename', type=str, default="KN_CONAN_final_data/hscnkp_train.csv", help='file name for train data')
    parser.add_argument('--valid_filename', type=str, default="KN_CONAN_final_data/hscnkp_valid.csv", help='file name for valid data')
    parser.add_argument('--test_filename', type=str, default="KN_CONAN_final_data/hscnkp_test.csv", help='file name for test data')
    parser_args = parser.parse_args()
    return parser_args

def main(df, train_filename, valid_filename, test_filename):
    train_file = open(f'{train_filename}.txt', "w")
    valid_file = open(f'{valid_filename}.txt', "w")
    test_file = open(f'{test_filename}.txt', "w")
    for index, row in df.iterrows():
        if row['split'] = 'train':
            train_file.write("<HS> " + row['hateSpeech'] + " <knowl> " + row['kn_sentence_hscnkp'] + " <CN> " + row[counterSpeech] + "\n")
        if row['split'] = 'valid':
            valid_file.write("<HS> " + row['hateSpeech'] + " <knowl> " + row['kn_sentence_hscnkp'] + " <CN> " + row[counterSpeech] + "\n")
        if row['split'] = 'test':
            test_file.write("<HS> " + row['hateSpeech'] + " <knowl> " + "\n")

if __name__ == '__main__':

    args = parse_args()
    
    df = pandas.read_csv(args.input_filename)
    main(df, args.train_filename, args.valid_filename, args.test_filename)

