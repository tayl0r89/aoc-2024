
def read_file():
    levels = []
    with open("input.txt") as file:
        for line in file.readlines():
            data = [int(x) for x in line.split(" ")]
            levels.append(data)
    
    return levels

def is_safe(levels):
    # Must be same direction of change
    # Min 1 max 3
    direction = None 
    for i in range(1, len(levels)):
        diff = levels[i - 1] - levels[i]
        temp_direction = "asc" if diff < 0 else "desc"

        if direction is None:
            direction = temp_direction

        if abs(diff) < 1 or abs(diff) > 3:
            return (False, i)
        
        if not direction == temp_direction:
            return (False, i)
        
        direction = temp_direction
    
    return (True, None)

def with_dampener(levels):
    result = is_safe(levels)
    if result[0]:
        return True
    
    if result[1] <= 2:
        print(f"Failed {levels} at {result[1]}")
        first_removed = is_safe(levels[1:])
        print(first_removed, levels[1:])
        second_removed = is_safe(levels[:1] + levels[2:])
        print(second_removed, levels[:1] + levels[2:])
        third_removed = is_safe(levels[:2] + levels[3:])
        print(second_removed, levels[:2] + levels[3:])
        return first_removed[0] or second_removed[0] or third_removed[0]
    else:
        print(f"Failed {levels} at {result[1]}")
        check = is_safe(levels[:result[1]] + levels[result[1] + 1:])
        print(check, levels[:result[1]] + levels[result[1] + 1:])
        return check[0]

def part_one():
    levels = read_file()
    return len(list(filter(lambda x: is_safe(x)[0], levels)))

def part_two():
    levels = read_file()
    return len(list(filter(with_dampener, levels)))

print(part_one())
print("====")
print(part_two())