from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
'''
USEFUL FUNCTIONS: player.current_room.id, player.current_room.get_exits() and player.travel(direction)

GOAL: You are provided with a pre-generated graph consisting of 500 rooms. You are responsible for filling
traversal_path with directions that, when walked in order, will visit every room on the map at least once.

STARTING STRATEGY: Start by writing an algorithm that picks a random unexplored direction from the player's
current room, travels and logs that direction, then loops. This should cause your player to walk a
depth-first traversal. When you reach a dead-end (i.e. a room with no unexplored paths), walk back to the
nearest room that does contain an unexplored path.

You can find the path to the shortest unexplored room by using a breadth-first search for a room with a
'?' for an exit. If you use the bfs code from the homework, you will need to make a few modifications.

1. Instead of searching for a target vertex, you are searching for an exit with a '?' as the value. If an
exit has been explored, you can put it in your BFS queue like normal.

2. BFS will return the path as a list of room IDs. You will need to convert this to a list of n/s/e/w
directions before you can add it to your traversal path.
'''

traversal_path = []

reverse_path = []

# graph's key is the room number, the values are directions
graph = {}
graph[player.current_room.id] = player.current_room.get_exits()

# graph[player.current_room.id].pop()
# player.travel('n')
# traversal_path.append('n')
# reverse_path.append('s')


def reverse(a):
        if a == "n":
            return 's'
        elif a == "s":
            return 'n'
        elif a == 'e':
            return 'w'
        elif a == 'w':
            return 'e'

counter = 0

# BREAK EACH SITUATION DOWN, MAKE SURE IT COVERS ALL EDGE CASES AND THEN MOVE ON TO THE NEXT SITUATION

while len(graph) < 500:
    # if we haven't been to this room before
    if player.current_room.id not in graph:
        #counter += 1
        print('new room',player.current_room.id)
        # store it in our graph
        graph[player.current_room.id] = player.current_room.get_exits()

        # identify the last room and remove it from the graph so its not an option
        # this ensures we do not go back down the same path unless we hit a dead end
        last_room = reverse_path[-1]
        graph[player.current_room.id].remove(last_room)

    # if we're at a dead end or a room that we've already passed through all the exits
    elif len(graph[player.current_room.id]) == 0:
        #counter += 1
        print('dead end/backtrack',player.current_room.id)

        # identify the last room
        #print('r',reverse_path)
        last_room = reverse_path[-1]

        # then remove it from the reverse path since we're backtracking
        reverse_path.pop()

        # then add it to the traversal path
        traversal_path.append(last_room)

        # then move back to the last room
        player.travel(last_room)

    # if neither of the above situations apply, ie we're in a room we've been to before
    # and haven't tried all the exits
    else:
        #counter += 1
        print('found new exit',player.current_room.id)
        # identify the last direction listed for the current room
        visit = graph[player.current_room.id][-1]

        # remove the current room from the graph
        graph[player.current_room.id].pop()

        # add the direction to the traversal path
        traversal_path.append(visit)

        # add the reverse of the direction to the reverse path so we can backtrack later 
        reverse_path.append(reverse(visit))

        # move to the next room
        player.travel(visit)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
