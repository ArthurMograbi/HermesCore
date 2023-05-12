import matplotlib.pyplot as plt
import pandas as pd
import json
import re


f = open("receivedlog.txt",'r',encoding='utf8')
txt = f.read()

f.close()

ol = txt.split("{\"_data")


nol = ["{\"_data"+i for i in ol[1:]] #skip the first cuz its empty

jl = [json.loads(i) for i in nol]


words = {}

for j in jl:
    j['body'] = re.sub(r'[!@#$%&*-?\n]',' ',j['body'])
    msgwords = [i.lower() for i in j['body'].split(" ") if len(i)>0]
    for w in msgwords:
        w = w.strip()
        if w in words:
            words[w]+=1
        else:
            words[w]=1


nonwords = ['e','de','a','que','do','o','com','não','da','na','em','no','é','sua'
            'eu','por','para','uma','um','sua','seu','vc','você','sou','como','os','as'
            'pra','me','se','mas','pelo','te','nossa','pela','dos','boa','tarde','noite',
            'eu','esse','também','tmb','olá','à']

for nw in nonwords:
    if nw in words:
        words.pop(nw)
        

df = pd.DataFrame({'word':list(words.keys()),'count':list(words.values())})

df = df.sort_values('count',ascending=False)

df = df.reset_index(drop=True)

from wordcloud import WordCloud
import matplotlib.pyplot as plt

font_path = 'resources/VeraMono.ttf'
# Create a dictionary of words and their corresponding frequencies
word_freq = dict(zip(df.word, df['count']))

# Generate the word cloud
wordcloud = WordCloud(width = 800, height = 800, background_color ='white', 
                min_font_size = 10,font_path=font_path).generate_from_frequencies(word_freq)

# Plot the word cloud
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
  
plt.show()

