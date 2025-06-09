import folium
import osmnx as ox
import networkx as nx


class MapaInteractivo:
    def __init__(self, mapa_obj, dict_ruta: dict):
        '''
        Constructor de la clase MapaInteractivo.

        Parameters
        ----------
        mapa_obj : Mapa
            Objeto de tipo Mapa con los lugares de interés.
        dict_ruta : dict
            Diccionario con la información sobre la ruta a seguir.

        Returns
        -------
        None.

        '''
        self.__mapa = mapa_obj.mapa()
        self.__coordenadas = mapa_obj.coordenadas()
        self.__ruta_indices = dict_ruta['Ruta']
        self.__lugares = mapa_obj.lugares

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
            Nuevo mapa alrededor de los lugares de interés.

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
            Lista con coordenadas de los lugares de interés.

        '''
        return self.__coordenadas

    @coordenadas.setter
    def coordenadas(self, new_value: list):
        '''
        Setter del atributo coordenadas.

        Parameters
        ----------
        new_value : list
            Lista con coordenadas de los nuevos lugares de interés.

        Returns
        -------
        None.

        '''
        self.__coordenadas = new_value

    @property
    def ruta_indices(self):
        '''
        Getter de la ruta a seguir.

        Returns
        -------
        list
            Lista de índices de los lugares en el orden de la ruta a seguir.

        '''
        return self.__ruta_indices

    @ruta_indices.setter
    def ruta_indices(self, new_value: list):
        '''
        Setter de la ruta a seguir.

        Parameters
        ----------
        new_value : list
            Nueva lista de índices de los lugares, en el orden de la ruta a seguir.
            Los índices de los lugares deben coincidir con el orden de los lugares asociados a este objeto.

        Returns
        -------
        None.

        '''
        self.__ruta_indices = new_value

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
        Método str de la clase MapaInteractivo.

        Returns
        -------
        str
            Descripción del objeto y sus atributos.

        '''
        return f'''Este es un objeto de tipo MapaInteractivo con:
            Mapa: {self.__mapa}
            Coordenadas: {self.__coordenadas}
            Ruta: {self.__ruta_indices}
            Lugares: {self.__lugares}
            '''

    def crear_mapa(self):
        '''
        Retorna un mapa con la ruta a seguir.

        Returns
        -------
        mapa : folium.folium.Map
            Mapa con la ruta a seguir.
            Es convertible a formato html.

        '''
        mapa = folium.Map(location=self.__coordenadas[0], zoom_start=14)

        for i in range(len(self.__ruta_indices) - 1):
            idx_origen = self.__ruta_indices[i]
            idx_destino = self.__ruta_indices[i + 1]

            coord_origen = self.__coordenadas[idx_origen]
            coord_destino = self.__coordenadas[idx_destino]

            nodo_origen = ox.nearest_nodes(self.__mapa, X=coord_origen[1], Y=coord_origen[0])
            nodo_destino = ox.nearest_nodes(self.__mapa, X=coord_destino[1], Y=coord_destino[0])

            try:
                ruta_nodos = nx.shortest_path(self.__mapa, nodo_origen, nodo_destino, weight='length')
                ruta_coords = [(self.__mapa.nodes[n]['y'], self.__mapa.nodes[n]['x']) for n in ruta_nodos]

                ruta_coords.insert(0, coord_origen)
                ruta_coords.append(coord_destino)

                folium.PolyLine(ruta_coords, color='blue', weight=5, opacity=0.8).add_to(mapa)
            except nx.NetworkXNoPath:
                continue

        for idx in self.__ruta_indices:
            coord = self.__coordenadas[idx]
            folium.Marker(
                location=coord,
                icon=folium.Icon(color='red', icon='info-sign'),
                popup=self.__lugares[idx]
            ).add_to(mapa)

        destino_idx = self.__ruta_indices[-1]
        folium.Marker(
            location=self.__coordenadas[destino_idx],
            icon=folium.Icon(color='green', icon='flag'),
            popup="Destino final"
        ).add_to(mapa)

        return mapa
    def crear_mapa_interactivo(self):
        '''
        Retorna un mapa interactivo con la ruta a seguir.

        Returns
        -------
        mapa : folium.folium.Map
            Mapa interactivo con la ruta a seguir.
            El mapa permite seleccionar el número de tramo a mostrar.
            Convertible a formato html.

        '''
        mapa = folium.Map(location=self.__coordenadas[self.__ruta_indices[0]], zoom_start=14)
    
        for idx in self.__ruta_indices:
            coord = self.__coordenadas[idx]
            folium.Marker(
                location=coord,
                icon=folium.Icon(color='red', icon='info-sign'),
                popup=self.__lugares[idx]
            ).add_to(mapa)
    
        destino_idx = self.__ruta_indices[-1]
        folium.Marker(
            location=self.__coordenadas[destino_idx],
            icon=folium.Icon(color='green', icon='flag'),
            popup="Destino final"
        ).add_to(mapa)
    
        for i in range(len(self.__ruta_indices) - 1):
            idx_origen = self.__ruta_indices[i]
            idx_destino = self.__ruta_indices[i + 1]
    
            coord_origen = self.__coordenadas[idx_origen]
            coord_destino = self.__coordenadas[idx_destino]
    
            nodo_origen = ox.nearest_nodes(self.__mapa, X=coord_origen[1], Y=coord_origen[0])
            nodo_destino = ox.nearest_nodes(self.__mapa, X=coord_destino[1], Y=coord_destino[0])
    
            try:
                ruta_nodos = nx.shortest_path(self.__mapa, nodo_origen, nodo_destino, weight='length')
                ruta_coords = [(self.__mapa.nodes[n]['y'], self.__mapa.nodes[n]['x']) for n in ruta_nodos]
    
                ruta_coords.insert(0, coord_origen)
                ruta_coords.append(coord_destino)
    
                capa = folium.FeatureGroup(name=f"Tramo {i+1}")
                folium.PolyLine(
                    ruta_coords,
                    color='blue',
                    weight=5,
                    opacity=0.8,
                    popup=f"Ruta del tramo {i+1}"
                ).add_to(capa)
                capa.add_to(mapa)
            except nx.NetworkXNoPath:
                continue
    
        folium.LayerControl().add_to(mapa)
        return mapa
