from django.shortcuts import render,redirect
from .forms import UploadFileForm
import matplotlib.pyplot as plt, mpld3
import pandas as pd
from collections import OrderedDict
import bibtexparser
import wordcloud
from wordcloud import WordCloud, STOPWORDS


from django.http import HttpResponse


def handle_uploaded_file(f):
    with open('bibtext.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return redirect('graph/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})



def graph(request):
    with open('bibtext.txt','r',encoding='utf8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
        df = pd.DataFrame(bib_database.entries)
        pages_count = {}
    
    df.pages
    maxValue=0
    for i in df.pages:
        try:
            x,y = map(int,i.split('-'))
            maxValue= max(maxValue,y-x)
        except:
            continue

    if(maxValue>100):
        divider=10
    elif(maxValue>50):
        divider=5
    elif(maxValue>20):
        divider =2
    else:
        divider=1
    for i in df.pages:
        try:
            x,y = map(int,i.split('-'))
            if(divider!=1):
                temp=int((y-x)/divider)
                pageWidthCluster=str(temp*divider)+"-"+str(temp*divider+divider-1)
            else:
                pageWidthCluster=str(y-x)
                pages_count[pageWidthCluster] = pages_count.get(pageWidthCluster,0)+1
        except:
            continue

    od = OrderedDict(sorted(pages_count.items()))

    fig1 = plt.figure(figsize = (10, 5)) 
    plt.bar(list( od.keys() ), list( od.values() ), color ='royalblue',  width = 0.4) 
    plt.xlabel("Pages") 
    plt.ylabel("Count") 
    plt.title("Number of pages in different papers") 
    
    g = mpld3.fig_to_html(fig1)


    month_to_paper = dict()
    monthsMapper = {'jan':'Jan','january':'Jan','feb':'Feb','february':'Feb','march':'Mar','mar':'Mar','april':'Apr','apr':'Apr','may':'May','june':'Jun','jun':'Jun','july':'Jul','jul':'Jul','aug':'Aug','august':'Aug','sep':'Sep','september':'Sep','oct':'Oct','october':'Oct','november':'Nov','nov':'Nov','december':'Dec','dec':'Dec'}

    for i in df.month.dropna():
        if i.lower() in monthsMapper:
            key=monthsMapper[i.lower()]
            month_to_paper[key] = month_to_paper.get(key,0)+1

    fig2 = plt.figure(figsize = (10, 5)) 


    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    month_num = dict(zip(months, range(12)))

    def compareMonth(month):
        return month_num[month]
    sorted_month=dict(sorted(month_to_paper.items(), key=lambda x: compareMonth(x[0])))
    plt.bar(list( sorted_month.keys() ), list( sorted_month.values() ), color ='crimson',  width = 0.4) 

    plt.xlabel("Month") 
    plt.ylabel("Count") 
    plt.title("Number of papers in different months")

    g += mpld3.fig_to_html(fig2)

    year_to_paper = {}
    for i in df.year.dropna():
        year_to_paper[i] = year_to_paper.get(i,0)+1

    fig3 = plt.figure(figsize = (10, 5))
    sorted_year = OrderedDict(sorted(year_to_paper.items()))

    plt.bar(list( sorted_year.keys() ), list( sorted_year.values() ), color ='crimson',  width = 0.4) 
    
    plt.xlabel("Year") 
    plt.ylabel("Count") 
    plt.title("Number of papers published in different years") 

    g += mpld3.fig_to_html(fig3)


    
    months = list(sorted_month.keys())

    year_to_month_papers = {}
    for i in range(len(df)):
        if df.year[i] not in year_to_month_papers:
            year_to_month_papers[df.year[i]] = dict.fromkeys(months,0)
        else:
            try:
                key=monthsMapper[df.month[i].lower()]
                year_to_month_papers[df.year[i]][key] = year_to_month_papers[df.year[i]][key]+1
            except:
                continue
    sorted_year_to_month_papers=OrderedDict(sorted(year_to_month_papers.items(), key=lambda x: x[0]))
    df2 = pd.DataFrame(sorted_year_to_month_papers)

    ax = df2.plot.bar(figsize=(12,8),width = 0.4,stacked=True)
    ax.set_xlabel("Month")
    ax.set_ylabel("No.of Papers")
    fig4 = ax.get_figure()

    g += mpld3.fig_to_html(fig4)

    ax = df2.T.plot.bar(figsize=(12,8),width = 0.4,stacked=True)
    ax.set_xlabel("Year")
    ax.set_ylabel("No.of Papers")
    fig5 = ax.get_figure()

    g += mpld3.fig_to_html(fig5)



    keyWordDict={}
    for index, row in df.iterrows():
        for keyWord in row['keywords'].split(';'):
            for individualWord in keyWord.split(' ') : 
                lowercaseKey=individualWord.lower()
                if lowercaseKey not in keyWordDict:
                    keyWordDict[lowercaseKey]={
                        'count':1,
                        'yearsMap':{
                            row['year'] :1
                        }
                    }
                else:
                    oldMap=keyWordDict[lowercaseKey]
                    oldMap['count']=oldMap['count']+1
                    oldYearsMap=oldMap['yearsMap']
                    oldYearsMap[row['year']]= oldYearsMap.get(row['year'],0)+1
                    oldMap['yearsMap']=oldYearsMap
                    keyWordDict[lowercaseKey]=oldMap


    sortedKeyWord = OrderedDict(sorted(keyWordDict.items(), key=lambda kv: kv[1]['count'], reverse=True))

    fig6 = plt.figure(figsize = (12, 8))
    for index, (key, value) in enumerate(sortedKeyWord.items()):
        # print(index, key, value)
        temp = OrderedDict(sorted(value['yearsMap'].items(), key=lambda kv: kv[0]))
        plt.plot(list(temp.keys()), list(temp.values()), label = key, marker='o')
        if index==5:
            break
    plt.xlabel('Years')
    plt.ylabel('Count')
    plt.title('Keyword historical trend ')
    plt.legend()

    g += mpld3.fig_to_html(fig6)


    vocab_w_freq = []

    for i in df.keywords:
        r = i.split(';')
        vocab_w_freq.extend(r)
    vocab = set( vocab_w_freq )



    stopwords = set(STOPWORDS) 
    vocab_w_freq_str = " ".join(vocab_w_freq)


    
    wordcloud = WordCloud(width = 800, height = 800, background_color ='white', stopwords = stopwords, min_font_size = 10).generate(vocab_w_freq_str) 
    
    # plot the WordCloud image
    fig5 = plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 

    g += mpld3.fig_to_html(fig5)


    
    return render(request,'graph.html',{'graph':g})

