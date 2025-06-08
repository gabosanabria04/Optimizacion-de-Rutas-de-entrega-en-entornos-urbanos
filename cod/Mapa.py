import osmnx as ox
class Mapa():
    def __init__(self, lugares: list):
        self.__lugares = lugares
    
    @property
    def lugares(self):
        return self.__lugares

    @lugares.setter
    def lugares(self, new_value):
        self.__lugares = new_value
        
    def coordenadas(self):
        coordenadas = []
        for lugar in self.__lugares:
            punto = ox.geocode(lugar)
            coordenadas.append(punto)

        return coordenadas
            
    def mapa(self):
        coordenadas = self.coordenadas()
        latitudes, longitudes = zip(*coordenadas)
        top, bottom = max(latitudes) + 0.003, min(latitudes) - 0.003
        right, left = max(longitudes) + 0.003, min(longitudes) - 0.003
        
        bbox = (left, bottom, right, top)
        G = ox.graph_from_bbox(top, bottom, left, right, network_type='drive')
        return G
