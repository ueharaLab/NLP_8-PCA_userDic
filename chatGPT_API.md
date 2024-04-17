# ChatGPT APIプログラミング

1. python からChatGPTプロンプトを生成して、ChatGPT APIで問い合わせるプログラミング
2. プログラミングの処理手順
   1. tsukurepo_df.csvからツクレポをpythonで１つづつ読み込む
   2. 固有表現（食感、食材）を取り出すプロンプトを生成
   3. 1,2をプロンプトにしてChatGPT APIにリクエスト
   4. ChatGPT APIから返却された固有表現を食感、食材別にリストにする
   5. 1～4を繰り返す
3. openai.ChatCompletion.create(model, プロンプト文字列)がChatGPT APIにプロンプトをリクエストするpythonメソッド
4. chat_GPT_ner.pyを実行すると実はめちゃくちゃ遅い（セキュリティの関係でデモだけ見てください）
```python

import pandas as pd
import re
import pickle

# プロンプトのひな型を定義して変数 templateに入れる
# '''   ''' でpythonの文字列とプロンプトメッセージを区別する。データ型や書式まで指定できる！
template = '''
"""__MSG__"""
- 食材名を取り出してingredients=食材名のリスト型 で取り出してください。
- 食感の単語を取り出してtextures=食感の単語のリスト型 で取り出してください。
'''
#openai.ChatCompletion.create(model名，プロンプト文字列)
def chat_completion(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages)
    
    return response.choices[0]['message']['content']


tsukurepo_df = pd.read_csv('./data/tsukurepo_df.csv', encoding='ms932', sep=',',skiprows=0)
tsukurepo_texts = tsukurepo_df['tsukurepo'].values.tolist()

ing_ners = []
texture_ners = []
for tsukurepo in tsukurepo_texts:
    # つくれぽを1行よんでプロンプトのひな型の__MSG__に代入する
    prompt = template.replace('__MSG__', tsukurepo)
    messages = [
        # ユーザーからの要求を意味するプロンプトの場合はプロンプトは以下のような形式にする
        {'role': 'user', 'content': prompt}
    ]
         
    s = chat_completion(messages)
    # S の中には、食感と食材が別々に入っている。余計な文字列も混じるので、
    # ingredients=食材名のリスト型 
    # textures=食感の単語のリスト型
    # の部分だけ取り出す
    ingreds=re.findall("(ingredients.*\[)(.*)(\])",s)
    if len(ingreds)!=0:
        ingreds = ingreds[0][1].replace('\'','').replace('\"','').replace(' ','')        
        ing_list = ingreds.split(',')
        print(ing_list)
        ing_ners+=ing_list
        #print(ing_ners)

    textures=re.findall("(textures.*\[)(.*)(\])",s)
    if len(textures)!=0:
        textures = textures[0][1].replace('\'','').replace('\"','').replace(' ','')        
        tex_list = textures.split(',')
        print(tex_list)
        texture_ners+=tex_list
        #print(texture_ners)
    

with open('./data/ing_ners.pickle', 'wb') as f:
    pickle.dump(ing_ners, f)
with open('./data/texture_ners.pickle', 'wb') as f:
    pickle.dump(texture_ners, f)
```
