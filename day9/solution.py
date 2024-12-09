def print_store(store):
    toprint = ""
    for p in store:
        for i in range(p[1]):
            if not p[0] == None:
                toprint += str(p[0])
            else:
                toprint += "."
    return toprint

def read_file_chars(path):
    processed = []
    with open(path) as file:
        lines = [x.strip() for x in file.readlines()]
        for line in lines:
            store = []
            id = 0
            for i, c in enumerate(line):
                if i % 2 == 0:
                    for i in range(int(c)):
                        store.append(str(id))
                    id = id + 1
                elif not c == '0':
                    for i in range(int(c)):
                        store.append(".")
            processed.append(store)

    return processed

def read_file(path):
    processed = []
    with open(path) as file:
        lines = [x.strip() for x in file.readlines()]
        for line in lines:
            store = []
            id = 0
            for i, c in enumerate(line):
                # if not c == '0':
                if i % 2 == 0:
                    store.append((id, int(c)))
                    # for i in range(int(c)):
                    #     store.append(str(id))
                    id = id + 1
                elif not c == '0':
                    store.append((None, int(c)))
                    # for i in range(int(c)):
                    #     store.append(".")
            processed.append(store)

    return processed

def checksum_chars(store):
    checksum = 0
    for i, val in enumerate(store):
        if not val == ".":
            checksum = checksum + (i * int(val))
    return checksum

def checksum(store):
    total = 0
    position = 0
    for val in store:
        for i in range(val[1]):
            if not val[0] == None:
                total += position * val[0]
            position = position + 1
    return total

def part_one(stores):
    for store in stores:
        start = 0
        end = len(store) - 1
        while start != end:
            if not store[start][0] == None:
                start = start + 1
            elif store[end][0] == None:
                end = end - 1
            else:
                # print(f"Attempting to move {store[end]}, starting at {start}")
                # print(store)
                current = store[end]
                if not current[0] == None:
                    # If we have a file at the end pointer
                    # If the file length is greater than the start space
                    if current[1] > store[start][1]:
                        # print("Moving part the file")
                        available = store[start][1]
                        # print(f"Available space {available}")
                        store[start] = (current[0], available)
                        store[end] = (current[0], current[1] - available)
                    elif current[1] == store[start][1]:
                        # print("Moving the whole file into exact")
                        store[start] = (current[0], store[start][1])
                        store.pop(end)
                        end = end - 1
                    else:
                        # print("Moving whole file into larget space")
                        # Theres more space than the file is
                        space = store[start] 
                        store.pop(end)
                        store = [*store[:start], current, (None, space[1] - current[1]), *store[start + 1:]]
                else:
                    end = end - 1
                # print(store)
                        
                
        # print(print_store(store))
        print(checksum(store))

def part_one_chars(stores):
    for store in stores:
        start = 0
        print(store[:-10])
        end = len(store) - 1
        while start != end:
            if not store[start] == ".":
                start = start + 1
            else:
                current = store[end]
                if not current == ".":
                    store[start] = current
                    store[end] = "."
                end = end - 1
        print(checksum_chars(store))

def find(store, starting, size):
    for i in range(starting, len(store)):
        if store[i][0] == None and store[i][1] >= size:
            return i
    return None

def part_two(stores):
    for store in stores:
        start = 0
        end = len(store) - 1
        while start <= end:
            if not store[start][0] == None:
                start = start + 1
            elif store[end][0] == None:
                end = end - 1
            else:
                location = find(store, 0, store[end][1])
                if location == None or location > end:
                    end = end - 1
                    continue
                else:
                    space = store[location]
                    if space[1] == store[end][1]:
                        store[location] = (store[end][0], store[end][1])
                        store[end] = (None, store[end][1])
                    elif space[1] > store[end][1]:
                        file_size = store[end][1]
                        diff = space[1] - store[end][1]
                        store = [*store[:location], (store[end][0], store[end][1]), (None, diff), *store[location + 1:]]
                        end = end + 1
                        store[end] = (None, file_size)
                    
                    # Tidy up any messy space 
                    if end + 1 < len(store) and store[end + 1][0] == None and store[end] == None:
                        space_size = store.pop(end+1)[1]
                        store[end] = (None, store[end][1] + space_size)
                    if store[end][0] == None and store[end - 1][0] == None:
                        space_size = store.pop(end)[1]
                        store[end - 1] = (None, store[end - 1][1] + space_size)
                        end = end - 1
                
        # line = print_store(store)
        # print(line)
        print(checksum(store))

if __name__ == "__main__":
    stores = read_file("input.txt")    
    part_one(stores)
    print("=======")
    stores = read_file("input.txt")
    part_two(stores)