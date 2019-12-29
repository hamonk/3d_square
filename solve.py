import copy

class Tile():
    """Class representing a tile and its actions."""
    def __init__(self, bugs):
        self.bugs = bugs

    def rotate(self, angle, direction="counterclockwise"):
        rotated_bug = list(self.bugs)
        for x in range(angle):
            rotated_bug = list(self.rotate_one(rotated_bug, direction=direction))
        return Tile(rotated_bug)

    def is_empty(self):
        return len(self.bugs) == 0

    def __getitem__(self, i):
        return self.bugs[i]

    def __str__(self):
        return "_".join([str(x) for x in self.bugs])

    @staticmethod
    def rotate_one(l, direction="counterclockwise"):
        if direction == "counterclockwise":
            return l[1:] + [l[0]]
        else:
            return [l[-1]] + l[:-1]

class Square:
    """Class representing the square."""
    def __init__(self):
        empty_line = [Tile([]), Tile([]), Tile([])]
        self.square = [list(empty_line), list(empty_line), list(empty_line)]

    def __str__(self):
        row1 = ",".join([x.__str__() for x in self.square[0]])
        row2 = ",".join([x.__str__() for x in self.square[1]])
        row3 = ",".join([x.__str__() for x in self.square[2]])
        return "\n".join([row1, row2, row3])

    def __setitem__(self, tup, tile):
        row, column = tup
        # print('--update--')
        # print(row)
        # print(column)
        # print(tile)
        self.square[row][column] = tile

    def __getitem__(self, tup):
        row, column = tup
        return self.square[row][column]

    def return_next_tile_to_fill(self):
        """Return the next empty tile (we go from top left to bottom right."""
        for i in range(0,3):
            for j in range(0,3):
                # print(self.square[(i,j)])
                if self.square[i][j].is_empty():
                    #print('Next free: ' + str((i, j)))
                    return (i,j)
        return None

def can_tile_fit_square(current_square, tile):
    """Return boolean: does the tile fits in the next available spot."""

    r, c = current_square.return_next_tile_to_fill()

    if r == 0:
        if c == 0:
            return True
        elif c == 1:
            return current_square[0,0][1] + tile[3] == 0
        elif c == 2:
            return current_square[0,1][1] + tile[3] == 0
    elif r == 1:
        if c == 0:
            return current_square[0,0][2] + tile[0] == 0
        elif c == 1:
            return (current_square[1,0][1] + tile[3] == 0) & (current_square[0,1][2] + tile[0] == 0)
        elif c == 2:
            return (current_square[1,1][1] + tile[3] == 0) & (current_square[0,2][2] + tile[0] == 0)
    elif r ==2:
        if c == 0:
            return current_square[1,0][2] + tile[0] == 0
        elif c == 1:
            return (current_square[2,0][1] + tile[3] == 0) & (current_square[1,1][2] + tile[0] == 0)
        elif c == 2:
            return (current_square[2,1][1] + tile[3] == 0) & (current_square[1,2][2] + tile[0] == 0)

def return_next_options(inputs):
    """Return the list of couple (square, available tiles) given a square and a list of tiles.
    A new possibility is found by finding a tile that fits the current square.
    We try all possibility (all tiles and the 4 rotations)
    """
    current_square, available_tiles = inputs
    square_to_fill = current_square.return_next_tile_to_fill()
    if square_to_fill is None:
        print("square full")
        print(current_square)
        return []
    elif len(available_tiles) == 0:
        print("no more available tiles")
        return []
    else:
        r, c = square_to_fill
        leads = []
        zip_availablle_tiles = zip(range(len(available_tiles)), available_tiles)
        # print(zip_availablle_tiles)

        for tile_num in range(len(available_tiles)):
            tile = zip_availablle_tiles[tile_num][1]
            for rotation in range(0,4):
                tile_to_use = tile.rotate(rotation)
                if can_tile_fit_square(current_square, tile_to_use):
                    new_square = copy.deepcopy(current_square)
                    # print('--in--')
                    # print(r,c)
                    new_square[r, c] = tile_to_use
                    # print(new_square)
                    new_available_tiles = [x[1] for x in zip_availablle_tiles if x[0] != tile_num]
                    leads.append((new_square, new_available_tiles))
                    # print(len(new_available_tiles))
                # else:
                #     print("no fit")

        return leads

def wrapper_call(list_inputs):
    """Wrapper function to call the recursion."""
    leads = []
    for inputs in list_inputs:
        next_leads = return_next_options(inputs)
        leads += next_leads
    return leads

# The "dictionary" number <--> animal
# sauterelle (grasshopper) -1 1 vert orange / green orange
# araignee (spider) -2 2 violet/purple
# coccinelle (lady bug) -3 3 rouge/red
# scarabe (beetle) -4 4 jaune/yellow

##### A tile is a list of 4 numbers representing the animals
#      0
# +--- X ---+
# |         |
# |         |
#3X         X 1
# |         |
# |         |
# +--- X ---+
#      2
#
#####

# List of tiles
tiles = [Tile([-1, 4, 2, 3]), Tile([-1, -3, 2, 4]), Tile([-4, 1, 3, -2]), 
         Tile([-2, 4, 2, -1]), Tile([1, 4, -2, 3]), Tile([4, -4, -1, 3]), 
         Tile([-3, -1, -2, -4]), Tile([2, 3, -3, 1]), Tile([4, 2, -3, -1])]

# Empty square
s = Square()

# Run first iteration (fill 1st upper left corner)
next_leads = return_next_options((s, tiles))
print(len(next_leads))

# Run the other iterations
for x in range(0, 9):
    next_leads = wrapper_call(next_leads)
    print(len(next_leads))

# Prints the solution (4 solutions are actually 1 but rotated 4 times)
# 36
# 146
# 528
# 1629
# 631
# 228
# 355
# 46
# 4
# square full
# -1_-2_4_2,4_-1_-3_2,4_-2_3_1
# -4_-1_3_4,3_-2_-4_1,-3_-1_4_2
# -3_1_2_3,4_2_3_-1,-4_-3_-1_-2
# square full
# -2_3_1_4,-1_4_2_-3,-3_-1_-2_-4
# -1_-3_2_4,-2_-4_1_3,2_3_-1_4
# -2_4_2_-1,-1_3_4_-4,1_2_3_-3
# square full
# -1_-2_-4_-3,3_-1_4_2,2_3_-3_1
# 4_2_-3_-1,-4_1_3_-2,3_4_-4_-1
# 3_1_4_-2,-3_2_4_-1,4_2_-1_-2
# square full
# 3_-3_1_2,4_-4_-1_3,2_-1_-2_4
# -1_4_2_3,1_3_-2_-4,2_4_-1_-3
# -2_-4_-3_-1,2_-3_-1_4,1_4_-2_3


# Some examples

# print(s)
# print('---')

# s[1,1] = t
# s[2,0] = t
# print(s)
# print('Next free: ' + str(s.return_next_tile_to_fill()))

# print(s[0, 0])
# print(s[1, 1])
# s[0,0] = t
# print(s[0, 0])

# print(s[0,0].is_empty())
# print(s[2,1].is_empty())
# print('---')
# print(s)
# print('Next free: ' + str(s.return_next_tile_to_fill()))
