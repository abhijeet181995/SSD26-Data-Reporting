import re
import pandas as pd
from matplotlib import pyplot as plt

with open("Bibtex.txt",'r') as rf:
    data = rf.read()

year=[]


biblist = [x for x in data.split('@INPROCEEDINGS')]
dic={}
for bib in biblist:
    if re.search("year={",bib) is not None:
        year.append(int(bib[re.search("year={",bib).span()[1]:re.search("year={",bib).span()[1]+4]))

df = pd.DataFrame({'year':year})

# df.hist()
plt.style.use('fivethirtyeight') 
df.hist()
plt.show()


