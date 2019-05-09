FilePath = 'assets/data.csv'

import csv
import math
import random
import matplotlib.pyplot as plt
import numpy as np

def main():
    Data = list(csv.reader(open(FilePath), quoting=csv.QUOTE_NONNUMERIC))
   
    handleCase(Data, 6)
    handleCase(Data, 12)
    handleCase(Data, 30)



def handleCase(Data, value):
    i = 0
    cluster = []
    cluster2 = []
    distances = []
    errors = []
    averageError = [0,0,0,0,0,0,0,0,0,0,0,0]
    matrix = []
    length = 0
    while i < 12:
        centroid = random.sample(Data, value)            #wybiera losowo centroidy
        cluster.clear()
        cluster2.clear()
        clustering(Data, centroid, cluster, distances)   #pierwsze grupowanie
        error(distances, errors, i, averageError)        #pierwszy blad
        new_center(cluster, centroid)                    #dopasowuje nowe centroidy
        clustering(Data, centroid, cluster2, distances)  #drugie grupowanie ale do innego klastra
        error(distances, errors, i, averageError)        #drugi blad

        while cluster2 != cluster:                       #powtarza do braku zmiany
            cluster.clear()
            cluster = cluster2.copy()
            cluster2.clear()
            new_center(cluster, centroid)
            clustering(Data, centroid, cluster2, distances)
            error(distances, errors, i, averageError)    #trzeci i w gore blad
            
        #if i != 0 and 
        length = len(errors)
        matrix.append(errors)                            #dodaje liste bledow z jednego przejscia do list /jakby macierz tworzy/
        errors.clear()
        i += 1
        
    for ae in averageError:     
        ae = ae / 12.0                                   #averageError ma srednie bledy

   #rysowanie wykresu rozmieszczenia danych i centroidów:   
    for d in Data:
        for c in centroid:
            plt.plot(d[0],d[1], 'ro', c[0],c[1], 'bs')
    plt.show()
  



def clustering(Data, centroid, cluster, distances):
    distances.clear()
    for case in Data:
        prev_distance = 0
        tmp = 0
        for center in centroid:
            distance = 0
            distance = (case[0]-center[0])**2+((case[1]-center[1])**2)
            distance = math.sqrt(distance)
            
            if prev_distance == 0 or distance < prev_distance:
                prev_distance = distance
                tmp = center
               
        cluster.append([case, tmp])
        distances.append(distance)
    
    
    
def new_center(cluster, centroid):
    j = 0
    for center in centroid:
        average = [0, 0]
        counter = 0
        for c in cluster:
            if c[1] == center:
                counter += 1
                i = 0
                for variable in c[0]:
                    average[i] += variable
                    i += 1
            
        if counter != 0:
            average[0] = average[0] / counter
            average[1] = average[1] / counter
                
        centroid[j] = average
        j += 1

        
        
def error(distances, errors, i, averageError):
    summ = 0
    for distance in distances:
        distance = distance**2
        summ = summ + distance
        
    summ = summ / 1000.0
    averageError[i] += summ 
    errors.append(summ)
    
    

if __name__ == "__main__":
    main()