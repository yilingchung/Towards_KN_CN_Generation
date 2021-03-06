"""read keyphrases returned from KeyphraseDigger to csv"""

import pandas

def extract_keyphrase(directory, cn_id):
    df_kp = pandas.read_csv(directory+str(cn_id)+".tsv", sep="\t")
    df_kp = df_kp.astype({"keyword": str})
    kp = df_kp["keyword"].tolist()
    num_kp = len(kp)     # calculate the number of keyphrases
    if num_kp > 0:
        kp = ', '.join(kp)
    else:
        kp = ''
    return pandas.Series([kp, num_kp])


if __name__ == '__main__':
    df = pandas.read_csv("data/conan.csv")
    df[['cn_keyword', 'num_cn_keyword']] = df.apply(lambda x: extract_kp("data/CN/", x['cn_id']), axis=1)
    df[['hs_keyword', 'num_hs_keyword']] = df.apply(lambda x: extract_kp("data/HS/", x['cn_id']), axis=1)
    df.to_csv("data/conan_hscnkp_keyphrase.csv", index=False)
