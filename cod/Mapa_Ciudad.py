

from Punto_de_Entrega import Punto_de_Entrega


class Mapa_Ciudad:
    def _init_(self):
        self.__puntos = []

    @property
    def puntos(self):
        return self.__puntos

    @puntos.setter
    def puntos(self, list_puntos):
        self.__puntos = list_puntos

    def agregar_punto(self, punto):
        self.__puntos.append(punto)
        
        
    def obtener_distancia(self, i, j):
        
        distancia = self._puntos[i].calcular_distancia(self._puntos[j])
        return round(distancia, 2)

    def matriz_distancias(self):
        n = len(self.__puntos)
        matriz = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    matriz[i][j] = self.obtener_distancia(i, j)
        return matriz

    def _str_(self):
        
        salida = "Puntos registrados en la ciudad:\n"
        for idx, punto in enumerate(self.__puntos):
            salida += f"{idx}. {punto}\n"
        return salida