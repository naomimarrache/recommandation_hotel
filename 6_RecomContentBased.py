# -*- coding: utf-8 -*-


import random
import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

"""
SYSTEME DE RECOMMENDATION BASE CONTENU
basé sur localisation, style, equipement, prix, category ..
saubegarde de la matrice cos_sim dans un fichier pickle pour pouvoir tester par la suite 
des recommendation plus rapidement, sans relancer les claculs matriciels
"""


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


Hdf1 = Hdf.copy()
Hdf1['localisation_hotel']=Hdf1.localisation_hotel.str.split("|")
for index, row in Hdf1.iterrows():
    for localisation in row['localisation_hotel']:
        Hdf1.at[index,localisation]=1
               
#Hdf1=Hdf1.fillna(0) 
Hdf1['style_hotel'].fillna("NoStyle||NoStyle",inplace=True)
#avant de faire le calcule de patrice spprimer la colonne NoStyle et 
#la colonne '' vide qui ne sont pas revelatrices de preferences

Hdf1['style_hotel']=Hdf1.style_hotel.str.split("|")
for index, row in Hdf1.iterrows():
    for style in row['style_hotel']:
        Hdf1.at[index,style]=1
        
Hdf1['equipments_hotel']=Hdf1.equipments_hotel.str.split("|")
for index, row in Hdf1.iterrows():
    for equipment in row['equipments_hotel']:
        Hdf1.at[index,equipment]=1
        
        
#ne pas oublier de supprimer les colonnes qui servent à rien

Hdf1=Hdf1.fillna(0)

Hdf1['col_price_hotel'] = Hdf1.price_hotel
Hdf1['col_category_hotel'] = Hdf1.category_hotel




df = pd.DataFrame(Hdf1)
df=df.set_index('hotel_id')
res=df.iloc[:,14:]

"""
minmax_scale = MinMaxScaler().fit(res)
df_minmax = minmax_scale.transform(res)
"""
cosin_sim=cosine_similarity(res)



#on test la reommandation avec un user id

test_user_id = 6
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
scores_series_fi_with_mean = mean_sim.head(10).keys()
final_with_mean = Hdf1['name_hotel'].iloc[scores_series_fi_with_mean]

#pour avoir les hotels les plus similaires à un des hotels deja note par user 
scores_series = pd.Series(list_hotel_sim).sort_values(ascending=False)
#supprimer ceux qui ont deja ete note
scores_series.drop(list_hotel_ever_rated)
scores_series_fi = scores_series.head(10).keys()
final = Hdf1['name_hotel'].iloc[scores_series_fi]


 
print('\n\nVoici les meilleurs hotels pour vous !\n(En se basant sur la similarité des hotels avec un que vous avez deja vu \n')
for i,hotel in enumerate(final):
    print(str(i+1)+"- "+hotel)
  


print('\n\nVoici les meilleurs hotels pour vous !\n(En se basant sur la similarité des hotels avec une moyenne des hotels deja vu \n')
for i,hotel in enumerate(final_with_mean):
    print(str(i+1)+"- "+hotel)
  




#charger la matrice cosin_sim dans u fichier
pickle.dump( cosin_sim, open( "app/pickleContentBased.p", "wb" ) )


#lire la matrice
#file = pickle.load( open( "app/pickleContentBased.p", "rb" ) )
