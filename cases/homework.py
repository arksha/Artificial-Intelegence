import sys
from Queue import PriorityQueue

'''Node class to store parent'''


class Node:
    def __init__(self, road_name, path_cost, parent):
        self.road_name = road_name
        self.path_cost = path_cost
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_path(self):
        node = self
        path = []
        while node:
            path.insert(0, node)
            node = node.parent
        return path

    def __cmp__(self, other):
        return self.path_cost - other.path_cost

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.road_name == other.road_name
        return False

'''BFS'''


def bfs(outputfile, live_line_array, sunday_line_array, start, goal):# input queue order
    if start == goal:
        outputfile.write(start + " " + str(0) + '\n') # Yaobuyao jia huanhangfu.
        return
    queue = [Node(start, 0, None)]

    explored = []
    while True:
        if queue == []:
            sys.exit("Fail to reach the destination.") # remember handle failure
        node = queue.pop(0)
        #outputfile.write(str(node.road_name) + " " + str(path_cost) + '\n')
        explored.append(node)

        #print "node", node
        if node.road_name in live_line_array:
            children = live_line_array[node.road_name]
        else:
            children = []
        #print "BFS", sorted(children.items())
        for child in children:
            if (child[0] not in [node1.road_name for node1 in explored]) and (child[0] not in [node1.road_name for node1 in queue]):
                new_node = Node(child[0], node.path_cost + 1, node)
                #print "New_node", child[0], node.path_cost + 1, node.road_name
                if child[0] == goal:
                    node_name_list = [node1.road_name for node1 in new_node.get_path()]
                    node_cost_list = [node1.path_cost for node1 in new_node.get_path()]
                    for i in range(len(node_name_list)):
                        outputfile.write(node_name_list[i] + " " + str(node_cost_list[i]) + "\n")
                    #outputfile.write(child[0] + " " + str(path_cost))  # Yaobuyao jia huanhangfu.
                    return
                queue.append(new_node)
                #print "Queue", [node1.road_name for node1 in queue]
                #print "Appended", child[0]


'''DFS'''
# insert in the front


def dfs(outputfile, live_line_array, sunday_line_array, start, goal):
    if start == goal:
        outputfile.write(start + " " + str(0)) # Yaobuyao jia huanhangfu.
        return
    stack = [Node(start, 0, None)]
    explored = []
    while True:
        if stack == []:
            sys.exit("Fail to reach the destination.") # remember handle failure
        node = stack.pop(-1)
        explored.append(node)
        if node.road_name in live_line_array:
            children = live_line_array[node.road_name]
        else:
            children = []
        for child in reversed(children):
            if (child[0] not in [node1.road_name for node1 in explored]) and (child[0] not in [node1.road_name for node1 in stack]):
                new_node = Node(child[0], node.path_cost + 1, node)
                if child[0] == goal:
                    node_name_list = [node1.road_name for node1 in new_node.get_path()]
                    node_cost_list = [node1.path_cost for node1 in new_node.get_path()]
                    for i in range(len(node_name_list)):
                        outputfile.write(node_name_list[i] + " " + str(node_cost_list[i]) + "\n")
                    return
                stack.append(new_node)


'''UCS'''


def ucs(outputfile, live_line_array, sunday_line_array, start, goal):
    #print "ucs>>>"
    priorityqueue = PriorityQueue()
    node = Node(start, 0, None)

    priorityqueue.put(node)
    explored = []
    while True:
        if priorityqueue.empty():
            sys.exit("Fail to reach the destination.")
        node = priorityqueue.get()
        # print "current node path cost:", node.road_name, node.path_cost
        if node.road_name == goal:
            path = node.get_path()
            for pathnode in path:
                outputfile.write(pathnode.road_name + " " + str(pathnode.path_cost) + '\n')
            return


        path_cost = node.path_cost
        # print "node", node

        if node.road_name in live_line_array:
            children = live_line_array[node.road_name]
        else:
            children = []
        for child in children: # remember to sort by cost
            # print "explore", explored
            # print "children", child, children
            newcost = path_cost + child[1]
            child_node = Node(child[0], 0, node)
            #index_child = priorityqueue.queue.index(child_node) if (child_node in priorityqueue.queue) else None
            # if index_child:
            #     print ">>child index:", priorityqueue.queue[index_child].road_name, index_child, priorityqueue.queue[index_child].path_cost
            # print "heap node:", [(pqnode.road_name, pqnode.path_cost, pqnode.parent.road_name) for pqnode in priorityqueue.queue]
            if (child_node not in explored) and (child_node not in priorityqueue.queue):
                priorityqueue.put(Node(child[0], newcost, node))
                print "new put in to heap :", child[0], newcost, node.road_name

                # print "heap node:", [(pqnode.road_name, pqnode.path_cost, pqnode.parent.road_name) for pqnode in priorityqueue.queue]
                print "------------if not in queue and explored:"
            elif child_node in priorityqueue.queue:
                # print "child_ ndoe ", child_node.road_name
                # print "------------if already in queue need update"
                index_child = priorityqueue.queue.index(child_node) if (child_node in priorityqueue.queue) else None
                # print "index child:", index_child
                # print "cost new :", newcost
                if priorityqueue.queue[index_child]:
                    # print "current parent", priorityqueue.queue[index_child].road_name
                    if newcost < priorityqueue.queue[index_child].path_cost:
                        priorityqueue.put(Node(child[0], newcost, node))
                        # priorityqueue.queue[index_child].path_cost = newcost
                        # priorityqueueorityqueue.queue[index_child].parent = node
                        print "heap node:", [(pqnode.road_name, pqnode.path_cost, pqnode.parent.road_name) for pqnode in priorityqueue.queue]
                        print ">>>>>update cost", priorityqueue.queue[index_child].road_name, priorityqueue.queue[index_child].path_cost
            elif child_node in explored:
                print "+++child is in explored"
                print "+++child", child
                print "+++explored", explored
                index_child = explored.index(child_node);
                old_node = explored[index_child]
                print "+++newcost", newcost, old_node.path_cost
                if newcost < old_node.path_cost:
                    print "update OLD NODE"
                    explored.remove(old_node)
                    # print "explored", explored
                    priorityqueue.put(Node(child[0], newcost, node))
        explored.append(node)
        print "EXPLORED:", [e.road_name for e in explored]

