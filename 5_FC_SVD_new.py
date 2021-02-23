# -*- coding: utf-8 -*-
import pandas as pd
from surprise import SVD, NMF, Reader, Dataset, accuracy
from surprise.model_selection.split import train_test_split
from surprise import SVD,NormalPredictor
from surprise.model_selection import GridSearchCV
import pickle


"""
FILTRAGE COLABORATIF
RECHERCHE DU MEILLEUR MODELE NMF ET SVD
TUNING PARAMETERS AVEC GRIDSEARCH
ENTRZINEMENT DU MEILLEUR MODELE 
SAUVEGARDE DU MODELE DANS FICHIER FICKLE pour utilisation en lancant un fihcier python,
 ou avec interface grahique avec flask requetant directement le modèle serialié
"""



UDF = pd.read_csv("users_profile_url.csv")
RDF = pd.read_csv('reviews.csv')
HDF = pd.read_csv('hotels_agreg.csv')
#allouer à chaque hotel/review un id hotel_id/review_id
UDF['user_id'] = UDF.index
HDF['hotel_id'] = HDF.index
#commencer à 1 et non 0
UDF['user_id']=UDF['user_id'].apply(lambda x : x+1)
HDF['hotel_id']=HDF['hotel_id'].apply(lambda x : x+1)
RHDF=pd.merge(RDF,HDF)
UHDF = pd.merge(RHDF,UDF)
rates = UHDF.rate
hotel_ids = UHDF.hotel_id
user_ids = UHDF.user_id

ratings = pd.DataFrame({'user_id':user_ids,'hotel_id':hotel_ids,'rating':rates})
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[['user_id','hotel_id','rating']],reader)

#construire les données d'entrainement
#trainset, testset = train_test_split(data,test_size = 0.20)

#on peut aussi entrainer autrement
trainset = data.build_full_trainset()


#RECHERCHE DES MEILLEURS PARAMETRES AVEC SVD

best_best_params = None
best_best_score = - 1000
best_model = None
best_model_name = None
list_score = []
list_mod = [SVD,NMF]
list_param = []

#recherche du meilleur modele et meilleurs paramètres
for mod in list_mod:
    param_grid = None
    param_grid_SVD = {'n_factors':[100,150,300],
                  'n_epochs':[20,30,40],
                  'lr_all':[0.005,0.01],
                  'reg_all':[0.02,0.1]}
    param_grid_NMF = {'n_factors':[100,150,300],
                  'n_epochs':[20,30,40]}
    
    if mod==SVD:
        param_grid = param_grid_SVD
    else:
        param_grid = param_grid_NMF
    gs = GridSearchCV(mod,param_grid, measures=['rmse'], cv=5)
    gs.fit(data)
    best_params = gs.best_params['rmse']
    best_score = gs.best_score['rmse']
    list_score.append(best_score)
    list_param.append(best_params)
    model_name = str(mod)[-5:-2]
    print("Best RMSE with " + model_name + " : " + str(best_score))
    print("Best Param with "+ model_name + " : " + str(best_params))
    
      
max_score = min(list_score) 
index_max =  list_score.index(max_score)
best_best_params = list_param[index_max]
best_model = list_mod[index_max]
        
print(best_model)
algo = None
if best_model == SVD:
    algo = best_model(n_factors=best_best_params['n_factors'],
                  n_epochs=best_best_params['n_epochs'],
                  lr_all=best_best_params['lr_all'],
                  reg_all=best_best_params['reg_all'])
else:
    algo = best_model(n_factors=best_best_params['n_factors'],
                  n_epochs=best_best_params['n_epochs'])


algo.fit(trainset)

# Predict ratings for all pairs (i,j) that are NOT in the training set.
testset = trainset.build_anti_testset()
predictions = algo.test(testset)

#serializer la prediction
pickle.dump( predictions, open( "app/pickleFcSvd.p", "wb" ) )


#predictions_pickle = pickle.load( open( "app/pickleFcSvd.p", "rb" ) )

#on transforme en df et on récupère que l'user id 1
user_select = 1
df_pred = pd.DataFrame(predictions)
user_1_pred = df_pred[df_pred['uid']==user_select]


nb_hotel = 10
user_1_best_rating_pred = user_1_pred.sort_values(by='est',ascending = False)[:nb_hotel]


hotel_best = list(HDF[HDF["hotel_id"].isin(list(user_1_best_rating_pred['iid']))]['name_hotel'])

print('\n\nVoici les meilleurs hotels pour vous !  \n')
for i,hotel in enumerate(hotel_best):
    print(str(i+1)+"- "+hotel)
    



