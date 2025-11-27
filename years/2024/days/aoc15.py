fmt_dict = { "sep": "\n\n" }


UP, RIGHT, DOWN, LEFT = -1, 1j, 1, -1j

def step(walls, boxes, robot, direction):
    next_robot = robot + direction
    if next_robot in walls:
        return boxes, robot
    if next_robot not in boxes:
        return boxes, next_robot
    # try pushing boxes
    end = next_robot
    while end in boxes:
        end += direction
    if end in walls:
        return boxes, robot
    return (boxes - { next_robot }) | { end }, next_robot

def step2(walls, boxes, robot, direction):
    next_robot = robot + direction
    if next_robot in walls:
        return boxes, robot
    if next_robot not in boxes and next_robot + LEFT not in boxes:
        return boxes, next_robot
    # try pushing boxes
    box_lefts_to_move = set()
    if next_robot not in boxes:
        box_lefts_to_move.add(next_robot + LEFT)
    else:
        box_lefts_to_move.add(next_robot)
    q = [box_lefts_to_move]
    while q:
        curr_lefts = q.pop()
        next_lefts = set()
        for box_left in curr_lefts:
            next_left = box_left + direction
            if next_left in walls or next_left + RIGHT in walls:
                return boxes, robot
            for pos in next_left, next_left + LEFT, next_left + RIGHT:
                if pos in boxes:
                    next_lefts.add(pos)
        if not next_lefts <= box_lefts_to_move:
            box_lefts_to_move |= next_lefts
            q.append(next_lefts)
    return (boxes - box_lefts_to_move) | { box_left + direction for box_left in box_lefts_to_move }, next_robot

def parse_grid(grid):
    walls = set()
    boxes = set()
    robot = 0
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            match c:
                case "#":
                    walls.add(i + j * 1j)
                case "O" | "[":
                    boxes.add(i + j * 1j)
                case "@":
                    robot = i + j * 1j
    return walls, boxes, robot

def gps(boxes):
    return sum(int(100 * p.real + p.imag) for p in boxes)

def solve(data):
    grid, steps = data
    walls, boxes, robot = parse_grid(grid.split("\n"))
    grid = grid.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
    walls2, boxes2, robot2 = parse_grid(grid.split("\n"))
    for move in steps:
        if move == "\n":
            continue
        direction = { "^": UP, ">": RIGHT, "v": DOWN, "<": LEFT }[move]
        boxes, robot = step(walls, boxes, robot, direction)
        boxes2, robot2 = step2(walls2, boxes2, robot2, direction)
    return gps(boxes), gps(boxes2)
