from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
class Enrutamiento():
    def __init__(self, matriz, cantidad_vehiculos, depot):
        self.__data = {
            "distance_matrix": matriz,
            "num_vehicles": cantidad_vehiculos,
            "depot": depot
                      }
        self.__manager = pywrapcp.RoutingIndexManager(
            len(self.__data["distance_matrix"]), self.__data["num_vehicles"], self.__data["depot"]
        )
        self.__routing = pywrapcp.RoutingModel(self.__manager)
    def distance_callback(self):
        from_node = self.__manager.IndexToNode(from_index)
        to_node = self.__manager.IndexToNode(to_index)
        return self.__data["distance_matrix"][from_node][to_node]
    
    def enrutar(self):        
        transit_callback_index = self.__routing.RegisterTransitCallback(self.distance_callback()) #falta
        print(transit_callback_index)
        self.__routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
            # https://developers.google.com/optimization/routing/routing_options?hl=es-419#first_solution_strategy
        )
        solution = self.__routing.SolveWithParameters(search_parameters)

        index = self.__routing.Start(0)
        plan_output = "Route for vehicle 0: "
        route_distance = 0

        while not self.__routing.IsEnd(index):
            plan_output += f" {self.__manager.IndexToNode(index)} ->"
            previous_index = index
            index = solution.Value(self.__routing.NextVar(index))
            route_distance += self.__routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output += f" {self.__manager.IndexToNode(index)}"
        if solution:
            dict_solucion = {
                "Objetivo": solution.ObjectiveValue(),
                "Ruta": plan_output,
                "Recorrido total": route_distance
            }
        return dict_solucion