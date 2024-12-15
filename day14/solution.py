from typing import Dict, List, Tuple
from math import ceil

Position = Tuple[int, int]
Vector = Tuple[int, int]
Robot = Tuple[Position, Vector]

def read_file(path) -> Dict[Position, Vector]:
    results = []
    with open(path) as file:
        lines = [x.strip() for x in file.readlines()]
        for l in lines:
            position, vector = l.split(" ")
            nums = list(map(int, position.split("=")[1].split(",")))
            p = (nums[0], nums[1])

            dirs = list(map(int,vector.split("=")[1].split(",")))
            v = (dirs[0], dirs[1])
            results.append((p, v))
    
    return results

def print_positions(positions, bounds):
    for line in pos_to_string(positions, bounds):
        print(line)


def ext_pos_to_string(positions, min_x, max_x, min_y, max_y):
    lines = []
    for y in range(min_y, max_y):
        line = []
        for x in range(min_x, max_x):
            if (x,y) in positions:
                line.append("x")
            else: 
                line.append(".")
        lines.append("".join(line))
    return lines



def pos_to_string(positions, bounds):
    lines = []
    for y in range(bounds[1]):
        line = []
        for x in range(bounds[0]):
            count = positions.get((x,y))
            if count:
                line.append("X")
            else:
                line.append(".")
        lines.append("".join(line))
    return lines

def count_quadrants(positions, bounds):
    x, y = bounds
    half_x = int(x / 2)
    other_half_x = ceil(x / 2)
    half_y = int(y / 2)
    other_half_y = ceil(y / 2)

    q1 = {}
    q2 = {}
    q3 = {}
    q4 = {}

    for p, count in positions.items():
        px, py = p
        if px < half_x:
            if py < half_y:
                q1[p] = count
            elif py >= other_half_y:
                q3[p] = count
        elif px >= other_half_x:
            if py < half_y:
                q2[p] = count
            elif py >= other_half_y: 
                q4[p] = count

    return (q1, q2, q3, q4)    


def get_after_moves(robots: List[Robot], moves, bounds):
    positions = {}
    for p,v in robots:
        x_mult = moves * v[0]
        y_mult = moves * v[1]
        x_offset = abs(x_mult) % bounds[0]
        y_offset = abs(y_mult) % bounds[1]

        if x_mult < 0:
            x_offset = x_offset * -1
        if y_mult < 0:
            y_offset = y_offset * -1

        final_move = (x_offset, y_offset)
        move_x, move_y = final_move
        final_x = p[0] + move_x
        final_y = p[1] + move_y
        
        if final_x < 0:
            final_x = final_x + bounds[0]
        elif final_x >= bounds[0]:
            final_x = final_x - bounds[0]

        if final_y < 0:
            final_y = final_y + bounds[1]
        elif final_y >= bounds[1]:
            final_y = final_y - bounds[1]

        final = (final_x, final_y)
        
        count = positions.get(final, 0)
        count = count + 1
        positions[final] = count
    return positions

def part_one(robots: List[Robot], moves=100, bounds=(11, 7)):
    positions = get_after_moves(robots, moves, bounds)
    
    q1, q2, q3, q4 = count_quadrants(positions, bounds)
    print(sum(q1.values()) * sum(q2.values()) * sum(q3.values()) * sum(q4.values()))


def part_two(robots: List[Robot], bounds):
    quarter_bounds = (int(bounds[0] / 2), int(bounds[1] / 2))
    print(quarter_bounds)
    found_tree = False
    min_max = len(robots)
    moves = 0
    while not found_tree:
        moves = moves + 1
        positions = get_after_moves(robots, moves, bounds)
        q1, q2, q3, q4 = count_quadrants(positions, bounds)

        q1_lines = ext_pos_to_string(q1, 0, int(bounds[0] / 2), 0, int(bounds[1] / 2))
        q2_lines = ext_pos_to_string(q2, ceil(bounds[0] / 2), bounds[0], 0, int(bounds[1] / 2))
        q3_lines = ext_pos_to_string(q3, 0, int(bounds[0] / 2), ceil(bounds[1] / 2), bounds[1])
        q4_lines = ext_pos_to_string(q4, ceil(bounds[0] / 2), bounds[0], ceil(bounds[1] / 2), bounds[1])

        # if sum(q1.values()) == sum(q2.values()) and sum(q3.values()) == sum(q4.values()):
        # if len(q1) == len(q2) and len(q3) == len(q4):
        # largest = max(positions.values())
        if len(q2) + len(q4) > 400:
            print_positions(positions, bounds)
            print(f"======= {moves} =========")
        # if len(positions) < 60:
        #     print_positions(positions, bounds)
        #     print(f"======== {moves} ========")
        #     all_good = True
        #     for i, l in enumerate(q1_lines):
        #         if not "".join(reversed(list(l))) == q2_lines[i]:
        #             all_good = False
        #             break
            
        #     if not all_good:
        #         continue
                
        #     for i, l in enumerate(q3_lines):
        #         if not "".join(reversed(list(l))) == q4_lines[i]:
        #             all_good = False
        #             break
            
        #     if all_good:
        #         print_positions(positions, bounds)
        #         found_tree = True


    print(moves)


if __name__ == "__main__":
    robots = read_file("input.txt")
    part_one(robots, moves=100, bounds=(101, 103))
    print("========")
    part_two(robots, bounds=(101, 103))