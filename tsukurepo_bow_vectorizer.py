from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import pandas as pd
from tokenizer_customDic import tokenize  # <1>
import codecs
import unicodedata
import re



tsukurepo_df = pd.read_csv('./data/tsukurepo_df.csv', encoding='ms932', sep=',',skiprows=0)
tsukurepo_texts = tsukurepo_df['tsukurepo'].values.tolist()
# Bag of Words計算

texts_list=[]
for text in tsukurepo_texts:
    text=unicodedata.normalize('NFKC',text)
    text=re.findall('[一-龥ぁ-んァ-ンー々]+',text )     
    text= ''.join(text)
    
    texts_list.append(text)


vectorizer = TfidfVectorizer(tokenizer=tokenize)

#vectorizer = CountVectorizer(tokenizer=tokenize,min_df=0.0001, max_df=0.1)  # <2>
vec=vectorizer.fit(texts_list)  # <3>
bow = vectorizer.transform(texts_list)  # <4>
print(vec.vocabulary_)
print(bow)
print(bow.toarray())


tsukurepo_bow = pd.DataFrame(bow.toarray(), columns=vectorizer. get_feature_names_out())
col_words = [w for w in tsukurepo_bow.columns if len(re.findall('[一-龥ぁ-んァ-ンー々]+',w ) )!=0]
print('dim : ', len(col_words))
tsukurepo_bow = tsukurepo_bow.loc[:,col_words]
assert len(tsukurepo_bow)==len(tsukurepo_df), 'tsukurepo len unmatch'
tsukurepo_df = pd.concat([tsukurepo_df, tsukurepo_bow], axis=1)
with codecs.open("./data/tsukurepo_bow.csv", "w", "ms932", "ignore") as f: 
    #header=Trueで、見出しを書き出す
    tsukurepo_df.to_csv(f, index=False, encoding="ms932", mode='w', header=True)