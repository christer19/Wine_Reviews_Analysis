import pandas as pd
import numpy as np
import hvplot.pandas
import holoviews as hv
import panel as pn
import panel.widgets as pnw
from PIL import Image

wine = pd.read_csv('clean_wine.csv')

# Adding style for the Panels
css = '''
.panel-widget-box {
  background: #fdfdfd;
  border-radius: 5px;
  border: 5px solid black;
}
.panel-button{
  background-color: #b300b3;
  color: white;
}
'''
pn.extension(raw_css=[css])

#pn.config.raw_css.append(css)


mar = (5,5,5,5)

def set_toolbar_options(plot, element):
    bokeh_plot = plot.state
    bokeh_plot.toolbar.autohide = True
    bokeh_plot.toolbar_location="above"
    bokeh_plot.toolbar.logo = None
    #bokeh_plot.toolbar_location = None

p = Image.open('glasses-306346_1280.png')
logo  = pn.pane.PNG(p,width=150, height=127)
title = pn.pane.HTML("<b>Wines Reviews Analysis</b> by Juan Marte" )
desc = pn.pane.HTML("""
   <p><b>Overview: </b>
   The goal of this analysis is to understand in a visual context the trends and patterns found in the wine reviews dataset. T
   his dataset contains 130,000 reviews of different type of wines, published by the <a href="https://www.winemag.com/">Wine Enthusiast Magazine</a>. 
   It includes the wine name,  country, variety, price, amongst others descriptors for each reviewed wine.</p>
   
  <p>The original data was transformed to simplify the analysis: to avoid confusion points was renamed rating, added new columns for vintage, price range, rating range,grape variety
   and description lengh other than those the only columns left are country, description, rating(points), price, and taster_name. A summary of the final data set can be seen by clicking the blue button.</p>                                                                                                           
                                                                                                           """, width=1200)

top = pn.Row(logo, pn.Column(title, desc), css_classes=['panel-widget-box'], width=1440, margin=(20,0,0,0))

rb = pnw.Button(name='Click For Random Sample', button_type='primary', css_classes=['panel_button'])

def rand_df():
    df = wine.sample(10).hvplot.table(width=500, height = 100)
    return df

ppp = pn.pane.HoloViews()

def b(event):

    ppp.object = rand_df()       


rb.on_click(b)

w_tab = pn.Column(rb, ppp, css_classes=['panel-widget-box'], margin=0)

#Histogram and descriptive statistics


variable = pnw.Select(name='Select', options=['rating', 'desc_length', 'price', 'vintage'], width=75)
limits = pnw.RangeSlider(name='Limits', start=80, end=100, value=(80, 100), step=1, orientation='horizontal')
bins = pnw.IntSlider(name='bins', value=20, start=10, end=100, orientation='vertical', width=50)

def cb(event):    
    if event.new == 'price':        
        limits.value = (int(wine['price'].min()),int(wine['price'].max()))
        limits.start = int(wine['price'].min())
        limits.end = int(wine['price'].max())
        limits.step = 50

    elif event.new == 'rating':
        limits.value = (int(wine['rating'].min()),int(wine['rating'].max()))
        limits.start = int(wine['rating'].min())
        limits.end = int(wine['rating'].max())
        limits.step = 1
        
        
    elif event.new == 'desc_length':
        limits.value = (int(wine['desc_length'].min()),int(wine['desc_length'].max()))
        limits.start = int(wine['desc_length'].min())
        limits.end = int(wine['desc_length'].max())
        limits.step = 10
        
        
    elif event.new == 'vintage':
        limits.value = (1900,int(wine['vintage'].max()))
        limits.start = int(wine['vintage'].min())
        limits.end = int(wine['vintage'].max())
        limits.step = 10
    else:
        pass
    
variable.param.watch(cb,'value')

@pn.depends(variable, limits, bins)
def w_hist(variable, limits, bins):
    
    h_dat =  wine.loc[(wine[variable]>=limits[0]) & (wine[variable]<=limits[1])]
    h = h_dat.hvplot.hist(y=variable, bins=bins, height=450, color='violet', hover_alpha=0.5, width=600, title='Histogram of '+variable)
    h.opts(hooks=[set_toolbar_options], backend='bokeh')
    return h


@pn.depends(variable)
def get_stats(variable='rating'):   
    df =  np.round(wine[variable].describe(),2).reset_index().rename({'index':'Stats'}, axis=1).T.hvplot.table(width=400, title='Descriptive Statistics')
    return df
insight_h = pn.pane.Markdown('''The distribution of wines prices on the data is extremely skewed to the right that's because the prices range from $4 up to $3300. 
                Also notice that 75% of all the wines reviewed cost less than 43 dollars. the distributions for rating and reviwed lengths seem normal.''', width=200, )

hg = pn.Column(pn.Row(pn.Column(variable,pn.Row(bins)),w_hist),limits,pn.Row(get_stats,insight_h), css_classes=['panel-widget-box'], width=700, height=700, margin=mar)


#Scatter plot
x = pnw.Select(name='Select X axis', options=['rating', 'desc_length', 'price', 'vintage'], sizing_mode="stretch_width" , max_width=100)
y = pnw.Select(name='Select Y axis', options=['rating', 'desc_length', 'price', 'vintage'], sizing_mode="stretch_width", max_width=100 )

