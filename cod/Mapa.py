import osmnx as ox
class Mapa():
    def __init__(self, lugares: list):
        '''
        Constructor de la clase Mapa.

        Parameters
        ----------
        lugares : list
            Lista con los nombres de los lugares de interés.

        Returns
        -------
        None.

        '''
        self.__lugares = lugares
    
    @property
    def lugares(self):
        '''
        Getter del atributo lugares.

        Returns
        -------
        list
            Lista de nombres de los lugares de interés.

        '''
        return self.__lugares

    @lugares.setter
    def lugares(self, new_value: list):
        '''
        Setter del atributo lugares.

        Parameters
        ----------
        new_value : list
            Lista de nombres de los nuevos lugares de interés.

        Returns
        -------
        None.

        '''
        self.__lugares = new_value
        
    def __str__(self):
        '''
        Método str de la clase Mapa.

        Returns
        -------
        str
            Descripción del objeto y sus atributos.

        '''
        return f'''Este es un objeto de la clase Mapa, asociado a:
            Lugares: {self.__lugares}
            '''
        
    def coordenadas(self):
        '''
        Retorna las coordenadas de los lugares de interés.

        Returns
        -------
        coordenadas : list
            Coordenadas de los lugares de interés.

        '''
        coordenadas = []
        for lugar in self.__lugares:
            punto = ox.geocode(lugar)
            coordenadas.append(punto)

        return coordenadas
            
    def mapa(self):
        '''
        Retorna el mapa alrededor de los lugares de interés.

        Returns
        -------
        G : networkx.classes.multidigraph.MultiDiGraph
            Mapa alrededor de los lugares de interés.

        '''
        coordenadas = self.coordenadas()
        latitudes, longitudes = zip(*coordenadas)
        top, bottom = max(latitudes) + 0.003, min(latitudes) - 0.003
        right, left = max(longitudes) + 0.003, min(longitudes) - 0.003
        
        G = ox.graph_from_bbox(top, bottom, left, right, network_type='drive')
        return G
