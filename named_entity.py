import spacy
from spacy import displacy
import pandas as pd
import codecs
#txt = ("牛乳がたくさんあったので作りました！更にアレンジして、上から苺ミルクをかけて食べたら、可愛くて更に美味しくなりました！！ 冷凍庫に入れてシャリシャリ食感で頂きました。美味しかったです★ 少し泡だってしまいましたが、味は◎！！")
tsukurepo_df = pd.read_csv('./data/tsukurepo_df.csv', encoding='ms932', sep=',',skiprows=0)
tsukurepo_texts = tsukurepo_df['tsukurepo'].values.tolist()

nlp = spacy.load("ja_ginza")
#nlp = spacy.load("ja_ginza_electra")
name_entity = {}
for text in tsukurepo_texts:
    doc = nlp(text)    
    for ent in doc.ents:
        if ent.text not in name_entity:
            name_entity[ent.text]=ent.label_
            print(ent.text,ent.label_)
        #print(ent.text, ent.label_, ent.start_char, ent.end_char)
        #displacy.render(doc, style="ent", options={"compact":True},  jupyter=True)


name_entity_df = pd.DataFrame([[n,e] for n,e in name_entity.items()],columns =['name','entity'])
with codecs.open("./data/named_entity.csv", "w", "ms932", "ignore") as f: 
    #header=Trueで、見出しを書き出す
    name_entity_df.to_csv(f, index=False, encoding="ms932", mode='w', header=True)