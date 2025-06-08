import osmnx as ox
import networkx as nx
import numpy as np

class Distancias():
    def __init__(self, objeto_mapa):
        self.__mapa = objeto_mapa.mapa()
        self.__coordenadas = objeto_mapa.coordenadas()

    def distancias(self):
        nodes = [ox.nearest_nodes(self.__mapa, lon, lat) for lat, lon in self.__coordenadas]
        
        n = len(nodes)
        distance_matrix = np.zeros((n, n), dtype=int)
        for i in range(n):
            for j in range(n):
                if i == j:
                    distance_matrix[i][j] = 0
                else:
                    try:
                        length = nx.shortest_path_length(self.__mapa, nodes[i], nodes[j], weight='length')
                        distance_matrix[i][j] = length #metros
                    except nx.NetworkXNoPath:
                        distance_matrix[i][j] = None 
        
        distance_matrix_km = (distance_matrix / 1000)
        
        return distance_matrix_km
