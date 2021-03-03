import numpy as np                                # For data management
import pandas as pd                               # For data management

import seaborn as sns                             # For data visualization and specifically for pairplot()
import matplotlib 
import matplotlib.pyplot as plt                   # For data visualization

from sklearn import datasets                      # To import the sample dataset
from sklearn.preprocessing import StandardScaler, LabelEncoder  # To transform the dataset
from sklearn.cluster import KMeans          # To instantiate, train and use model
from sklearn import metrics                   # For Model Evaluation

 
matplotlib.use('TkAgg')

range_cluster = range(2, 13)
number_of_cluster = 13


def prepareDataset():
    dataset = pd.read_csv("./dataset.csv", engine="python")

    toRemove = ['time', 'periodo_visione', 'cosa_fare', 'preferenza_visione', 'media_film', 'media_puntate', 'email', 'nome', 'cognome']

    dataset = dataset.drop(toRemove, axis=1)

    labelEncoder = LabelEncoder()
    labelEncoder.fit(dataset['genere_preferito'])
    dataset['genere_preferito'] = labelEncoder.transform(dataset['genere_preferito'])


    labelEncoder = LabelEncoder()
    labelEncoder.fit(dataset['età'])
    dataset['età'] = labelEncoder.transform(dataset['età'])
    return dataset

def generateHeatmap():
    dataset = prepareDataset()
    plt.figure(figsize = (15,6))
    sns.heatmap( dataset.corr(), annot=True)
    plt.show()

def generatePairPlot():
    dataset = prepareDataset()
    sns.pairplot(dataset)
    plt.show()

def standardizeDataset():
    dataset = prepareDataset()
    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(dataset)
    scaled_dataframe = pd.DataFrame( scaled_array, columns = dataset.columns )
    print("SCALED DATAFRAME:")
    print(scaled_dataframe.describe())
    return scaled_dataframe

def bestKMeans(n_cluster = 1):
    scaled_dataframe = standardizeDataset()
    k_to_test = range(2, n_cluster, 1) 
    silhouette_scores = {}
    elbow_scores = []

    for k in k_to_test:
        model_kmeans_k = KMeans( n_clusters = k )
        model_kmeans_k.fit(scaled_dataframe)
        labels_k = model_kmeans_k.labels_
        score_k = metrics.silhouette_score(scaled_dataframe, labels_k)
        silhouette_scores[k] = score_k
        elbow_scores.append(model_kmeans_k.inertia_)
        print("Tested kMeans with k = %d\tSS: %5.4f" % (k, score_k))

    return silhouette_scores, elbow_scores

def generateElbowPointGraph(n_cluster = number_of_cluster):
    silhuette, elbow = bestKMeans(n_cluster = n_cluster)
    plt.plot(range(2, n_cluster, 1), elbow, 'bx-')
    plt.xlabel('numero cluster')
    plt.show()

def generateSilhuetteIndex(n_cluster = number_of_cluster):
    silhuette, elbow = bestKMeans(n_cluster = n_cluster)
    plt.plot(silhuette.values())
    plt.show()

def fitModel(n_cluster = 1):
    scaled_dataframe = standardizeDataset()
    KMeans_model = KMeans(n_clusters = n_cluster)
    KMeans_model.fit(scaled_dataframe)
    scaled_dataframe['cluster'] = KMeans_model.labels_
    return KMeans_model, scaled_dataframe

def generateScatterPlot(n_cluster = 1, coppie=[('hobby', 'genere_preferito')]):
    model, scaled_dataframe = fitModel(n_cluster)
    #fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = (16,10))
    plt.figure(figsize=(15,6))
    for coppia in coppie:
        sns.scatterplot(x = coppia[0], y = coppia[1],  data = scaled_dataframe, hue = "cluster", palette = "Accent", legend=False)
        plt.show()

def printCentroidsCoordinates(n_cluster = 1):
    model, *resto = fitModel(n_cluster = n_cluster)
    centroidi = model.cluster_centers_
    print("Centroidi: ")
    print(centroidi)

def main():
    while True:
        print("""|------------------------|\n|  SELEZIONA OPERAZIONE  |\n|------------------------|""")
        print("\t1 - Heat Map", "2 - Pair Plot", "3 - Elbow Point", "4 - Indice di Silhuette", "5 - Scatter Plot", "0 - esci", sep="\n\t")
        scelta_utente = input("Scegli uno dei seguenti: ")
        
        if(int(scelta_utente) == 1):
            generateHeatmap()
        elif(int(scelta_utente) == 2):
            generatePairPlot()
        elif(int(scelta_utente) == 3):
            numero_cluster = input("Scegli il numero massimo di cluster: ")
            try:
                generateElbowPointGraph(n_cluster = int(numero_cluster))
            except ValueError:
                print('Valori consentiti: 0 - 9')
        elif(int(scelta_utente) == 4):
            numero_cluster = input("Scegli il numero massimo di cluster: ")
            try:
                generateSilhuetteIndex(n_cluster = int(numero_cluster))
            except ValueError:
                print('Valori consentiti: 0 - 9')
        elif(int(scelta_utente) == 5):
            numero_cluster = input("Scegli il numero di cluster: ")
            numero_coppie = input("Scegli il numero di scatterplot. Per ognuno dovrai fornire una coppia. ")
            coppie = []
            try:
                for i in range(0, int(numero_coppie)):
                    print("\t\t0 - età", "1 - genere preferito", "2 - hobby", "3 - sesso", sep="\n\t\t")
                    primo_valore_raw = input("inserisci prima etichetta della etichetta {} coppia: ".format(i+1))
                    secondo_valore_raw = input("inserisci seconda etichetta della etichetta {} coppia: ".format(i+1))
                    if int(primo_valore_raw) == 0:
                        primo_valore = 'età'
                    elif int(primo_valore_raw) == 1:
                        primo_valore = 'genere_preferito'
                    elif int(primo_valore_raw) == 2:
                        primo_valore = 'hobby'
                    elif int(primo_valore_raw) == 3:
                        primo_valore = 'sesso'
                    
                    if int(secondo_valore_raw) == 0:
                        secondo_valore = 'età'
                    elif int(secondo_valore_raw) == 1:
                        secondo_valore = 'genere_preferito'
                    elif int(secondo_valore_raw) == 2:
                        secondo_valore = 'hobby'
                    elif int(secondo_valore_raw) == 3:
                        secondo_valore = 'sesso'
                    
                    coppie.append((primo_valore, secondo_valore))

                generateScatterPlot(n_cluster=int(numero_cluster), coppie=coppie)

            except ValueError as e:
                print(e)
                print('Valori consentiti 0 - 4')

        elif(int(scelta_utente) == 0):
            print("USCITA")
            break
        else:
            print("Errore - Input non valido")

if __name__ == "__main__":
    main()