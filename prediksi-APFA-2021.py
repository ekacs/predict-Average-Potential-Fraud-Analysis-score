#!/usr/bin/env python
# coding: utf-8

# In[ ]:


PERSIAPAN


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score


# In[ ]:


#load data KorWil.xlsx
korwil = pd.read_excel("D:\Jaga Data Challenge\KorWil.xlsx")

#membuang data terakhir karena sama dengan nama kolom
korwil.drop(korwil.tail(1).index,inplace=True)

korwil.isna().sum()


# In[ ]:


#merubah tipe data 'bobot_area_intervensi' menjadi tipe data numerik
korwil['bobot_area_intervensi'] = pd.to_numeric(korwil['bobot_area_intervensi'])

#gouping data berdasarkan instansi dan area_intervensi dengan ratas nilai bobot_area_intervensi 
korwil1 = korwil.groupby([korwil['instansi'], korwil['area_intervensi']]).mean()
korwil2 = korwil1.reset_index()
pivot_df = pd.pivot(korwil2, index='instansi', columns = 'area_intervensi', values='bobot_area_intervensi')

korwil_pivot = pivot_df.reset_index()

#menghilangkan kata Pemerintah di kolom instansi 
Instansi=[]
i=0
for i in range(len(korwil_pivot)):
    nama= korwil_pivot.iloc[i,0].replace('Pemerintah ', '')
    Instansi.append(nama)

korwil_pivot.insert(loc=1, column='Instansi', value=Instansi)
korwil_pivotTable = korwil_pivot.drop(korwil_pivot.columns[0], axis=1)
korwil_pivotTable

#Output hasil ke bentuk CSV
#korwil_pivot.to_csv("korwil_pivotTable.csv", index=False)


# In[ ]:


#load data opentender 
opentender = pd.read_excel("D:\Jaga Data Challenge\sumber-opentender-2021.xlsx")
opentender.head()


# In[ ]:


#menghilangkan kata lpse pada kolom lpse
lpse2=[]
for i in range(len(opentender)):
    nama = opentender.iloc[i,2].replace('LPSE ', '')
    lpse2.append(nama)
opentender['lpse2'] = lpse2
opentender.head()

#Output hasil ke bentuk CSV
#opentender.to_csv("Opentender.csv", index=False)


# In[ ]:


#groping data opentender dengan ratas skor
group_opentender = opentender.groupby(opentender['lpse2']).mean()
group_opentender


# In[ ]:


#join data korwil dengan opentender
join_data = pd.merge(korwil_pivotTable, group_opentender, left_on=['Instansi'], right_on=['lpse2'], how='inner')

#menghapus data na
join_data = join_data1.dropna(axis=0, how="any")

#Output hasil ke bentuk CSV
join_data.to_csv("join_data.csv", index=False)


# In[ ]:


join_data.isna().sum()


# PEMBENTUKAN BASIC ML PREDICTION BASED ON MULTIPLE LINIER REGRETION

# In[ ]:


#pembacaan data(1)
atribut = ['rec','x1','x2','x3','x4','x5','x6','x7','x8','x9','x10','x11','y']
filepath = 'I:/My Drive/NOWHERE TIM/JAGA-DATA-CHALLENGE-2021/join_data.csv'
df = pd.read_csv(filepath, header=1, names=atribut)
df.head()


# In[ ]:


#pembacaan data(2)
df.info()


# In[ ]:


#pembacaan data(3)
df.describe()


# In[ ]:


#pembersihan data
df.isnull().sum()


# In[ ]:


#pembentukan model data
features = ['x1','x2','x3','x4','x8','x10'] #terpilih hanya yg signifikan sesuai hasil penelitian dg pendekatan PLS
X = df[features]
y = df['y']


# In[ ]:


#pembuatan data training dan data tes, dengan ukuran 9:1  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)
abs(lin_reg.score(X_test, y_test)*100) #cek besaran akurasi prediksi absolutnya


# In[ ]:


#menghitung rata-rata kesalahan mutlak
y_hat = lin_reg.predict(X_test)
mean_absolute_error(y_test, y_hat)

UJI COBA pada Pemerintah Kabupaten Aceh memiliki skor indikator:
1)APIP = 15
2)Manajemen ASN = 11.79
3)Manajemen Aset Daerah = 10.625
Optimalisasi Pajak Daerah = 10.6
4)Tata Kelola Dana Desa = 16
5)Perizinan = 5

hasilnya adalah 41.29764827 seharusnya 40, terdapat selisih sebesar 1.298 (3.245% lebih besar). 
# In[ ]:


lin_reg.predict([[15, 11.79, 10.625, 10.6, 16, 5]])

