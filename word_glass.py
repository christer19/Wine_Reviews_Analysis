#The function to create the glass of words.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PIL import Image
from matplotlib.pyplot import imshow

from nltk import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def words_glass(wine):
    text = " ".join(r for r in wine['description'])
    custom_stop_words = ['flavor','flavors','wine','drink']
    stop_words = set(stopwords.words('english'))
    stop_words.update(custom_stop_words)
    word_tokens = word_tokenize(text) 
    word_tokens = [w.lower() for w in word_tokens]
    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    maski = np.array(Image.open('wine-white.png'))
    text = " ".join(w for w in filtered_sentence)
    wordcloud = WordCloud(mask = maski, 
                        background_color='white', 
                        max_font_size=60, 
                        max_words=500, 
                        contour_width=3, 
                        contour_color='thistle', 
                        font_step = 5, colormap = 'gnuplot').generate(text)   
    
    fig = Figure(figsize=(6,10))
    ax = fig.add_subplot()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    fig.set_tight_layout(True)
    return fig