
from typing import Dict, List, Set, Tuple

Position = Tuple[int, int]


def read_file(path) -> Tuple[Dict[Position, int], List[Position]]:
    positions: Dict[Position, int] = {}
    trailheads: Set[Position] = set()
    with open(path) as file:
        lines = [x.strip() for x in file.readlines()]
        for y, line in enumerate(lines):
            for x, pos in enumerate(line):
                positions[(x,y)] = int(pos)
                if int(pos) == 0:
                    trailheads.add((x,y))
    
    return positions, list(trailheads)

def get_moves(positions: Dict[Position, int], at: Position) -> List[Position]:
    directions = [(at[0] - 1, at[1]), (at[0] + 1, at[1]), (at[0], at[1] - 1), (at[0], at[1] + 1)]
    options = []
    height = positions.get(at)

    if height == None:
        raise ValueError("This is not possible")

    for direction in directions:
        pos = positions.get(direction)
        if pos and pos - height == 1:
            options.append(direction)
    
    return options

def find_routes(positions: Dict[Position, int], trailhead: Position, seen: Set[int]) -> List[Position]:
    seen.add(trailhead)
    height = positions.get(trailhead)
    if height == None:
        raise ValueError(f"Trailhead should be in the map {trailhead}")

    if height == 9:
        return [trailhead]

    moves = get_moves(positions, trailhead)
    if len(moves) == 0:
        return []
    
    results = []
    possible = list(filter(lambda x: not x in seen, moves))
    # print(f"Potential moves for {trailhead} at height {height} are {possible}")
    for move in possible:
        # print(f"Going to {move}")
        results = [*results, *find_routes(positions, move, seen)]
    
    return results

def part_one(positions, trailheads):
    score = 0
    for trailhead in trailheads:
        potential = set()
        results = find_routes(positions, trailhead, set())
        for x in results:
            potential.add(x)
        score = score + len(potential)
        # print(f"From {trailhead} we can reach {len(potential)}")
    print(score)

if __name__ == "__main__":
    positions, trailheads = read_file("input.txt")
    part_one(positions, trailheads)

    # print(find_routes(positions, (5,5)))
    
        