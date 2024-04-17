import pickle
import codecs
import numpy as np
import pandas as pd

with open('./data/texture_ners.pickle', 'rb') as f:
    texture_ners = pickle.load(f)

with open('./data/ing_ners.pickle', 'rb') as f:
    ing_ners = pickle.load(f)

texture_ners=np.array(list(set(texture_ners)))
ing_ners=np.array(list(set(ing_ners)))
np.delete(texture_ners, np.where(texture_ners == ''))
np.delete(ing_ners, np.where(ing_ners == ''))

texture_ners_df = pd.DataFrame(texture_ners.reshape(-1,1) ,columns =['texture'])
with codecs.open("./data/texture_ners.csv", "w", "ms932", "ignore") as f: 
    #header=Trueで、見出しを書き出す
    texture_ners_df.to_csv(f, index=False, encoding="ms932", mode='w', header=True)

ingred_df = pd.DataFrame(ing_ners.reshape(-1,1) ,columns =['ingredient'])
with codecs.open("./data/ingredient_ners.csv", "w", "ms932", "ignore") as f: 
    #header=Trueで、見出しを書き出す
    ingred_df.to_csv(f, index=False, encoding="ms932", mode='w', header=True)

