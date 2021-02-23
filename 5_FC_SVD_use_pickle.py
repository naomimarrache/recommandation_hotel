# -*- coding: utf-8 -*-
import pickle
import pandas as pd



def best_hotel(id,nb):
    HDF = pd.read_csv('hotels_agreg.csv')
    #allouer à chaque hotel/review un id hotel_id/review_id
    
    HDF['hotel_id'] = HDF.index
    #commencer à 1 et non 0
    HDF['hotel_id']=HDF['hotel_id'].apply(lambda x : x+1)
    
    predictions_pickle = pickle.load( open( "app/pickleFcSvd.p", "rb" ) )
    
    user_select = id
    df_pred = pd.DataFrame(predictions_pickle)
    user_1_pred = df_pred[df_pred['uid']==user_select]
    
    nb_hotel = nb
    user_1_best_rating_pred = user_1_pred.sort_values(by='est',ascending = False)[:nb_hotel]
    
  
    hotel_best = list(HDF[HDF["hotel_id"].isin(list(user_1_best_rating_pred['iid']))]['name_hotel'])
    
    print('\n\nVoici les meilleurs hotels pour vous !  \n')
    for i,hotel in enumerate(hotel_best):
        print(str(i+1)+"- "+hotel)
        
        
        
if __name__=="__main__":
    id_user = 3
    nb_hotel = 10
    best_hotel(id_user,nb_hotel)
    


