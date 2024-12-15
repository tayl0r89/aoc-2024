
from typing import List, Tuple


Button = Tuple[int, int, int]
Prize = Tuple[int, int]
Machine = Tuple[List[Button], Prize]

def read_file(path) -> List[Machine]:
    with open(path) as file:
        machines = [
            x.strip()
            for x in file.read().split("\n\n")
        ]
        results: List[Machine] = []
        for m in machines:
            prize = None
            buttons = []
            for part in m.split("\n"):
                before, after = part.split(":")
                if before.startswith("Button"):
                    button = 3 if before[-1] == "A" else 1 
                    coords = after.split(",")
                    x = int(coords[0].strip().split("+")[1])
                    y = int(coords[1].strip().split("+")[1])
                    buttons.append((button, x, y))
                elif before.startswith("Prize"):
                    coords = after.split(",")
                    x = int(coords[0].strip().split("=")[1])
                    y = int(coords[1].strip().split("=")[1])
                    prize = (x,y)
            results.append((buttons, prize))
        return results

def smallest(button_1, button_2, prize):
    x_max = int(prize[0] / button_1[1])
    winners = []
    for i in range(1, x_max+1):
        cost = i * button_1[0]
        total = (i * button_1[1], i * button_1[2])
        remain = (prize[0] - total[0], prize[1] - total[1])
        other_x_max = int(remain[0] / button_2[1])
        for y in range(1, other_x_max + 1):
            other_cost = y * button_2[0]
            total_2 = (button_2[1] * y, button_2[2] * y)
            final = (total[0] + total_2[0], total[1] + total_2[1])
            if final[0] == prize[0] and final[1] == prize[1]:
                winners.append(cost + other_cost)
    
    if len(winners) == 0:
        # print("No winner")
        return None

    # print(winners)
    return min(winners)

def get_input(machine: Machine) -> int:
    buttons = machine[0]
    prize = machine[1]
    return smallest(buttons[0], buttons[1], prize)


def find_b(x1, y1, x2, y2, xp, yp) -> int | None:
    top = (xp * y1) - (yp * x1)
    bottom = (y1 * x2) - (y2 * x1)
    b = top / bottom
    
    if int(b) == b:
        return b
    return None

def find_a(x1, y1, x2, y2, xp, yp, b) -> int | None:
    top = (xp * y1) - (b*y1*x2)
    bottom = (x1 * y1)
    a = top / bottom
    if int(a) == a:
        return a
    return None

# def part_one(machines: List[Machine]):
#     total = 0
#     for m in machines:
#         buttons = m[0]
#         prize = m[1]
#         cost = smallest(buttons[0], buttons[1], prize)
#         if cost:
#             total = total + cost
#     print(f"Winner is {total}")

def part_one(machines: List[Machine], offset = 0):
    total = 0
    for m in machines:
        buttons = m[0]
        prize = m[1]
        x1 = buttons[0][1]
        y1 = buttons[0][2]
        x2 = buttons[1][1]
        y2 = buttons[1][2]
        xp = prize[0] + offset
        yp = prize[1] + offset

        b = find_b(x1, y1, x2, y2, xp, yp)
        if b:
            a = find_a(x1,y1, x2, y2, xp, yp, b)
            if a:
                print(f"A is {a} B is {b}")
                total = total + (a*3) + (b*1)

    print(total)


if __name__ == "__main__":
    machines = read_file("input.txt")
    part_one(machines)
    print("=====")
    part_one(machines, offset=10000000000000)