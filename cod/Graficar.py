import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx

class Graficar():
    def __init__(self, mapa, dict_ruta: dict):
        '''
        Constructor de la clase Graficar.

        Parameters
        ----------
        mapa : Mapa
            Objeto de la clase Mapa.
        dict_ruta : dict
            Diccionario con datos de enrutamiento.

        Returns
        -------
        None.

        '''
        self.__mapa = mapa.mapa()
        self.__lugares = mapa.lugares
        self.__coordenadas = mapa.coordenadas()
        self.__rutas = dict_ruta['Ruta']

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
    def lugares(self):
        '''
        Getter del atributo lugares.

        Returns
        -------
        list
            Lista con los nombres de los lugares de interés.

        '''
        return self.__lugares

    @lugares.setter
    def lugares(self, new_value: list):
        '''
        Setter del atributo lugares.

        Parameters
        ----------
        new_value : list
            Lista con los nombres de los nuevos lugares de interés.

        Returns
        -------
        None.

        '''
        self.__lugares = new_value

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
            Lista con las nuevas coordenadas de los lugares de interés.

        Returns
        -------
        None.

        '''
        self.__coordenadas = new_value

    @property
    def rutas(self):
        '''
        Getter del atributo rutas.

        Returns
        -------
        list
            El recorrido de la ruta, en formato lista.

        '''
        return self.__rutas

    @rutas.setter
    def rutas(self, new_value: list):
        '''
        Setter del atributo rutas.

        Parameters
        ----------
        new_value : list
            Nuevo recorrido de la ruta.

        Returns
        -------
        None.

        '''
        self.__rutas = new_value

    def __str__(self):
        '''
        Método str de la clase Graficar.

        Returns
        -------
        str
            Descripción del objeto y sus atributos.

        '''
        return f'''Este es un objeto de la clase Graficar con:
            Mapa: {self.__mapa}
            Lugares: {self.__lugares}
            Coordenadas: {self.__coordenadas}
            Ruta: {self.__ruta}
            '''

    def graficar_una(self, index: int):
        '''
        Grafica una parte de la ruta, utilizando el mapa asociado al objeto.

        Parameters
        ----------
        index : int
            Número de recorrido deseado. Empieza en 1.

        Returns
        -------
        fig : Figure
            Gráfico del recorrido indicado.

        '''
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
