from typing import List

def read_file(path):
    with open(path) as file:
        return [list(x.strip()) for x in file.readlines()]
    

def find(wordsearch: List[List[str]], query: List[str], position, direction):
    if len(query) == 0:
        raise ValueError("SHouldnt get here")
    
    target_letter = query.pop(0)
    target_x = position[0]
    target_y = position[1]
    wordsearch_letter = None

    if target_x < 0 or target_y < 0:
        return False

    try:
        wordsearch_letter = wordsearch[target_y][target_x]
    except:
        return False

    if wordsearch_letter == target_letter:
        if len(query) == 0:
            return True
        else:
            next_x = position[0] + direction[0]
            next_y = position[1] + direction[1]
            return find(wordsearch, query, (next_x, next_y), direction)

    return False
    
def part_one(wordsearch):
    rot = list(zip(*wordsearch[::-1]))
    rot2 = list(zip(*rot[::-1]))
    rot3 = list(zip(*rot2[::-1]))
    print(find_xmas(wordsearch) + find_xmas(rot) + find_xmas(rot2) + find_xmas(rot3))

def find_xmas(wordsearch):
    total_count = 0
    for y, line in enumerate(wordsearch):
        for x, _letter in enumerate(line):
            count = 0
            if find(wordsearch, ['X', 'M', 'A', 'S'], (x,y), (1,0)):
                count = count + 1
            if find(wordsearch, ['X', 'M', 'A', 'S'], (x,y), (1,1)):
                count = count + 1

            total_count += count
    return total_count

def part_two(wordsearch):
    total_count = 0
    for y, line in enumerate(wordsearch):
        for x, letter in enumerate(line):
            if letter == 'A' and x < len(line) - 1 and y < len(wordsearch) - 1 and x > 0 and y > 0:
                if (wordsearch[y - 1][x - 1] == 'M' and wordsearch[y + 1][x + 1] == 'S') or (wordsearch[y - 1][x - 1] == 'S' and wordsearch[y + 1][x + 1] == 'M'):
                    if(wordsearch[y + 1][x - 1] == 'M' and wordsearch[y - 1][x + 1] == 'S') or (wordsearch[y + 1][x - 1] == 'S' and wordsearch[y - 1][x + 1] == 'M'):
                        total_count = total_count + 1

    print(total_count)

if __name__ == "__main__":
    wordsearch = read_file("input.txt")
    part_one(wordsearch)
    print("============")
    part_two(wordsearch)
