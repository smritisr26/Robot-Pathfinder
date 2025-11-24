# 🤖 ROBOT PATHFINDER – Interactive + AI Hints (BFS/DFS/A*)
# -----------------------------------------------------------

import os
from collections import deque
import heapq
import time

grid = [
    ["⬜","⬜","⬛","⬜","⬜"],
    ["⬜","⬛","⬛","⬜","⬜"],
    ["⬜","⬜","⬜","⬜","⬜"],
    ["⬛","⬜","⬛","⬛","⬜"],
    ["⬜","⬜","⬜","⬜","🎯"]
]

ROWS, COLS = 5, 5

robot_x, robot_y = 0, 0
goal = (4, 4)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def display():
    clear()
    for r in range(ROWS):
        row = ""
        for c in range(COLS):
            if (r, c) == (robot_y, robot_x):
                row += "🤖 "
            else:
                row += grid[r][c] + " "
        print(row)
    print("\nControls: w/a/s/d = move | b = BFS hint | d = DFS hint | a = A* hint | q = quit\n")

def is_valid(nx, ny):
    return 0 <= nx < COLS and 0 <= ny < ROWS and grid[ny][nx] != "⬛"


# ------------------------------
# BFS (Shortest Path)
# ------------------------------
def bfs(start, end):
    q = deque([start])
    visited = {start: None}

    while q:
        y, x = q.popleft()
        if (y, x) == end:
            break

        for dy, dx in [(1,0),(-1,0),(0,1),(0,-1)]:
            ny, nx = y + dy, x + dx
            if is_valid(nx, ny) and (ny, nx) not in visited:
                visited[(ny, nx)] = (y, x)
                q.append((ny, nx))

    if end not in visited:
        return None

    # Reconstruct path
    path = []
    cur = end
    while cur:
        path.append(cur)
        cur = visited[cur]
    return path[::-1]


# ------------------------------
# DFS
# ------------------------------
def dfs(start, end):
    stack = [start]
    visited = {start: None}

    while stack:
        y, x = stack.pop()
        if (y, x) == end:
            break

        for dy, dx in [(1,0),(-1,0),(0,1),(0,-1)]:
            ny, nx = y + dy, x + dx
            if is_valid(nx, ny) and (ny, nx) not in visited:
                visited[(ny, nx)] = (y, x)
                stack.append((ny, nx))

    if end not in visited:
        return None

    # Reconstruct
    path = []
    cur = end
    while cur:
        path.append(cur)
        cur = visited[cur]
    return path[::-1]


# ------------------------------
# A* Search
# ------------------------------
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def a_star(start, end):
    pq = [(0, start)]
    visited = {start: None}
    cost = {start: 0}

    while pq:
        _, current = heapq.heappop(pq)
        if current == end:
            break

        y, x = current

        for dy, dx in [(1,0),(-1,0),(0,1),(0,-1)]:
            ny, nx = y + dy, x + dx
            if not is_valid(nx, ny):
                continue

            new_cost = cost[(y, x)] + 1

            if (ny, nx) not in cost or new_cost < cost[(ny, nx)]:
                cost[(ny, nx)] = new_cost
                visited[(ny, nx)] = (y, x)
                priority = new_cost + heuristic((ny, nx), end)
                heapq.heappush(pq, (priority, (ny, nx)))

    if end not in visited:
        return None

    # Path reconstruction
    path = []
    cur = end
    while cur:
        path.append(cur)
        cur = visited[cur]
    return path[::-1]


# -----------------------------------
# FUNCTION: Suggest the Next Move
# -----------------------------------
def next_move(path):
    if not path or len(path) < 2:
        return "No path found."
    y1, x1 = path[0]
    y2, x2 = path[1]

    if x2 > x1: return "➡️ Right"
    if x2 < x1: return "⬅️ Left"
    if y2 > y1: return "⬇️ Down"
    if y2 < y1: return "⬆️ Up"


# ------------------------------
# MAIN LOOP
# ------------------------------
display()

while True:
    move = input("Your move: ").lower()

    # Quit
    if move == "q":
        print("Game ended.")
        break

    # Movement
    if move in ("w", "a", "s", "d"):
        nx, ny = robot_x, robot_y

        if move == "w": ny -= 1
        if move == "s": ny += 1
        if move == "a": nx -= 1
        if move == "d": nx += 1

        if is_valid(nx, ny):
            robot_x, robot_y = nx, ny
        else:
            print("⛔ That is a wall!")
            time.sleep(0.6)

        display()

        if (robot_y, robot_x) == goal:
            print("🎉🤖 YOU REACHED THE GOAL!")
            break

    # AI Hints
    elif move == "b":
        path = bfs((robot_y, robot_x), goal)
        print("🤖 BFS Suggestion:",)