''''A*'''


def a_star(outputfile, live_line_array, sunday_line_array, start, goal):
    # print "A star >>>"
    path_cost = {}
    priorityqueue = PriorityQueue()
    node = Node(start, sunday_line_array[start], None)

    priorityqueue.put(node)
    explored = set()
    while not priorityqueue.empty():#
        if priorityqueue.empty():
            sys.exit("Fail to reach the destination.")
        node = priorityqueue.get()
        if node.road_name == goal:
            path = node.get_path()

            for pathnode in path:
                outputfile.write(pathnode.road_name + " " + str(pathnode.path_cost - sunday_line_array[pathnode.road_name]) + '\n')
            return

        path_cost[node.road_name] = node.path_cost
        if node.road_name in live_line_array:
            children = live_line_array[node.road_name]
        else:
            children = []
        # print "path cost (g + h):", path_cost
        # print "heap node >>>>before expand child:", [(pqnode.road_name, pqnode.path_cost, pqnode.parent.road_name) for pqnode in priorityqueue.queue]
        for child in children:
            newcost = path_cost[node.road_name] - sunday_line_array[node.road_name] + child[1]
            # print "newcost", newcost
            # print "g + h score", child[0], newcost + sunday_line_array[child[0]]

            # print "explored", explored
            child_node = Node(child[0], 0, node.road_name)
            # print "child_node", child_node.road_name
            if (child[0] not in explored) and (child_node not in priorityqueue.queue): #exists is dup
                #explored.add(child[0])
                priorityqueue.put(Node(child[0], newcost + sunday_line_array[child[0]], node))
                # print "not in pq or explored"
                # print "heap node:", [(pqnode.road_name, pqnode.path_cost, pqnode.parent.road_name) for pqnode in priorityqueue.queue]
            elif child_node in priorityqueue.queue:
                # print "child_node", child_node.road_name
                index_child = priorityqueue.queue.index(child_node) if (child_node in priorityqueue.queue) else None
                # print "find index in pq: ", priorityqueue.queue[index_child].road_name
                if priorityqueue.queue[index_child]:
                    if (newcost + sunday_line_array[child[0]]) < priorityqueue.queue[index_child].path_cost:
                        priorityqueue.queue[index_child].path_cost = newcost + sunday_line_array[child[0]]
                        priorityqueue.queue[index_child].parent = node
                        # print ">>>update in pq ", child[0], newcost + sunday_line_array[child[0]], node.road_name
                        # print "heap node:", [(pqnode.road_name, pqnode.path_cost, pqnode.parent.road_name) for pqnode in priorityqueue.queue]
            elif child[0] in explored:
                # print "child 0", child
                # print ">>>find in explored"
                if newcost + sunday_line_array[child[0]] < child[1] + path_cost[node.road_name]:
                    explored.remove(child[0])
                    # print "remove in explord", child[0]
                    # print "explored", explored
                    priorityqueue.put(Node(child[0], newcost + sunday_line_array[child[0]], node))
                    # print "heap node:", [(pqnode.road_name, pqnode.path_cost, pqnode.parent.road_name) for pqnode in priorityqueue.queue]
        explored.add(node.road_name)

'''read input file'''
inputfile = open('input.txt', 'r')

algorithm = inputfile.readline().strip()
start = inputfile.readline().strip()
goal = inputfile.readline().strip()

live_lines = eval(inputfile.readline())

live_line_array = {}

for i in range(live_lines):
    edge_str = inputfile.readline()
    e_a, e_b, cost = edge_str.split()
    if e_a not in live_line_array:
        live_line_array[e_a] = []
    live_line_array[e_a].append((e_b, eval(cost)))
# print "live line", live_line_array

sunday_lines = eval(inputfile.readline())

sunday_line_array = {}
for i in range(sunday_lines):
    heuristic_str = inputfile.readline()
    heuristic, cost = heuristic_str.split()
    sunday_line_array[heuristic] = eval(cost)
    # print "sunday array", sunday_line_array

inputfile.close()


outputfile = open('output.txt', 'w')
if algorithm == 'BFS':
    bfs(outputfile, live_line_array, sunday_line_array, start, goal)
if algorithm == 'DFS':
    dfs(outputfile, live_line_array, sunday_line_array, start, goal)
if algorithm == 'UCS':
    ucs(outputfile, live_line_array, sunday_line_array, start, goal)
if algorithm == 'A*':
    a_star(outputfile, live_line_array, sunday_line_array, start, goal)
