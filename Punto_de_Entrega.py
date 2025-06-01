

class Punto_de_Entrega:
    def __init__(self, latitud, longitud, nombre):
        self.__latitud = latitud
        self.__longitud = longitud
        self.__nombre = nombre

    @property
    def latitud(self):
        return self.__latitud

    @latitud.setter
    def latitud(self, lat):
        self.__latitud = lat

    @property
    def longitud(self):
        return self.__longitud

    @longitud.setter
    def longitud(self, long):
        self.__longitud = long

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

    def __str__(self):
        return f"Punto: {self.__nombre} (Latitud: {self.__latitud}, Longitud: {self.__longitud})"