@pn.depends(x,y)
def w_scatter(x='price',y='rating'):
    sp = wine.hvplot.scatter(x=x, y=y, width=500, height=400, hover=False, color='purple', title= x +' vs '+ y + ' scatter plot' )
    sp.opts(hooks=[set_toolbar_options], backend='bokeh')
    return sp

@pn.depends(x,y)
def get_corr(x,y):
    return 'Correlation Coefficient: ' + str(np.round(np.corrcoef(x=wine[x],y=wine[y])[1][0],2))

sp_insight = ''' 
                The doesn't seem to be a high correlation between the numerical variables as shown in the correlation matrix. The only slighlty correlated is description length with rating,
                which seems to imply that longer the review gets that higher the rating for the specific wine.
            '''

sp = pn.Column(pn.Row(x,y, get_corr),w_scatter,sp_insight, css_classes=['panel-widget-box'], width=500, height=550, margin=mar)


#Taster comparison
taster = pn.widgets.MultiChoice(name='Tasters Names', value=list(wine['taster_name'].value_counts().index),options=list(wine['taster_name'].value_counts().index))

@pn.depends(taster)
def taster_box(taster=list(wine['taster_name'].value_counts().index)):
    taste = wine.loc[wine['taster_name'].isin(taster)]
    #orde = taste.groupby('taster_name')['rating'].median().sort_values(ascending=False).index
    bp = taste.hvplot.box(by='taster_name', y = 'rating', rot=45, width=1000, height=450, hover_cols=['taster_name'], color='#ac39ac')
    bp.opts(hooks=[set_toolbar_options], backend='bokeh')
    return bp

b_insight = '''
                This boxplot shows a comparison of the distribution of ratings for each taster. Notice that they are very equated, except for 3 of them: Alexander Peartree tends to rate the wines with lower
                scores, Anne Krebiehl rate them higher than the others and Christina Pickard is very conservative with her rating as she keeps on the range 87-88 with only a few outliers.
            '''

boxen = pn.Row(pn.Column(taster_box, b_insight), taster,  width=1440, height=550, css_classes=['panel-widget-box'], margin=mar)


#Glass of words
glass = Image.open('glass_of_words.PNG')
glass = pn.pane.PNG(glass, width = 200, height = 500)

text = '''The glass has the most common words and phrases found on all the descriptions from the wine reviews, the size of the word represent 
            the frequency of each term. It looks like tasters like to use; full bodied, black cherry and black fruit very often to describe the wine flavor, amonght other words.'''

glass =  pn.Column(glass, text, width = 240, height = 700, css_classes=['panel-widget-box'], margin=mar)


#Vintage line chart
vgr = pd.DataFrame(wine.groupby(['vintage','grape_variety'])['rating'].mean().reset_index())

year = pnw.RangeSlider(name='yearRange', start=1900, end=2020, value=(1900, 2020), step=10, width=1200)

@pn.depends(year)
def lp(year):
    l = vgr.loc[(vgr['vintage']>=year[0]) & (vgr['vintage'] <= year[1])].hvplot.line(x='vintage',
                                                                                     y='rating', 
                                                                                     by='grape_variety', 
                                                                                     color=['red','gray','plum'], 
                                                                                     title='Average Ratings by Vintage Year', 
                                                                                     width=1200, height=400) 
    s = vgr.loc[(vgr['vintage']>=year[0]) & (vgr['vintage'] <= year[1])].hvplot.scatter(x='vintage',
                                                                                        y='rating', 
                                                                                        by='grape_variety', 
                                                                                        color=['red','gray','plum'], 
                                                                                        title='Average Ratings by Vintage Year',
                                                                                        width=1200, height=400)
    
    p = l * s
    p.opts(hooks=[set_toolbar_options], backend='bokeh')
    
    return p

text = '''
        <br><br> Judging by the line graph, it seems that the ratings peak for both types of wines from the 1970 and then goes down after that period. It is possible to check different periods using the slider
        but it seems that white wines rate better overall. 
        '''

vp = pn.Column(year,lp, text, css_classes=['panel-widget-box'], width=1440, margin=mar)


#Bottom part
p = Image.open('grapes-34298_640.png')
logo  = pn.pane.PNG(p,width=150, height=127)
desc = pn.pane.HTML("""
  <b>Credits and Resources: </b><br>
  <ul>
   <li>This analysis and the dashboard were made using Python 3.8, with the help of the libraries: numpy, pandas, matplotlib, seaborn, nltk, PIL,WordCloud and panel.<br></li>   
   <li>The picture used to draw the glass and logos were taken from <a href=https://pixabay.com/vectors/search/wine/>pixalbay.com</a><br></li>
   <li>The data for the grapes variety was obtained from <a href=https://en.wikipedia.org/wiki/List_of_grape_varieties>https://en.wikipedia.org/wiki/List_of_grape_varieties.</a></li>
   <li>Credits to Doung Vu for <a href='https://www.datacamp.com/community/tutorials/wordcloud-python'>Generating WordClouds in Python</a></li>
   <li> The data cleaning process, exploratory data analysis and app prototype for the wine reviews data set can be found on the <a href=https://github.com/jm1988/Wine_Reviews_Analysis>Wine Reviews Analysis git hub repository</a>.</li>
  </ul>                                                                                                           
                                                                                                           """, width=1200)

bottom = pn.Row(desc, logo, css_classes=['panel-widget-box'], width=1440, margin=mar)

#Main dash
dash = pn.Column(top,pn.Row(pn.Column(w_tab,sp),hg ,glass), boxen, vp, bottom, css_classes=['panel-widget-box'])

dash.servable()