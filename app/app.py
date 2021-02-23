# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import pickle
import pandas as pd
import random

app = Flask(__name__)


import requests

from bs4 import BeautifulSoup 






def recom_hotels(username): 
    PATH = "C:/Users/Naomi/SYSTEME_RECOMMANDATION/PROJET_HOTEL/"
    Rdf = pd.read_csv(PATH +'reviews.csv')
    
    
    Udf = pd.read_csv(PATH + "users_profile_url.csv")
    Rdf = pd.read_csv(PATH + 'reviews.csv')
    Hdf = pd.read_csv(PATH + 'hotels_agreg.csv')
    
    
    #allouer à chaque hotel/review un id hotel_id/review_id
    Udf['user_id'] = Udf.index
    Hdf['hotel_id'] = Hdf.index
    #commencer à 1 et non 0
    Udf['user_id']=Udf['user_id'].apply(lambda x : x+1)
    Hdf['hotel_id']=Hdf['hotel_id'].apply(lambda x : x+1)
    
    RHdf=pd.merge(Rdf,Hdf)
    UHdf = pd.merge(RHdf,Udf)
    rates = UHdf.rate
    hotel_ids = UHdf.hotel_id
    user_ids = UHdf.user_id
    
    cosin_sim = pickle.load( open( "pickleContentBased.p", "rb" ) )
    
    
    
    
    test_user_id = int(Udf[Udf['username']==username].user_id)
    test_UHdf = UHdf.loc[UHdf['user_id']==test_user_id]
    test_UHdf = test_UHdf[test_UHdf['rate']>=4]
    list_hotel_ever_rated = test_UHdf.hotel_id.values
    
    #pour eviter d'avoir tout le temps les mêmes 
    id_hotel_for_sim = random.choice(list_hotel_ever_rated)
    print(id_hotel_for_sim)
    
    list_hotel_sim = cosin_sim[:,id_hotel_for_sim]
    
    #pour avoir les hotels les plus similaires à un des hotels deja note par user 
    scores_series = pd.Series(list_hotel_sim).sort_values(ascending=False)
    scores_series.drop(list_hotel_ever_rated)
    scores_series_fi = scores_series.head(5).keys()
    final = Hdf['name_hotel'].iloc[scores_series_fi]
    final_url = Hdf['url_hotel'].iloc[scores_series_fi]
    
    img_list = []
    
    for url in final_url:
        r=requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        img = soup.find('img',class_="_1a4WY7aS")['src']
        img_list.append(img)
    
    
    return final, img_list



@app.route('/')
def home():
    recom = recom_hotels('EileanE')
    hotels = recom[0].tolist()
    img = recom[1]
    name = "nao"
    
    return render_template('home.html', name = name,hotels=hotels, img=img)



@app.route('/test',methods = ['POST'])
def test():
    result = request.form
    r = result['username']
    error = False
    try:
        recom = recom_hotels(r)
        hotels = recom[0].tolist()
        img = recom[1]
    except:
        error = True
        recom = 0
        hotels = 0
        img = 0
    name = "nao"
    return render_template('test.html', username = r,hotels=hotels, img=img,error=error)





if __name__ == '__main__':
	app.run(debug=True)
    




    