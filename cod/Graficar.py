import matplotlib.pyplot as plt

class Graficar():
    def __init__(self, mapa, dict_ruta):
        self.__mapa = mapa.mapa()
        self.__lugares = mapa.lugares
        self.__coordenadas = mapa.coordenadas()
        self.__rutas = dict_ruta['Ruta']

    @property
    def mapa(self):
        return self.__mapa

    @mapa.setter
    def mapa(self, new_value):
        self.__mapa = new_value

    @property
    def lugares(self):
        return self.__lugares

    @lugares.setter
    def lugares(self, new_value):
        self.__lugares = new_value

    @property
    def coordenadas(self):
        return self.__coordenadas

    @coordenadas.setter
    def coordenadas(self, new_value):
        self.__coordenadas = new_value

    @property
    def rutas(self):
        return self.__rutas

    @rutas.setter
    def rutas(self, new_value):
        self.__rutas = new_value

    def graficar_una(self, index):
        n_origen = self.__rutas[index-1]
        n_destino = self.__rutas[index]
        print(f'va de {self.__lugares[n_origen]} a {self.__lugares[n_destino]}')
        coordenadas = self.__coordenadas
        origen = coordenadas[n_origen]
        destino = coordenadas[n_destino]
        origen_nodo = ox.nearest_nodes(self.__mapa, X=origen[1], Y=origen[0])
        destino_nodo = ox.nearest_nodes(self.__mapa, X=destino[1], Y=destino[0])
        ruta = nx.shortest_path(self.__mapa, origen_nodo, destino_nodo, weight='length')
        ox.plot_graph_route(
            self.__mapa,
            ruta,
            route_linewidth=4,
            node_size=0,
            bgcolor='black',
            show=False,
            close=False
        )
        fig = plt.gcf()
        return fig
