import Dijkstra

def main():

    print("Welcome to our program!\nHow can we help you? \n")
    ch = int(input("\t1- I wish to update the graph(map)\n\t2- I wish to leave from one place to another\n\t3- I wish to leave from a place to many others\n\t4- Quit\nYour Choice: "))

    match ch:
        case 1:
            graph = Dijkstra.read_file_graph('Graph_Input.txt')
            u = int(input("Updated start location: ")) #start location
            v = int(input("Updated destination: "))
            Distance = input("Its distance in km: ")
            Delay_time = input("Delay time in hrs: ")
            Fuel_consumption = 0.05
               #updating the graph
            graph = Dijkstra.update_graph(graph, u, v, Distance, Delay_time, Fuel_consumption)
               #updating the graph in the file
            Dijkstra.write_txt_graph(graph, 'Graph_Input.txt')

            print("You just updated the graph and the file.")

        case 2:
            graph = Dijkstra.read_file_graph('Graph_Input.txt')
            start = int(input("Your starting location: "))
            end = int(input("Your destination: "))

             #lets find the most economical path
            path, cost = Dijkstra.Dijkstras(graph, start, end)

            displayR = str(path[0]) 

            for i in range(1,len(path)):
                displayR = displayR + " -> " + str(path[i])

            print(f"\nFollow this path, it's shortest: {displayR}\n")    
            print(f"Total cost: £{cost:.2f}")
            print("\n")

        case 3:
            graph = Dijkstra.read_file_graph('Graph_Input.txt')
            start = int(input("Your starting location: "))
            destinations = list(map(int, input("Your destinations: ").split()))

            cost, visited_path = Dijkstra.multiple_destinations(graph, start, destinations)
            
            display = str(visited_path[0]) 

            for i in range(1,len(visited_path)):
                display = display + " -> " + str(visited_path[i])

            List = []
            for i in range(len(visited_path)-1):
                path, cost1 = Dijkstra.Dijkstras(graph, visited_path[i], visited_path[i+1])
                List.append(path)  

            print(f"\nFollow this path, it's shortest: {display}\n")
            print(f"Total cost: £{cost:.2f}\n")
            print("You're also provided with the most economical path between each pair: \n")

            for sublist in List:
                displayRoute = str(sublist[0])
                for i in range(1,len(sublist)):
                    displayRoute = displayRoute + " -> " + str(sublist[i])
                couple = "(" + str(sublist[0]) + "," + str(sublist[len(sublist)-1]) + ")"  
                print(f"{couple} : {displayRoute}")  

            print("\n")

        case _:
            print("Invalid choice... Cow")


if __name__ == "__main__":
    main()