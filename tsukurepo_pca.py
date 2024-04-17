
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn import datasets
import pandas as pd
import japanize_matplotlib
import seaborn as sns



csv_input = pd.read_csv('./data/tsukurepo_bow.csv', encoding='ms932', sep=',',skiprows=0)
#素性をTF-IDFにするなら、create_dataset_tfidfを使う
cluster=csv_input['keyword'].tolist()
cls = {c:i for i,c in enumerate(list(set(cluster)))}
#print(cls)

dataset=csv_input.iloc[:,4:].values
feature_names = csv_input.iloc[:,4:].columns
fig, ax = plt.subplots(1,1, figsize=(8,8))

# 主成分分析クラスのインスタンス化(n_components:計算する主成分の数）
pca = PCA(n_components=212)	
pca.fit(dataset)
transformed = pca.transform(dataset)
print(transformed)
tr_df = pd.DataFrame(transformed)
#cls_df = pd.DataFrame(,columns=['dish'])
pca_score_df = pd.concat([csv_input.iloc[:,0],tr_df],axis=1)


colors=['orange','red','blue','gold']

sns.scatterplot(x=0, y=1, hue='keyword', palette="hls",data=pca_score_df,s=200,alpha=0.4)


# 語彙空間の各軸(one hot vector)を部分空間PC1,PC2に射影したベクトルpを求めたい strang p.171
# pは語彙の個数分求まる。これらの中でノルムがtop10のものを求める
# top10のベクトル座標をpca.transformで主成分空間に回転する
# 
# 変数間の対応を整理
# b : 語彙軸one hot vector 次元数は語彙数(vocab_e)   
#     bは語彙数分存在する（pca.componentsの列数で確認すること
# A : pca_vectors=pca.components_[:2,:]を列ベクトルにして並べたもの（列空間） 次元数は語彙数
# p : bを列空間Aに射影した点の座標　次元数は語彙数
#   。pのノルムが大きいほどAとbは近い

vocab_e = np.eye(len(feature_names))
A=pca.components_[:2,:].T
A_inv = np.linalg.inv(np.dot(A.T,A))
P = np.dot(np.dot(A,A_inv),A.T)
p_matrix = np.dot(P,vocab_e)#pの列ベクトルが語彙毎の主成分ベクトル部分空間(PC1,PC2)への射影ベクトルになる

p_norm = {name:np.linalg.norm(p_matrix[:,i], ord=2) for i,name in enumerate(feature_names) }
p_norm_sorted = dict(sorted(p_norm.items(), key=lambda x:x[1],reverse=True))
print(p_norm_sorted)
ranking =15
top_ranked_voc = [name for i,name in enumerate(p_norm_sorted) if i < ranking]
p_matrix_df = pd.DataFrame(p_matrix,columns=feature_names)

top_vocs = p_matrix_df.loc[:,top_ranked_voc]
top_vocs = top_vocs.T
trans_top_vocs = pca.transform(top_vocs.values)

for row,name in zip(trans_top_vocs,top_vocs.index):
	ax.arrow(0,0,row[0]*1,row[1]*1,width=0.001,head_width=0.005,head_length=0.01,length_includes_head=True,color='blue')
	ax.annotate(name,xy=(row[0]*1,row[1]*1),size=16,color = 'black')
	
    	

'''
pca_vectors=pca.components_.T[:,:2] 
pca_vec_sqsum = [(pv[0]**2) + (pv[1]**2) for pv in pca_vectors]
pca_vecs=[]
for pca_vec, sq_sum, feature in zip(pca_vectors, pca_vec_sqsum, feature_names):
    	pca_vecs.append([sq_sum,pca_vec[0],pca_vec[1],feature])

pca_vecs_df = pd.DataFrame(pca_vecs,columns=['sq_sum','x','y','name'])
pca_vecs_df = pca_vecs_df.sort_values('sq_sum', ascending=False)


for i,row in pca_vecs_df.iloc[:ranking,:].iterrows():
	ax.arrow(0,0,row['x']*1,row['y']*1,width=0.001,head_width=0.005,head_length=0.01,length_includes_head=True,color='blue')
	#ax.quiver(0,0,row['x'],row['y'],angles='xy',scale_units='xy',scale=1)
	ax.annotate(row['name'],xy=(row['x']*1,row['y']*1),size=16,color = 'black')
'''		
contrib_list=np.round(pca.explained_variance_ratio_, decimals=3)
print(contrib_list)
ax.set_xlabel('PC1 ({})'.format(contrib_list[0]),fontsize=18)
ax.set_ylabel('PC2 ({})'.format(contrib_list[1]),fontsize=18)
plt.show()


	
		
	
