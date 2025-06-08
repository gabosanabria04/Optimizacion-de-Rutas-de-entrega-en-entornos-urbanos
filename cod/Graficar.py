import matplotlib.pyplot as plt
class Graficar():
    def __init__(self, mapa, rutas: list):
        self.__mapa = mapa.mapa()
        self.__lugares = mapa.lugares
        self.__coordenadas = mapa.coordenadas()
        self.__rutas = rutas

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