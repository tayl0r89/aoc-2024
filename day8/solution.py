

def read_file(path):
    view = {}
    with open(path) as file:
        lines = [list(x.strip()) for x in file.readlines()]
        for y, line in enumerate(lines):
            for x, ind in enumerate(line):
                if ind == '.':
                    continue
                items = view.get(ind,[])
                items.append((x,y))
                view[ind] = items
    return view, (len(lines[0]), len(lines))

def is_in_bounds(vector, bounds):
    return vector[0] >= 0 and vector[0] < bounds[0] and vector[1] >= 0 and vector[1] < bounds[1]

def part_one(view, bounds):
    overlaps = set()
    for _key, values in view.items():
        for i, v in enumerate(values):
            for other in values[i+1:]:
                vector = (other[0] - v[0], other[1] - v[1])
                first = (v[0] - vector[0], v[1] - vector[1])
                second = (other[0] + vector[0], other[1] + vector[1])
                if is_in_bounds(first, bounds):
                    overlaps.add(first)

                if is_in_bounds(second, bounds):
                    overlaps.add(second)  

    print(len(overlaps))

def part_two(view, bounds):
    overlaps = set()
    for key, values in view.items():
        for i, v in enumerate(values):
            overlaps.add(v)
            for other in values[i+1:]:
                vector = (other[0] - v[0], other[1] - v[1])
                first = (v[0] - vector[0], v[1] - vector[1])
                second = (other[0] + vector[0], other[1] + vector[1])

                while is_in_bounds(first, bounds):
                    overlaps.add(first)
                    first = (first[0] - vector[0], first[1] - vector[1])
                
                while is_in_bounds(second, bounds):
                    overlaps.add(second)  
                    second = (second[0] + vector[0], second[1] + vector[1])

    print(len(overlaps))

if __name__ == "__main__":
    view, bounds = read_file("input.txt")
    part_one(view, bounds)
    print("======")
    part_two(view, bounds)