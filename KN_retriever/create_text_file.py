"""This script prepares files to run keyphrase digger over.
It creates a txt file for each hate speech and counter narrative in CONAN."""

import pandas

def create_txt(output_directory, text, id):
    with open(output_directory+str(id)+".txt", "w") as f:
        f.write(text.strip())

if __name__ == '__main__':
    df = pandas.read_csv("data/CONAN.csv")
    df.apply(lambda x: create_txt("data/HS/", x['hateSpeech'], x['cn_id']), axis=1)
    df.apply(lambda x: create_txt("data/CN/", x['counterSpeech'], x['cn_id']), axis=1)
