import re
import pandas as pd
from matplotlib import pyplot as plt

import bibtexparser

with open('Bibtex.txt') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

for entry of bib_database.entries():
    print(entry)
# with open("Bibtex.txt",'r') as rf:
#     data = rf.read()
# import bibtexparser

# with open('bibtex.bib') as bibtex_file:
#     bib_database = bibtexparser.load(bibtex_file)
# # year=[]
# # keyword=[]
# # month=[]
# # biblist = [x for x in data.split('@INPROCEEDINGS')]
# # dic={}
# # for bib in biblist:
# #     if re.search("year={",bib) is not None:
# #         p =re.search("year={",bib).span()[0]
# #         year.append(int(bib[re.search("year={",bib).span()[1]:re.search("year={",bib).span()[1]+4]))
# #         keyword+=bib[re.search("keywords={.*}",bib).span()[0]+10:re.search("keywords={.*}",bib).span()[1]-1].split(';')
        

# # # print(([Counter(x.split(';')) for x in keyword]))
# # counts = Counter(keyword)
# # new = plt.figure(2)
# # plt.bar(counts.keys(),counts.values())
# # plt.show()

# # df = pd.DataFrame({'year':year})
# # plt.style.use('fivethirtyeight')
# # df.hist()
# # plt.show()





