import folium
import osmnx as ox
import networkx as nx

class VisualizarFolium:
    def __init__(self, mapa_obj, ruta_indices):
        self.__mapa = mapa_obj.mapa()
        self.__coordenadas = mapa_obj.coordenadas()
        self.__ruta_indices = ruta_indices
        self.__lugares = mapa_obj.lugares

    def crear_mapa(self):
        ruta_coords = []
        ultimo_nodo = None

        for i in range(len(self.__ruta_indices) - 1):
            idx_origen = self.__ruta_indices[i]
            idx_destino = self.__ruta_indices[i + 1]
            origen = self.__coordenadas[idx_origen]
            destino = self.__coordenadas[idx_destino]
            nodo_origen = ox.nearest_nodes(self.__mapa, X=origen[1], Y=origen[0])
            nodo_destino = ox.nearest_nodes(self.__mapa, X=destino[1], Y=destino[0])

            ruta = nx.shortest_path(self.__mapa, nodo_origen, nodo_destino, weight='length')
            coords_ruta = [(self.__mapa.nodes[n]['y'], self.__mapa.nodes[n]['x']) for n in ruta]
            ruta_coords.extend(coords_ruta)

            ultimo_nodo = ruta[-1]

        mapa = folium.Map(location=ruta_coords[0], zoom_start=14)

        for i, coord in enumerate(self.__coordenadas):
            folium.Marker(
                location=coord,
                popup=self.__lugares[i],
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)

        folium.PolyLine(ruta_coords, color='blue', weight=5, opacity=0.7).add_to(mapa)

        if ultimo_nodo:
            coord_final = (self.__mapa.nodes[ultimo_nodo]['y'], self.__mapa.nodes[ultimo_nodo]['x'])
            folium.Marker(
                location=coord_final,
                icon=folium.Icon(color='green', icon='flag'),
                popup="Destino final"
            ).add_to(mapa)

        return mapa

    def crear_mapa_interactivo(self):
        mapa = None
        ultimo_nodo = None

        for i in range(len(self.__ruta_indices) - 1):
            idx_origen = self.__ruta_indices[i]
            idx_destino = self.__ruta_indices[i + 1]
            origen = self.__coordenadas[idx_origen]
            destino = self.__coordenadas[idx_destino]
            nodo_origen = ox.nearest_nodes(self.__mapa, X=origen[1], Y=origen[0])
            nodo_destino = ox.nearest_nodes(self.__mapa, X=destino[1], Y=destino[0])

            ruta = nx.shortest_path(self.__mapa, nodo_origen, nodo_destino, weight='length')
            coords_tramo = [(self.__mapa.nodes[n]['y'], self.__mapa.nodes[n]['x']) for n in ruta]
            ultimo_nodo = ruta[-1]

            if mapa is None:
                mapa = folium.Map(location=coords_tramo[0], zoom_start=14)

            capa = folium.FeatureGroup(name=f"Tramo {i + 1}")
            folium.PolyLine(
                coords_tramo,
                color="blue",
                weight=5,
                opacity=0.8,
                popup=f"De {self.__lugares[idx_origen]} a {self.__lugares[idx_destino]}"
            ).add_to(capa)
            capa.add_to(mapa)

        for i, coord in enumerate(self.__coordenadas):
            folium.Marker(
                location=coord,
                popup=self.__lugares[i],
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)

        if ultimo_nodo:
            coord_final = (self.__mapa.nodes[ultimo_nodo]['y'], self.__mapa.nodes[ultimo_nodo]['x'])
            folium.Marker(
                location=coord_final,
                icon=folium.Icon(color='green', icon='flag'),
                popup="Destino final"
            ).add_to(mapa)

        folium.LayerControl().add_to(mapa)
        return mapa
