import numpy as np                                # For data management
import pandas as pd                               # For data management

import seaborn as sns                             # For data visualization and specifically for pairplot()
import matplotlib 
import matplotlib.pyplot as plt                   # For data visualization

from sklearn import datasets                      # To import the sample dataset
from sklearn.preprocessing import StandardScaler, LabelEncoder  # To transform the dataset
from sklearn.cluster import KMeans          # To instantiate, train and use model
from sklearn import metrics                       # For Model Evaluation
 
matplotlib.use('TkAgg')

dataset = pd.read_csv("./dataset.csv", engine="python")

toRemove = ['time', 'periodo_visione', 'cosa_fare', 'preferenza_visione', 'media_film', 'media_puntate']

dataset = dataset.drop(toRemove, axis=1)

labelEncoder = LabelEncoder()
labelEncoder.fit(dataset['genere_preferito'])
dataset['genere_preferito'] = labelEncoder.transform(dataset['genere_preferito'])


labelEncoder = LabelEncoder()
labelEncoder.fit(dataset['età'])
dataset['età'] = labelEncoder.transform(dataset['età'])

"""
VERGOGNA TOTALE QUESTE VARIABILI PIÙ SCORRELATE DEI DISCORSI DEI SALVINI
"""
# TODO dobbiamo stampare la heatmat fare uno screen e metterla nella doc
# print(dataset.corr())
plt.figure(figsize = (15,6))
sns.heatmap( dataset.corr(), annot=True)
# plt.show()

sns.pairplot(dataset)


# Standardizzazione del dataset
scaler = StandardScaler()
scaled_array = scaler.fit_transform(dataset)

scaled_dataframe = pd.DataFrame( scaled_array, columns = dataset.columns )

print(scaled_dataframe.describe())

# Kmeans
# Mi piace il K-means 
# Proprio bello
KMeans_model = KMeans(n_clusters = 10)
KMeans_model.fit(scaled_dataframe)

centroidi = KMeans_model.cluster_centers_
print(centroidi)
print(KMeans_model.labels_)

# aggiungo il cluster assegnato alle osservazioni alle osservazioni stesse
scaled_dataframe['cluster'] = KMeans_model.labels_

print(dataset)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = (16,10))

sns.scatterplot(x = "sesso", y = "età", data = scaled_dataframe, hue = "cluster", palette = "Accent", ax = ax1, legend=False)
sns.scatterplot(x = "genere_preferito", y = "sesso", data = scaled_dataframe, hue = "cluster", palette = "Accent",ax = ax2, legend=False)
sns.scatterplot(x = "genere_preferito", y = "hobby", data = scaled_dataframe, hue = "cluster", palette = "Accent", ax = ax3, legend=False)
sns.scatterplot(x = "età", y = "hobby", data = scaled_dataframe, hue = "cluster", palette = "Accent",ax = ax4, legend=False)


sns.pairplot(data = scaled_dataframe, hue = "cluster", palette = "Accent_r")
plt.show()

# k_to_test = range(2,13, 1) # [2,3,4, ..., 24]
# silhouette_scores = {}


# k_to_test = range(2,13,1) # [2,3,4, ..., 24]
# silhouette_scores = {}

# for k in k_to_test:
#     model_kmeans_k = KMeans( n_clusters = k )
#     model_kmeans_k.fit(scaled_dataframe.drop("cluster", axis = 1))
#     labels_k = model_kmeans_k.labels_
#     score_k = metrics.silhouette_score(scaled_dataframe.drop("cluster", axis=1), labels_k)
#     silhouette_scores[k] = score_k
#     print("Tested kMeans with k = %d\tSS: %5.4f" % (k, score_k))
    
# print("Done!")

# plt.figure(figsize = (16,5))
# plt.plot(silhouette_scores.values())
# plt.show()