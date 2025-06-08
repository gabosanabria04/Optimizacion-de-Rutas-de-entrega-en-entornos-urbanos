from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
class Enrutamiento():
    def __init__(self, matriz, depot: int, matriz_costo = None):
        '''
        Constructor de la clase Enrutamiento

        Parameters
        ----------
        matriz : numpy.ndarray
            Matriz de distancias entre los lugares.
        depot : int
            Índice del lugar de inicio (y fin).
        matriz_costo : numpy.ndarray
            Matriz de costos. Opcional, por defecto, la matriz de distancias.

        Returns
        -------
        None.

        '''
        self.__data = {
            "distance_matrix": matriz,
            "num_vehicles": 1,
            "depot": depot
        }
        self.__manager = pywrapcp.RoutingIndexManager(
            len(self.__data["distance_matrix"]), self.__data["num_vehicles"], self.__data["depot"]
        )
        self.__routing = pywrapcp.RoutingModel(self.__manager)
        if matriz_costo == None:
            self.__matriz_costo = matriz
        else:
            self.__matriz_costo = matriz_costo

    @property
    def data(self):
        '''
        Getter de los datos para el enrutamiento.

        Returns
        -------
        dict
            Diccionario con la matriz de distancias, el número de vehículos y el lugar de inicio.

        '''
        return self.__data

    @data.setter
    def data(self, new_value: dict):
        '''
        Setter de los datos para el enrutamiento.

        Parameters
        ----------
        new_value : dict
            Diccionario con la matriz de distancias, el número de vehículos y el lugar de inicio..

        Returns
        -------
        None.

        '''
        self.__data = new_value

    @property
    def manager(self):
        '''
        Getter del atributo manager.

        Returns
        -------
        ortools.constraint_solver.pywrapcp.RoutingIndexManager
            Manager actual.

        '''
        return self.__manager

    @manager.setter
    def manager(self, new_value):
        '''
        Setter del atributo manager.

        Parameters
        ----------
        new_value : ortools.constraint_solver.pywrapcp.RoutingIndexManager
            Nuevo manager.

        Returns
        -------
        None.

        '''
        self.__manager = new_value

    @property
    def routing(self):
        '''
        Getter del atributo routing.

        Returns
        -------
        ortools.constraint_solver.pywrapcp.RoutingModel
            Routing actual.

        '''
        return self.__routing

    @routing.setter
    def routing(self, new_value):
        '''
        Setter del atributo routing.

        Parameters
        ----------
        new_value : ortools.constraint_solver.pywrapcp.RoutingModel
            Nuevo routing.

        Returns
        -------
        None.

        '''
        self.__routing = new_value

    @property
    def matriz_costo(self):
        '''
        Getter de la matriz de costos.

        Returns
        -------
        numpy.ndarray
            Matriz con los costos de transporte entre cada lugar.
        '''
        return self.__matriz_costo
    
    @matriz_costo.setter
    def matriz_costo(self, new_value):
        '''
        Setter de la matriz de costos.

        Parameters
        ----------
        new_value : numpy.ndarray
            Nueva matriz de costos de transporte entre cada lugar.

        Returns
        -------
        None.

        '''
        self.__matriz_costo = new_value
        
    def __str__(self):
        return f'''Este es un objeto de Enrutamiento, que utilizará
                Datos: {self.__data} 
                Manager: {self.__manager}
                Routing: {self.__routing}
                Matriz de costo: {self.__matriz_costo}
                '''

    def distance_callback(self, from_index, to_index):
        '''
        Calcula el costo de ir de un nodo a otro. Los parámetros son propios de ortools.
        Utiliza la matriz de costos si se proporcionó una.

        Parameters
        ----------
        from_index : automático
        to_index : automático

        Returns
        -------
        float
            Costo de ir de un nodo a otro.
        '''
        from_node = self.__manager.IndexToNode(from_index)
        to_node = self.__manager.IndexToNode(to_index)
        return self.__matriz_costo[from_node][to_node]
        
    def enrutar(self):   
        '''
        Retorna la ruta más económica, según la matriz de costos.

        Returns
        -------
        dict_solucion : dict
            Diccionario con la distancia objetivo, la distancia del recorrido y la ruta.
            plan_output : list
                Recorrido óptimo en formato lista.
            recorrido_objetivo : str
                Recorrido objetivo en kilómetros.
            recorrido_total : str
                Recorrido total en kilómetros.
        '''
        transit_callback_index = self.__routing.RegisterTransitCallback(
            lambda from_index, to_index: self.distance_callback(from_index, to_index)
        )
        print(transit_callback_index)
        self.__routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        solution = self.__routing.SolveWithParameters(search_parameters)

        index = self.__routing.Start(0)
        plan_output = []
        route_distance = 0

        while not self.__routing.IsEnd(index):
            plan_output.append(self.__manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(self.__routing.NextVar(index))
            route_distance += self.__routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output.append(self.__manager.IndexToNode(index))
        recorrido_objetivo = f'{solution.ObjectiveValue()} km'
        recorrido_total = f'{route_distance} km'
        if solution:
            dict_solucion = {
                "Objetivo": recorrido_objetivo,
                "Ruta": plan_output,
                "Recorrido total": recorrido_total
            }
        return dict_solucion
