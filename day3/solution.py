import re

def read_file():
    with open("input.txt") as file:
        content = file.read()

    return content

PATTERN = r'mul\(\d{1,3},\d{1,3}\)'

def part_one(input):
    results = re.findall(PATTERN, input)
    return sum(map(execute, results))

PATTERN_TWO = r'mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)'

def part_two(input):
    results = re.findall(PATTERN_TWO, input)
    should_count = True
    count = 0
    for match in results:
        if match == "don't()":
            should_count = False
        elif match == "do()":
            should_count = True
        elif should_count:
            count = count + execute(match)
    return count

def execute(mul_string: str):
    data = mul_string.replace("mul(", "").replace(")", "").split(",")
    return int(data[0]) * int(data[1])

content = read_file()
print(part_one(content))
print("=========")
print(part_two(content))