
directions = ['<', '^', '>', 'v']
vectors = [(-1,0), (0, -1), (1, 0), (0, 1)]

def read_file(path):
    map = dict()
    starting_position = None
    starting_direction = None
    bounds = None
    with open(path) as file:
        lines = [x.strip() for x in file.readlines()]
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c.lower() in ['>', '<', '^', 'v']:                    
                    starting_position = (x,y)
                    starting_direction = vectors[directions.index(c.lower())]
                    map[(x,y)] = "."
                else:
                    map[(x,y)] = c
        bounds = (len(lines[0]), len(lines))
    return map, starting_position, starting_direction, bounds

def rotate(direction):
    rotated_index = vectors.index(direction) + 1 if vectors.index(direction) + 1 < len(vectors) else 0
    return vectors[rotated_index]

def resolve(position, direction):
    return (position[0] + direction[0], position[1] + direction[1])

def walk(view, starting_position, starting_direction, bounds):
    hits = {}
    direction = starting_direction
    position = starting_position
    target_position = resolve(position, direction)
    while(target_position[0] >= 0 and target_position[0] < bounds[0] and target_position[1] >= 0 and target_position[1] < bounds[1]):
        seen_directions = hits.get(position, [])
        if direction in hits.get(position, []):
            return hits, True

        seen_directions = hits.get(position, [])
        seen_directions.append(direction)
        hits[position] = seen_directions

        if view[target_position] == '.':
            position = target_position
        elif view[target_position] == '#':
            direction = rotate(direction)
        
        target_position = resolve(position, direction)
            
    seen_directions = hits.get(position, [])
    seen_directions.append(direction)
    hits[position] = seen_directions
    return hits, False

def part_one(view, starting_position, starting_direction, bounds):
    hits, looped = walk(view, starting_position, starting_direction, bounds)
    print(len(hits), f"Looped - {looped}")

def part_two(view, starting_position, starting_direction, bounds):
    blocks = set()
    hits, _ = walk(view, starting_position, starting_direction, bounds)

    for pos in hits.keys():
        if not pos == starting_position:
            test = {**view}
            test[pos] = '#'
            _, looped = walk(test, starting_position, starting_direction, bounds)
            if looped:
                blocks.add(pos)
    print(len(blocks))


if __name__ == "__main__":
    view, starting_position, starting_direction, bounds = read_file("input.txt")
    part_one(view, starting_position, starting_direction, bounds)
    print("=====")
    part_two(view, starting_position, starting_direction, bounds)

