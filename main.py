import sys


class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def print(self):
        for node in self.frontier:
            print(node.state)

    # methods: add, contains_state, isEmpty, remove
    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(state == node.state for node in self.frontier)

    def isEmpty(self):
        return len(self.frontier) == 0

    def remove(self):
        try:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        except IndexError:
            print('Frontier unable to remove due to indexError')


class QueueFrontier(StackFrontier):
    def remove(self):
        try:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        except IndexError:
            print('Frontier unable to remove due to indexError')


class GreedySearch(StackFrontier):
    def remove(self):
        try:
            self.sort()
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        except IndexError:
            print('Frontier unable to remove due to indexError')

    def sort(self):
        d = {}
        for node in self.frontier:
            score = manhattan(node.state)
            d[node.state] = score
        d = sorted(d.items(), key=lambda kv: kv[1])

        list = []
        for item in d:
            for node in self.frontier:
                if item[0] == node.state:
                    list.append(node)

        self.frontier = list
        return


class AStarSearch(GreedySearch):
    def sort(self):
        d = {}
        for node in self.frontier:
            score1 = manhattan(node.state)
            score2 = heuristic(node)
            d[node.state] = score1 + score2
        d = sorted(d.items(), key=lambda kv: kv[1])

        list = []
        for item in d:
            for node in self.frontier:
                if item[0] == node.state:
                    list.append(node)

        self.frontier = list
        return


def manhattan(state):
    """Return the manhattan distance between a cell and the goal"""
    i, j = state
    x, y = maze.goal
    return abs(i - x) + abs(j - y)


def heuristic(node):
    score = 0
    while node.parent is not None:
        score += 1
        node = node.parent
    return score


class Maze:
    def __init__(self, file):
        with open(file) as f:
            f = f.read()

        self.solution = None

        if f.count('A') != 1 or f.count('B') != 1:
            raise Exception('Maze must contain 1 start and 1 goal')

        f = f.splitlines()
        self.height = len(f)
        self.width = max(len(row) for row in f)
        self.f = f
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if f[i][j] == 'A':
                        self.start = (i, j)
                        row.append(False)
                    elif f[i][j] == 'B':
                        self.goal = (i, j)
                        row.append(False)
                    elif f[i][j] == ' ':
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

    # methods: print, neighbors, solve
    def print(self):
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if self.walls[i][j]:
                    print('█', end='')
                elif self.start == (i, j):
                    print('A', end='')
                elif self.goal == (i, j):
                    print('B', end='')
                elif self.solution is not None and (i, j) in self.solution[1]:
                    print('*', end='')
                elif self.solution is not None and (i, j) in self.explored:
                    print('\\', end='')
                else:
                    print(' ', end='')
            print()

    def neighbors(self, state):
        row, col = state
        movements = [
            ('up', (row - 1, col)),
            ('down', (row + 1, col)),
            ('left', (row, col - 1)),
            ('right', (row, col + 1))
        ]

        results = []
        for action, (r, c) in movements:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                results.append((action, (r, c)))

        return results

    def solve(self, method):
        self.num_explored = 0
        self.explored = set()

        start = Node(state=self.start, parent=None, action=None)
        frontier = method
        frontier.add(start)

        while True:
            if frontier.isEmpty():
                return False

            node = frontier.remove()
            self.num_explored += 1
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = actions, cells
                return True

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if state not in self.explored and not frontier.contains_state(state):
                    child = Node(state, parent=node, action=action)
                    frontier.add(child)


def choose_mazes(mazes):
    for i, m in enumerate(mazes):
        print(f'Maze {i + 1}: ')
        m.solution = None
        m.print()
        print()
    run = True
    while run:
        i = input('Choose a maze: ')
        try:
            i = int(i)
            run = False
        except ValueError:
            print('Type a number e.g. 3')

    return mazes[i - 1]



"""Load files"""
files = [(f'maze{i}.txt') for i in range(1, 6)]
mazes = []
for file in files:
    m = Maze(file)
    mazes.append(m)

"""Start Game"""
maze = choose_mazes(mazes)
while True:
    print('Choose a searching algorithm:')
    option = input('\t1. Depth-First Search(Stack)\n\t2. Breadth-First Search(Queue)'
                   '\n\t3. Greedy Best Search\n\t4. A* Search'
                   '\n\t5. How to play\n\t6. Play with another maze \n\t7. Quit\n')
    try:
        option = int(option)
    except ValueError:
        print('Enter a number')

    if option == 1:
        if maze.solve(StackFrontier()):
            maze.print()
            print(f'Explored: {maze.num_explored}')
        else:
            print('no solution')
    elif option == 2:
        if maze.solve(QueueFrontier()):
            maze.print()
            print(f'Explored: {maze.num_explored}')
        else:
            print('no solution')
    elif option == 3:
        if maze.solve(GreedySearch()):
            maze.print()
            print(f'Explored: {maze.num_explored}')
        else:
            print('no solution')
    elif option == 4:
        if maze.solve(AStarSearch()):
            maze.print()
            print(f'Explored: {maze.num_explored}')
        else:
            print('no solution')
    elif option == 5:
        print('How the computer show route:\n'
              '\t\'A\' is the start point\n'
              '\t\'B\' is the goal\n'
              '\t\'█\' is the wall\n'        
              '\t\'*\' is the final route\n'
              '\t\'\\\' is the explored place during the searching process.')
    elif option == 6:
        maze = choose_mazes(mazes)
    else:
        sys.exit(0)

    option = input('Press to Continue.')


