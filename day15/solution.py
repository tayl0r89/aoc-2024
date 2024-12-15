
def read_file(path):
    with open(path) as file:
        starting = None
        board, instructions = file.read().split("\n\n")
        view = {}
        for y, line in enumerate(board.split("\n")):
            for x, item in enumerate(list(line.strip())):
                if item == "@":
                    starting = (x,y)
                view[(x,y)] = item
    
        moves = []
        for line in instructions.split("\n"):
            for move in list(line):
                moves.append(move)

    return view, moves, starting


def read_file_doubled(path):
    with open(path) as file:
        starting = None
        board, instructions = file.read().split("\n\n")
        view = {}
        for y, line in enumerate(board.split("\n")):
            for x, item in enumerate(list(line.strip())):
                if item == "@":
                    starting = (x*2,y)
                    view[((x*2),y)] = "@"
                    view[((x*2) + 1,y)] = "."
                elif item == "O":
                    view[((x*2),y)] = "["
                    view[((x*2) + 1,y)] = "]"
                elif item == ".":
                    view[((x*2),y)] = "."
                    view[((x*2) + 1,y)] = "."
                elif item == "#":
                    view[((x*2),y)] = "#"
                    view[((x*2) + 1,y)] = "#"
                else:
                    raise ValueError("HERE")
    
        moves = []
        for line in instructions.split("\n"):
            for move in list(line):
                moves.append(move)

    return view, moves, starting


def get_direction(move):
    if move == ">":
        return (1, 0)
    elif move == "<":
        return (-1, 0)
    elif move == "v":
        return (0, 1)
    elif move == "^":
        return (0, -1)
    
    raise ValueError(f"BAD DIRECTION {move}")


def can_move(pos, direction, view):
    target = (pos[0] + direction[0], pos[1] + direction[1])
    
    item = view.get(target)
    if not item:
        return False
    elif item == "#":
        return False
    elif item == ".":
        return True
    elif item == "O":
        return can_move(target, direction, view)
    
    raise ValueError(f"Shouldnt get here {item}")

def make_move(pos, direction, view):
    target = (pos[0] + direction[0], pos[1] + direction[1])
    moving = view[pos]
    item = view.get(target)
    if not item or not pos:
        raise ValueError("Fail")
    elif item == "#":
        raise ValueError("Shouldnt be expecting this.")
    elif item == ".":
        view[target] = moving
        view[pos] = "."
        return target
    elif item == "O":
        make_move(target, direction, view)
        item = view.get(target)
        if not item == ".":
            raise ValueError("FAILED TO MOVE OTHERS")
        else:
            view[target] = moving
            view[pos] = "."
            return target
        
def score(view):
    score = 0
    for k, item in view.items():
        if item == "O":
            score = score + (100 * k[1]) + k[0]
    return score

def score_p2(view):
    max_x = max(map(lambda x: x[0], view.keys())) + 1
    max_y = max(map(lambda x: x[1], view.keys())) + 1
    score = 0
    for k, item in view.items():
        if item == "[":
            top_dist = k[1]
            bottom_dist = max_y - k[1]
            left_dist = k[0]
            right_dist = max_x - k[0]
            score = score + (100 * top_dist) + left_dist
    print(score)


def print_view(view):
    coords = view.keys()
    x_max = max(map(lambda x: x[0], coords))
    y_max = max(map(lambda x: x[1], coords))
    for y in range(y_max + 1):
        line = []
        for x in range(x_max + 1):
            line.append(view[(x,y)])
        print("".join(line))


def can_move_doubled(pos, direction, view):
    target = (pos[0] + direction[0], pos[1] + direction[1])
    item = view.get(target)

    if item == "#":
        return False
    elif item == ".":
        return True
    elif item == "[" or item == "]":
        if not direction[0] == 0:
            return can_move_doubled(target, direction, view)
        else:
            if item == "[":
                return can_move_doubled(target, direction, view) and can_move_doubled((target[0] + 1, target[1]), direction, view)
            elif item == "]":
                return can_move_doubled(target, direction, view) and can_move_doubled((target[0] - 1, target[1]), direction, view)
            raise ValueError("BAD INPUT BOX")
    
    print_view(view)
    raise ValueError(f"Shouldnt get here {item}")

def make_move_doubled(pos, direction, view):
    target = (pos[0] + direction[0], pos[1] + direction[1])
    moving = view[pos]
    item = view.get(target)
    if not item or not pos:
        raise ValueError("Fail")
    elif item == "#":
        raise ValueError("Shouldnt be expecting this.")
    elif item == ".":
        view[target] = moving
        view[pos] = "."
        return target
    elif item == "[" or item == "]":
        if not direction[0] == 0:
            make_move_doubled(target, direction, view)
            view[target] = moving
            view[pos] = "."
            return target
        else:
            if item == "[":
                make_move_doubled((target[0] + 1, target[1]), direction, view)
                make_move_doubled(target, direction, view) 
                view[target] = moving
                view[pos] = "."
                return target
            elif item == "]":
                make_move_doubled((target[0] - 1, target[1]), direction, view)
                make_move_doubled(target, direction, view)
                view[target] = moving
                view[pos] = "."
                return target
            else:
                raise ValueError("BAD INPUT BOX")

    raise ValueError(f"END OF MMD {item}")

def part_one(view, moves, start):
    pos = start
    for m in moves:
        direction = get_direction(m)
        if can_move(pos, direction, view):
            pos = make_move(pos, direction, view)
    print(score(view))
    
def part_two(view, moves, start):
    pos = start
    for m in moves:
        direction = get_direction(m)
        if can_move_doubled(pos, direction, view):
            pos = make_move_doubled(pos, direction, view)
    score_p2(view)
    

if __name__ == "__main__":
    file = "input.txt"
    view, moves, start = read_file(file)
    part_one(view, moves, start)
    print("======")

    view, moves, start = read_file_doubled(file)
    part_two(view, moves, start)