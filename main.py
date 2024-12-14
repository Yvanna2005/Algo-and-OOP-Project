import Dijkstra

def main():

    print("Welcome to our program!\nHow can we help you? \n")
    ch = int(input("\t1- I wish to update the graph(map)\n\t2- I wish to leave from one place to another\n\t3- I wish to leave from a place to many others\n\t4- Quit\nYour Choice: "))

    match ch:
        case 1:
            graph = Dijkstra.read_file_graph('Graph_Input.txt')
            u = int(input("Updated start location: "))
            v = int(input("Updated destination: "))
            Distance = input("Its distance in km: ")
            Delay_time = input("Delay time in hrs: ")
            Traffic_cost = input("Traffic cost in £: ")
               #updating the graph
            graph = Dijkstra.update_graph(graph, u, v, Distance, Delay_time, Traffic_cost)
               #updating the graph in the file
            Dijkstra.write_txt_graph(graph, 'Graph_Input.txt')

            print("You just updated the graph and the file.")

        case 2:
            graph = Dijkstra.read_file_graph('Graph_Input.txt')
            start = int(input("Your starting location: "))
            end = int(input("Your destination: "))

             #lets find the most economical path
            path, cost = Dijkstra.Dijkstras(graph, start, end)

            print(f"Most economical path: {path}")
            print(f"Total cost: £{cost:.2f}")

        case 3:
            print("Not operational yet...")

        case _:
            print("Invalid choice... Cow")


if __name__ == "__main__":
    main()