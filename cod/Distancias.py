import osmnx as ox
import networkx as nx
import numpy as np

class Distancias():
    def __init__(self, objeto_mapa):
        '''
        Constructor de la clase Distancias.

        Parameters
        ----------
        objeto_mapa : Mapa
            Objeto de la clase Mapa.

        Returns
        -------
        None.

        '''
        self.__mapa = objeto_mapa.mapa()
        self.__coordenadas = objeto_mapa.coordenadas()
    
    @property
    def mapa(self):
        '''
        Getter del atributo mapa.

        Returns
        -------
        networkx.classes.multidigraph.MultiDiGraph
            Mapa alrededor de los lugares de interés.

        '''
        return self.__mapa

    @mapa.setter
    def mapa(self, new_value):
        '''
        Setter del atributo mapa.

        Parameters
        ----------
        new_value : networkx.classes.multidigraph.MultiDiGraph
            Nuevo mapa de los lugares de interés.

        Returns
        -------
        None.

        '''
        self.__mapa = new_value

    @property
    def coordenadas(self):
        '''
        Getter del atributo coordenadas.

        Returns
        -------
        list
            Lista de coordenadas de los lugares de interés.

        '''
        return self.__coordenadas

    @coordenadas.setter
    def coordenadas(self, new_value: list):
        '''
        Setter del atributo coordenadas.

        Parameters
        ----------
        new_value : list
            Lista de nuevas coordenadas de los lugares de interés.

        Returns
        -------
        None.

        '''
        self.__coordenadas = new_value
        
    def __str__(self):
        '''
        Método str de la clase Distancias.

        Returns
        -------
        str
            Descripción del objeto y sus atributos.

        '''
        return f'''Este es un objeto de tipo Distancias con:
            Objeto Mapa: {self.__objeto_mapa}
            '''
        
    def distancias(self):
        '''
        Retorna la matriz de distancias entre los lugares de interés, en el mapa.

        Returns
        -------
        distance_matrix_km : numpy.ndarray
            Matriz con las menores distancias entre los lugares de interés.
            La distancia se calcula de acuerdo al grafo/mapa, es decir, en carretera.

        '''
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
                        distance_matrix[i][j] = length
                    except nx.NetworkXNoPath:
                        distance_matrix[i][j] = None 
        
        distance_matrix_km = (distance_matrix / 1000)
        
        return distance_matrix_km
