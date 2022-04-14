""""""

import pandas, linecache

def read_data(filename, index):
    line = linecache.getline(filename, index+1)
    return line.replace("\n", "").replace("â\x80\x9c", "")

def main(id, kn_file, n=5):
    text = read_data(kn_file, id).split(" <EOS> ")
    KN = ""
    i = 1
    if text != ['']:
        if len(text) >= n:
            for ele in text:
                if i < n+1:
                    if ele != '':
                        KN += ele + " <EOS> "
                        i += 1
                else:
                    return pandas.Series([KN, n])
        else:
            print(id, ": ", text)
            for ele in text:
                if ele != '':
                    KN += ele + " <EOS> "
            return pandas.Series([KN, len(text)])
    else:
      return pandas.Series(["", 0])

if __name__ == '__main__':

    df1 = pandas.read_excel("CONAN_hscnkp.xlsx")
    kn_file1 = "retrieved_KN_sentence/top40_KN_sentences_first25_doc_hscnkp.txt"
    df1[['KN', 'num_KN']] = df1.apply(lambda x: main(x['ID'], kn_file1, 5), axis=1)
    df1.to_excel("CONAN_hscnkp_kn_retrieved.xlsx", index=False)

