from functools import cmp_to_key

def read_file(path):
    with open(path) as file:
        content = file.read()
        instructions, sequences = content.split("\n\n")
        return [list(map(int, x.split("|"))) for x in instructions.split("\n")], [list(map(int,x.split(","))) for x in sequences.split("\n")]


def is_valid(sequence, before):
    is_valid = True
    for i, value in enumerate(sequence):
        for test in sequence[:i]:
            if test in before.get(value, []):
                is_valid = False
                break
        if not is_valid:
            return False
    
    return is_valid
            

def part_one(rules, sequences):
    before = {}
    for rule in rules:
        values = before.get(rule[0], [])
        values.append(rule[1])
        before[rule[0]] = values
    
    count = 0
    for sequence in sequences:
        is_seq_valid = is_valid(sequence, before)
        
        if is_seq_valid:
            middle = int(len(sequence) / 2)
            count += sequence[middle]
    
    print(count)

def part_two(rules, sequences):
    before = {}
    for rule in rules:
        values = before.get(rule[0], [])
        values.append(rule[1])
        before[rule[0]] = values
    
    def compare(a, b):
        if b in before.get(a, []):
            return -1
        return 0 

    count = 0
    for sequence in sequences:
        is_seq_valid = is_valid(sequence, before)
        
        if not is_seq_valid:
            sorted_seq = sorted(sequence, key=cmp_to_key(compare))
            middle = int(len(sorted_seq) / 2)
            count += sorted_seq[middle]
    
    print(count) 

if __name__ == "__main__":
    rules, sequences = read_file("input.txt")
    part_one(rules, sequences)
    print("=====")
    part_two(rules, sequences)