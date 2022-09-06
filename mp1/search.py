# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)
import math

visited_queue = []


def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
        "astar_m": astar_multi_points,
    }.get(searchMethod)(maze)


def bfs(maze):
    route_queue = []
    stack = [maze.getStart()]
    result = bfs_search_func(maze, [], [stack])
    # TODO: Write your code here
    # return path, num_states_explored
    return result[1], len(visited_queue)


def bfs_search_func(maze, fathers, search_queues):
    global visited_queue
    next_search_queue = []
    next_fathers = []
    for search_queue in search_queues:
        for point in search_queue:
            if not (point in visited_queue):
                if maze.isObjective(point[0], point[1]):
                    route = [point]
                    route.insert(0, fathers[search_queues.index(search_queue)])
                    return [True, route]
                visited_queue.append(point)
                next_search_queue.append(maze.getNeighbors(point[0], point[1]))
                next_fathers.append(point)
    result = bfs_search_func(maze, next_fathers, next_search_queue)
    if result[0]:
        for search_queue in search_queues:
            if search_queue.__contains__(result[1][0]):
                if len(fathers) > 0:
                    result[1].insert(0, fathers[search_queues.index(search_queue)])
                return result


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    result = dfs_search_func(maze, [maze.getStart()], maze.getStart())

    return result[1], len(visited_queue)


def dfs_search_func(maze, finalized_queue_, start_point):
    global visited_queue
    neighbors = maze.getNeighbors(start_point[0], start_point[1])
    finalized_queue = finalized_queue_
    # Generate the new queue
    visited_queue.append(start_point)
    for point in neighbors:
        if not (point in visited_queue):
            # Go through the valid neighbors
            finalized_queue.append(point)
            if maze.isObjective(point[0], point[1]):
                return [True, finalized_queue]
            result = dfs_search_func(maze, finalized_queue, point)
            if result[0]:
                return [True, result[1]]
            else:
                finalized_queue.remove(point)
                pass
    return [False]


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    result = greedy_search_func(maze, [maze.getStart()], maze.getStart())
    return result[1], len(visited_queue)


def get_manhattan_dist(point, objective):
    return abs(point[0] - objective[0]) + abs(point[1] - objective[1])


def greedy_search_func(maze, finalized_queue_, start_point):
    global visited_queue
    objective = maze.getObjectives()
    objective = objective[0]
    neighbors = maze.getNeighbors(start_point[0], start_point[1])
    searched_queue = []
    for point in neighbors:
        searched_queue.append({"point": point, "dist": get_manhattan_dist(point, objective, 0)})
    searched_queue = sorted(searched_queue, key=lambda i: i['dist'])

    finalized_queue = finalized_queue_
    # Generate the new queue
    visited_queue.append(start_point)
    for point in searched_queue:
        if not (point["point"] in visited_queue):
            # Go through the valid neighbors
            finalized_queue.append(point["point"])
            if maze.isObjective(point["point"][0], point["point"][1]):
                return [True, finalized_queue]
            result = greedy_search_func(maze, finalized_queue, point["point"])
            if result[0]:
                return [True, result[1]]
            else:
                finalized_queue.remove(point["point"])
                pass
    return [False]


'''
def astar(maze):
    result = astar_search_func(maze, [], maze.getStart())
    # return path, num_states_explored
    return result[1], len(visited_queue)

'''


def astar(maze):
    result = astar_search_route(maze, maze.getStart(), maze.getObjectives()[0])
    # # return path, num_states_explored
    return result


def astar_multi_points(maze):
    result = astar_search_func_multipoint(maze, maze.getStart())
    return result


def astar_search_route(maze, start, objective):
    """Open List elements structure (point, father, known dist + estimate dist)"""

    search_start_p = {"point": start, "father": (), "dist": 0, "est_dist": get_manhattan_dist(start, objective)}
    open_list = [search_start_p]
    visited_list = [search_start_p]
    count = 0
    while not search_start_p["point"] == objective:

        """Dead end check"""
        is_dead_end = True
        idx = 0

        open_list_points = []
        visited_list_points = []
        for i in open_list:
            open_list_points.append(i["point"])
        for i in visited_list:
            visited_list_points.append(i["point"])

        while is_dead_end:
            """Spread the boundary from the search point"""
            search_start_p = open_list[idx]

            for point in maze.getNeighbors(search_start_p["point"][0], search_start_p["point"][1]):
                if point not in open_list_points and point not in visited_list_points:
                    open_list.append(
                        {"point": point, "father": search_start_p["point"], "dist": search_start_p["dist"] + 1,
                         "est_dist": search_start_p["dist"] + 1 + get_manhattan_dist(point, objective)})
                    visited_list.append(open_list[-1])
                    is_dead_end = False
                if point == objective:
                    '''Enable loop for first point'''
                    visited_list.append(
                        {"point": point, "father": search_start_p["point"], "dist": search_start_p["dist"] + 1,
                         "est_dist": search_start_p["dist"] + 1 + get_manhattan_dist(point, objective)})
                    visited_list_points.append(point)
                    close_list = [point]
                    while start not in close_list:
                        child = close_list[0]
                        child_index = visited_list_points.index(child)
                        child_node = visited_list[child_index]
                        father = child_node["father"]
                        close_list.insert(0, father)
                    return close_list, len(visited_list)

            idx += 1
        open_list.remove(search_start_p)
        open_list = sorted(open_list, key=lambda j: j['est_dist'])
        """Update search point"""
        search_start_p = open_list[0]
    return [start, objective], 0


def astar_search_func_multipoint(maze, start_point):
    global visited_queue
    objectives = maze.getObjectives()
    objectives.insert(0, maze.getStart())

    result = []

    '''Generate the map'''
    routes = []
    explored = []
    visited = []
    for i in range(len(objectives)):
        visited.append(False)
        routes_j = []
        explored_j = []
        for j in range(len(objectives)):
            single_route, count = astar_search_route(maze, objectives[i], objectives[j])
            routes_j.append(single_route)
            explored_j.append(count)
        routes.append(routes_j)
        explored.append(explored_j)
    target_count = len(objectives)
    visited[0] = True
    current_idx = 0
    explored_count = 0
    while target_count > 1:
        min_idx = 0
        min_dist = maze.rows * maze.cols
        for i in range(len(objectives)):
            if (not visited[i]) and len(routes[current_idx][i]) < min_dist:
                min_dist = len(routes[current_idx][i])
                min_idx = i
        result += routes[current_idx][min_idx]
        explored_count += explored[current_idx][min_idx]
        if target_count > 2:
            result.pop()
        visited[min_idx] = True
        target_count -= 1
        current_idx = min_idx

    return result, explored_count
