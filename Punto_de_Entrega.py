from geopy.distance import geodesic

class Punto_de_Entrega:
    def __init__(self, latitud, longitud, nombre):
        self.nombre = nombre 
        self.latitud = latitud
        self.longitud = longitud
        
        