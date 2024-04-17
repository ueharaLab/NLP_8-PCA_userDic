# カスタム辞書による料理関連語彙BoWの作成

1. 従来のbowの実装とほとんど同じだが、形態素解析tokenizerのコーディングだけ少し異なる。  
2. どこが違うか、[tokenizer.py](tokenizer.py)と比較して特定せよ。
3. この違いでどのように料理関連語彙だけのBoWを作成できるのだろうか。同義語処理はどのように行っているのか。
4. このBoWの次元数（語彙種類数）は212 なので、PCAでは最大212本の主成分ベクトルが引ける。これは、[tsukurepo_pca.py](tsukurepo_pca.py)中のどこに反映しているか

### 演習
userDic_onomatopea.csvを用いてオノマトペだけのBoWを作成して主成分平面に表示せよ。

[tokenizer_costomDic.py](tokenizer_customDic.py)   メインプログラムは[tsukurepo_bow_vectorizer.py](tokenizer_customDic.py)
``` python
def tokenize(sentence):

	csv_input = pd.read_csv('userDic_cooking.csv', encoding='ms932', sep=',',skiprows=0)	
	thesaurus_dict={}
	for key,val in zip(csv_input['key'],csv_input['value']):

		thesaurus_dict[key] = val
	
	tagger = MeCab.Tagger("mecabrc -u c:/neologd/NEologd.dic")
	
	node = tagger.parseToNode(sentence)

	tokens = []
	
	while node:            
				
		unique_word=thesaurus_dict.get(node.surface)
		if unique_word != None:	
			tokens.append(unique_word)
		
		node = node.next
	return tokens   
```		