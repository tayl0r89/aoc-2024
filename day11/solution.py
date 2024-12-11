

def read_file(path):
    with open(path) as file:
        return [list(map(int, x.strip().split(" "))) for x in file.readlines()]

def blink(item):
    if item == 0:
        return [1]
    
    digits = len(str(item))
    if digits % 2 == 0:
        half = int(digits / 2)
        return [int(str(item)[:half]), int(str(item)[half:])]
    
    return [item * 2024]

cache = {}

def blink_n(item, times=25) -> int:
    hit = cache.get((item, times))
    if hit:
        return hit
    
    if times == 1:
        return len(blink(item))
    
    blinked = blink(item)
    all = [*[blink_n(x, times=times-1) for x in blinked]]
    total = sum(all)

    cache[(item, times)] = total

    return total


def process(items, times=25):
    count = 0
    for val in items:
        stones = blink_n(val, times)
        count = count + stones

    print(count)


if __name__ == "__main__":
    input = read_file("input.txt")
    process(input[0], times=25)
    print("=============")
    process(input[0], times=75)