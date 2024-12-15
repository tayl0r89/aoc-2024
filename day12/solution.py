
from typing import List, Tuple, Dict

Position = Tuple[int,int]

def read_file(path) -> Dict[Position, str]:
    with open(path) as file:
        view = {
            (x,y): str(val)
            for y, line in enumerate(file.readlines())
            for x, val in enumerate(list(line.strip()))
        }
        return view
    raise ValueError("Failed to load file")

def get_diagonal_coords(current: Position) -> List[Position]:
    return [
        (current[0] - 1, current[1] - 1), # Left, Up
        (current[0] + 1, current[1] - 1), # Right, Up
        (current[0] - 1, current[1] + 1), # Left, Down
        (current[0] + 1, current[1] + 1) # Right, DOwn
    ]

def get_neighbour_coords(current: Position) -> List[Position]:
    return [
        (current[0], current[1] - 1),
        (current[0], current[1] + 1),
        (current[0] - 1, current[1]),
        (current[0] + 1, current[1])
    ]

def get_neighbours(current: Position, view: Dict[Position, str], seen: set[Position], include_diagonal=False) -> List[Position]:
    val = view[current]
    if not val:
        raise ValueError("Get neighbours called with bad position.")
    
    neighbours = get_neighbour_coords(current)
    if include_diagonal:
        neighbours = [*neighbours, *get_diagonal_coords(current)]

    return [n for n in neighbours if not n == None and not n in seen and view.get(n) == view.get(current)]

def get_missing(current: Position, view: Dict[Position, str]):
    val = view[current]
    if not val:
        raise ValueError("Get neighbours called with bad position.")
    
    neighbours = get_neighbour_coords(current)
    neighbours = [*neighbours, *get_diagonal_coords(current)]

    return [n for n in neighbours if not n == None and view.get(n) == None]


def get_perimeter(items: List[Position]) -> int:
    total = 0
    for current in items:
        possible_neighbours = get_neighbour_coords(current)
        actual_neighbours = [c for c in possible_neighbours if c in items]

        if len(actual_neighbours) == 4:
            total = total + 0
        elif len(actual_neighbours) == 3:
            total = total + 1
        elif len(actual_neighbours) == 2:
            total = total + 2
        elif len(actual_neighbours) == 1:
            total = total + 3
        elif len(actual_neighbours) == 0:
            total = total + 4
    return total

def rotate(heading):
    if heading == (1,0):
        return (0,1)
    elif heading == (0,1):
        return (-1,0)
    elif heading == (-1,0):
        return (0, -1)
    elif heading == (0, -1):
        return (1,0)
    raise ValueError("BAD ROTATE")

Edge = Tuple[Position, Position]
def node_to_edge(pos: Position, view: Dict[Position, str]) -> List[Edge]:
    n_count = len(get_neighbours(pos, view, seen=set()))
    if n_count == 4:
        return []
    return [(pos, (pos[0] + 1, pos[1])), (pos, (pos[0], pos[1] + 1))]


def get_direction(e: Edge) -> Position:
    direction = (e[1][0] - e[0][0], e[1][1] - e[0][1])
    return (0 if direction[0] > 0 else 1, 0 if direction[1] > 0 else 1)


def get_sides(nodes: List[Position], view: Dict[Position, str]) -> int:
    mini_view = {}
    for node in nodes:
        mini_view[node] = view.get(node)
    total = 0
    for n in nodes:
        sides = count_corners(n, mini_view)
        total = total + sides 
    return total        

def count_corners(pos: Position, view: Dict[Position, str]) -> int:
    # res = view.get(pos)

    up = 0 if view.get((pos[0], pos[1] - 1)) is None else 1
    down = 0 if view.get((pos[0], pos[1] + 1)) is None else 1
    left = 0 if view.get((pos[0] - 1, pos[1])) is None else 1
    right = 0 if view.get((pos[0] + 1, pos[1]))  is None else 1
    up_left = 0 if view.get((pos[0] - 1, pos[1] - 1)) is None else 1
    up_right = 0 if view.get((pos[0] + 1, pos[1] - 1)) is None else 1
    down_left = 0 if view.get((pos[0] - 1, pos[1] + 1)) is None else 1
    down_right = 0 if view.get((pos[0] + 1, pos[1] + 1)) is None else 1

    corners = 0

    around = [up, up_right, right, down_right, down, down_left, left, up_left]
    total_around = sum(around)
    if total_around == 0:
        return 4

    # Corner spaces
    if not up_left and (up and left):
        corners = corners + 1
    if not up_right and (up and right):
        corners = corners + 1
    if not down_left and (down and left):
        corners = corners + 1
    if not down_right and (down and right):
        corners = corners + 1

    if not up:
        if up_left + left == 0:
            corners = corners + 1
    if not down:
        if down_right + right == 0:
            corners = corners + 1
    if not left:
        if down_left + down == 0:
            corners = corners + 1
    if not right:
        if up_right + up == 0:
            corners = corners + 1

    # CHeckerboard
    if not down and not right and down_right:
        corners = corners + 1
    if not up and not left and up_left:
        corners = corners + 1
    if not left and not down and down_left:
        corners = corners + 1
    if not right and not up and up_right:
        corners = corners + 1

    return corners

def part_one(view: Dict[Position,str]) -> int:
    seen = set()
    total = 0
    total_sides = 0
    for pos, val in view.items():
        if pos in seen:
            continue
        seen.add(pos)
        current = set()
        current.add(pos)

        next = get_neighbours(pos, view, seen)

        while len(next) > 0:
            test = next.pop()
            if not test in seen:
                seen.add(test)
                current.add(test)
                neighbours = get_neighbours(test, view, seen)
                next = [*next, *neighbours]

        perimeter = get_perimeter(list(current))
        sides = get_sides(list(current), view)
        # print(f"A region of {val} plants with price {len(current)} * {perimeter} = {len(current) * perimeter}")
        print(f"A region of {val} plants with price {len(current)} * {sides} = {len(current) * sides}")
        # print(f"It has {sides} sides")
        total = total + (len(current) * perimeter)
        total_sides = total_sides + (len(current) * sides)
        # break
    return total, total_sides


if __name__ == "__main__":
    view = read_file("input.txt")
    print(part_one(view))
    