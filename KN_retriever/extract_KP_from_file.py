import pandas

"""read keyphrases computed from KeyphraseDigger to csv"""


def extract_kp(directory, cn_id):
    df_kp = pandas.read_csv(directory+str(cn_id)+".tsv", sep="\t")
    kp = df_kp["keyword"].tolist()
    num_kp = len(kp)     # calculate the number of keyphrases
    if num_kp > 0:
        kp = ', '.join(kp)
    else:
        kp = ''
    return kp


if __name__ == '__main__':
    df = pandas.read_csv("CONAN.csv")
    df['cn_keywords'] = df.apply(lambda x: extract_kp("CN/", x['cn_id']), axis=1)
    df['hs_keywords'] = df.apply(lambda x: extract_kp("HS/", x['cn_id']), axis=1)
    df.to_csv("CONAN_hscnkp.csv", index=False)