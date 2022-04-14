"""read keyphrases returned from KeyphraseDigger to csv"""

import pandas

def extract_keyphrase(directory, cn_id):
    df_kp = pandas.read_csv(directory+str(cn_id)+".tsv", sep="\t")
    kp = df_kp["keyword"].tolist()
    num_kp = len(kp)     # calculate the number of keyphrases
    if num_kp > 0:
        kp = ', '.join(kp)
    else:
        kp = ''
    return pandas.Series([kp, num_kp])


if __name__ == '__main__':
    df = pandas.read_csv("CONAN.csv")
    df[['CN_keyword', 'num_CN_keyword']] = df.apply(lambda x: extract_keyphrase("CN/", x['cn_id']), axis=1)
    df[['HS_keyword', 'num_HS_keyword']] = df.apply(lambda x: extract_keyphrase("HS/", x['cn_id']), axis=1)
    df.to_csv("CONAN_hscnkp.csv", index=False)
