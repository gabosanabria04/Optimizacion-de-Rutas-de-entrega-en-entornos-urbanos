import folium
import osmnx as ox
import networkx as nx
from folium.plugins import TimestampedGeoJson
from datetime import datetime, timedelta

class VisualizarFolium:
    def __init__(self, mapa_obj, ruta_indices):
        self.__mapa = mapa_obj.mapa()
        self.__coordenadas = mapa_obj.coordenadas()
        self.__ruta_indices = ruta_indices
        self.__lugares = mapa_obj.lugares

    def crear_mapa(self):
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
