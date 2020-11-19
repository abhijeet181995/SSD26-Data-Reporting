from django.shortcuts import render,redirect
from .forms import FileFieldForm
import matplotlib.pyplot as plt, mpld3
import pandas as pd
import os
from collections import OrderedDict
import bibtexparser
import wordcloud
from wordcloud import WordCloud, STOPWORDS


from django.http import HttpResponse


def handle_uploaded_file(files):
    counter=1
    for file in files:
        name= "temp/"+"bibtext"+str(counter)+".txt"
        with open(name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        counter+=1
            


def upload_file(request):
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            handle_uploaded_file(files)
            return redirect('graph/')
    else:
        form = FileFieldForm()
    return render(request, 'upload.html', {'form': form})


def plotPagesCount(df):
    maxValue=0
    pages_count = {}
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

    fig = plt.figure(figsize = (10, 5)) 
    plt.bar(list( od.keys() ), list( od.values() ), color ='royalblue',  width = 0.4) 
    plt.xlabel("Pages") 
    plt.ylabel("Count") 
    plt.title("Number of pages in different papers") 
    return mpld3.fig_to_html(fig)

def plotMonthYearAnalysis(df):
    month_to_paper = dict()
    monthsMapper = {'jan':'Jan','january':'Jan','feb':'Feb','february':'Feb','march':'Mar','mar':'Mar','april':'Apr','apr':'Apr','may':'May','june':'Jun','jun':'Jun','july':'Jul','jul':'Jul','aug':'Aug','august':'Aug','sep':'Sep','september':'Sep','oct':'Oct','october':'Oct','november':'Nov','nov':'Nov','december':'Dec','dec':'Dec'}

    for i in df.month.dropna():
        if i.lower() in monthsMapper:
            key=monthsMapper[i.lower()]
            month_to_paper[key] = month_to_paper.get(key,0)+1

   
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month_num = dict(zip(months, range(12)))
    def compareMonth(month):
        return month_num[month]
    sorted_month=dict(sorted(month_to_paper.items(), key=lambda x: compareMonth(x[0])))
    fig1 = plt.figure(figsize = (10, 5)) 
    plt.bar(list( sorted_month.keys() ), list( sorted_month.values() ), color ='crimson',  width = 0.4) 
    plt.xlabel("Month") 
    plt.ylabel("Count") 
    plt.title("Number of papers in different months")

    year_to_paper = {}
    for i in df.year.dropna():
        year_to_paper[i] = year_to_paper.get(i,0)+1

    fig2 = plt.figure(figsize = (10, 5))
    sorted_year = OrderedDict(sorted(year_to_paper.items()))

    plt.bar(list( sorted_year.keys() ), list( sorted_year.values() ), color ='crimson',  width = 0.4) 
    
    plt.xlabel("Year") 
    plt.ylabel("Count") 
    plt.title("Number of papers published in different years") 


    
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
    fig3 = ax.get_figure()
    ax = df2.T.plot.bar(figsize=(12,8),width = 0.4,stacked=True)
    ax.set_xlabel("Year")
    ax.set_ylabel("No.of Papers")
    fig4 = ax.get_figure()

    return mpld3.fig_to_html(fig1),mpld3.fig_to_html(fig2),mpld3.fig_to_html(fig3),mpld3.fig_to_html(fig4)

def plotHistoricalTrend(df):
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
    fig1 = plt.figure(figsize = (12, 8))
    totalCountDict={}
    for index, (key, value) in enumerate(sortedKeyWord.items()):
        # print(index, key, value)
        temp = OrderedDict(sorted(value['yearsMap'].items(), key=lambda kv: kv[0]))
        totalCountDict[key]=value['count']
        plt.plot(list(temp.keys()), list(temp.values()), label = key, marker='o')
        if index==5:
            break
    plt.xlabel('Years')
    plt.ylabel('Count')
    plt.title('Top 5 Keyword historical trend ')
    plt.legend()
    sortedCountDict = OrderedDict(sorted(totalCountDict.items(), key=lambda kv: kv[1]))
    fig2 = plt.figure(figsize = (12, 8))
    plt.pie(list(sortedCountDict.values())[:5], labels = list(sortedCountDict.keys())[:5]) 
    plt.title('Top 5 keywords ')
    return mpld3.fig_to_html(fig1),mpld3.fig_to_html(fig2)


def plotWordCloud(df):
    vocab_w_freq = []
    for i in df.keywords:
        r = i.split(';')
        vocab_w_freq.extend(r)
    vocab = set( vocab_w_freq )
    stopwords = set(STOPWORDS) 
    vocab_w_freq_str = " ".join(vocab_w_freq)
    wordcloud = WordCloud(width = 800, height = 800, background_color ='white', stopwords = stopwords, min_font_size = 10).generate(vocab_w_freq_str) 
    fig = plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    return mpld3.fig_to_html(fig)

def plotAuthor(df):
    author_count = {}
    for authors in df.author.dropna():
        for author in authors.split('and'):
            author_count[author] = author_count.get(author,0)+1
    fig = plt.figure(figsize = (12, 8))
    sorted_author_count=OrderedDict(sorted(author_count.items(), key=lambda x: x[1]),reverse=True)
    plt.pie(list(sorted_author_count.values())[:5], labels = list(sorted_author_count.keys())[:5]) 
    plt.title('Most publishing author ')
    return mpld3.fig_to_html(fig)


def graph(request):
    filelist = os.listdir('temp') 
    df_list = [  ]
    for file in filelist:
        f = open('temp/'+file, encoding="utf-8")
        bib_database = bibtexparser.load(f)
        df_ENTRY = pd.DataFrame(bib_database.entries)
        df_list.append(df_ENTRY)
        f.close()
        os.remove('temp/'+file)
    df = pd.concat(df_list,ignore_index=True)

    args={}
    graph1=plotPagesCount(df)
    graph2,graph3,graph4,graph5=plotMonthYearAnalysis(df)
    graph6,graph7=plotHistoricalTrend(df)
    graph8=plotWordCloud(df)
    graph9=plotAuthor(df)
    args['graph1']=graph1
    args['graph2']=graph2
    args['graph3']=graph3
    args['graph4']=graph4
    args['graph5']=graph5
    args['graph6']=graph6
    args['graph7']=graph7
    args['graph8']=graph8
    args['graph9']=graph9
    return render(request,'graph.html',args)

