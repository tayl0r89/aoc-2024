

from typing import List

operators = ['+', '*', '||']

def read_file(path):
    with open(path) as file:
        lines = [x.strip() for x in file.readlines()]
        inputs = [(
            int(x.split(":")[0]), 
            list(map(int, x.split(":")[1].strip().split(" ")))
        ) for x in lines] 
        return inputs


def is_valid(target: int, values: List[int], concat_enabled=False) -> bool:
    if len(values) == 0:
        raise ValueError("Bad input")

    next = values[0]
    remaining = values[1:]
    # No negatives in the input so this prune is valid
    if next > target:
        return False

    if len(remaining) == 0:
        return next == target
        

    valid = False
    for operator in operators:
        match operator:
            case '+': valid = is_valid(target, [next + remaining[0], *remaining[1:]], concat_enabled=concat_enabled)
            case '*': valid = is_valid(target, [next * remaining[0], *remaining[1:]], concat_enabled=concat_enabled)
            case '||': 
                concat_value = int(str(next) + str(remaining[0]))
                valid = is_valid(target, [concat_value, *remaining[1:]], concat_enabled=concat_enabled) if concat_enabled else False
        if valid:
            return True     
            
    return False

def part_one(inputs):
    total = 0
    for input in inputs:
        target = input[0]
        values = input[1]
        if is_valid(target, values):
            total = total + target

    print(total)

def part_two(inputs): 
    total = 0
    for input in inputs:
        target = input[0]
        values = input[1]
        if is_valid(target, values, concat_enabled=True):
            total = total + target

    print(total)

if __name__ == "__main__":
    inputs = read_file("input.txt")#
    part_one(inputs)
    print("=====")
    part_two(inputs)
    # print(is_valid(7290, [486, 15], concat_enabled=True))