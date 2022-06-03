"""
Create train, valid and test data.
"""

import argparse
import pandas
import linecache

def parse_args():
    """Parses Command Line Args"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_filename', type=str, default = "data/conan_hscnkp_top5kn.csv", help = "help='file name for input data")
    parser.add_argument('--train_filename', type=str, default="data/KN_CONAN_final_data/hscnkp_train.csv", help='file name for train data')
    parser.add_argument('--valid_filename', type=str, default="data/KN_CONAN_final_data/hscnkp_valid.csv", help='file name for valid data')
    parser.add_argument('--test_filename', type=str, default="data/KN_CONAN_final_data/hscnkp_test.csv", help='file name for test data')
    parser_args = parser.parse_args()
    return parser_args

def main(df, train_filename, valid_filename, test_filename):
    train_file = open(f'{train_filename}.txt', "w")
    valid_file = open(f'{valid_filename}.txt', "w")
    test_file = open(f'{test_filename}.txt', "w")
    for index, row in df.iterrows():
        kn = row['kn_sentence_hscnkp'].replace(" <EOS> ", " ")
        if row['split'] == 'train':
            train_file.write("<HS> " + row['hateSpeech'] + " <knowl> " + kn + "<CN> " + row['counterSpeech'] + "\n")
        if row['split'] == 'valid':
            valid_file.write("<HS> " + row['hateSpeech'] + " <knowl> " + kn + "<CN> " + row['counterSpeech'] + "\n")
        if row['split'] == 'test':
            test_file.write("<HS> " + row['hateSpeech'] + " <knowl> " + kn + "<CN> " + "\n")

if __name__ == '__main__':

    args = parse_args()
    
    df = pandas.read_csv(args.input_filename)
    df = df[df['num_doc_retrieved'] > 0]
    main(df, args.train_filename, args.valid_filename, args.test_filename)

