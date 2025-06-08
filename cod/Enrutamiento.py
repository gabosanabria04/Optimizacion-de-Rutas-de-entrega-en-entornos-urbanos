from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
class Enrutamiento():
    def __init__(self, matriz, depot: int):
        '''
        Constructor de la clase Enrutamiento

        Parameters
        ----------
        matriz : np.ndarray
            Matriz de distancias entre los lugares.
        depot : int
            Índice del lugar de inicio (y fin).

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

    def distance_callback(self, from_index, to_index):
        '''
        Calcula el costo de ir de un nodo a otro. Los parámetros son propios de ortools.

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
        return self.__data["distance_matrix"][from_node][to_node]
        
    def enrutar(self):   
        transit_callback_index = self.__routing.RegisterTransitCallback(
            lambda from_index, to_index: self.distance_callback(from_index, to_index)
        )
        print(transit_callback_index)
        self.__routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
            # https://developers.google.com/optimization/routing/routing_options?hl=es-419#first_solution_strategy
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
        if solution:
            dict_solucion = {
                "Objetivo": f'{solution.ObjectiveValue()} km',
                "Ruta": plan_output,
                "Recorrido total": f'{route_distance} km'
            }
        return dict_solucion
