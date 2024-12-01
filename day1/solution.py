
def read_lists(): 
    left = []
    right = []
    with open("input.txt") as file:
        for line in file.read().split("\n"):
            data = line.split("  ")
            left.append(int(data[0]))
            right.append(int(data[1]))
    return (right, left)

def part_one():
    left, right = read_lists()
    sorted_left = sorted(left)
    sorted_right = sorted(right)

    total = 0
    for i, val in enumerate(sorted_left):
        total += abs(val - sorted_right[i])
    
    print(total)
    
def part_two():
    left, right = read_lists()
    counts = dict()
    for val in right:
        seen = counts.get(val, 0)
        counts[val] = seen + 1

    total = 0
    for val in left:
        total += val * counts.get(val, 0)
    
    print(total)

part_one()
print("====")
part_two()
