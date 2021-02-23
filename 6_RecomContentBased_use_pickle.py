# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import pickle
import pandas as pd
import random


def best_hotel(id,nb):
    Udf = pd.read_csv("users_profile_url.csv")
    Rdf = pd.read_csv('reviews.csv')
    Hdf = pd.read_csv('hotels_agreg.csv')
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
    
    ratings = pd.DataFrame({'user_id':user_ids,'hotel_id':hotel_ids,'rating':rates})
    cosin_sim = pickle.load( open( "app/pickleContentBased.p", "rb" ) )
        
    #on test la reommandation avec un user id
    test_user_id = id
    test_UHdf = UHdf.loc[UHdf['user_id']==test_user_id]
    test_UHdf = test_UHdf[test_UHdf['rate']>=4]
    list_hotel_ever_rated = test_UHdf.hotel_id.values
    
    #pour eviter d'avoir tout le temps les mêmes 
    id_hotel_for_sim = random.choice(list_hotel_ever_rated)
    print(id_hotel_for_sim)
    list_hotel_sim = cosin_sim[:,id_hotel_for_sim]
    
    #pour avoir les hotels les plus similaire à tous les hotels deja noté par user 
    matrice_dict_hotel_sim = { id:cosin_sim[:,id] for id in list_hotel_ever_rated }
    matrice_df_hotel_sim = pd.DataFrame(matrice_dict_hotel_sim)
    mean_sim =  (matrice_df_hotel_sim.sum(axis=1)/matrice_df_hotel_sim.shape[1]).sort_values(ascending=False)
    #supprimer ceux qui ont deja ete note
    mean_sim.drop(list_hotel_ever_rated)
    scores_series_fi_with_mean = mean_sim.head(nb).keys()
    final_with_mean = Hdf['name_hotel'].iloc[scores_series_fi_with_mean]
    
    #pour avoir les hotels les plus similaires à un des hotels deja note par user 
    scores_series = pd.Series(list_hotel_sim).sort_values(ascending=False)
    #supprimer ceux qui ont deja ete note
    scores_series.drop(list_hotel_ever_rated)
    scores_series_fi = scores_series.head(nb).keys()
    final = Hdf['name_hotel'].iloc[scores_series_fi]

     
    print('\n\nVoici les meilleurs hotels pour vous !\n(En se basant sur la similarité des hotels avec un que vous avez deja vu )\n')
    for i,hotel in enumerate(final):
        print(str(i+1)+"- "+hotel)
      
    
    
    print('\n\nVoici les meilleurs hotels pour vous !\n(En se basant sur la similarité des hotels avec une moyenne des hotels deja vu )\n')
    for i,hotel in enumerate(final_with_mean):
        print(str(i+1)+"- "+hotel)
      
    
    
    
        
        
if __name__=="__main__":
    id_user = 4
    nb_hotel = 10
    best_hotel(id_user,nb_hotel)
    


