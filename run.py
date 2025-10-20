import sys
import heapq
from typing import List, Tuple

# Энергозатраты для каждого типа амфипода
MOVE_COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

# Индексы дверей комнат в коридоре
ROOM_DOORS = (2, 4, 6, 8)

# Разрешённые позиции для остановки в коридоре
HALL_STOP_POSITIONS = (0, 1, 3, 5, 7, 9, 10)

# Разбирает входные строки в структуру данных:
def parse_labyrinth(lines: List[str]) -> Tuple[Tuple[str, ...], Tuple[Tuple[str, ...], ...]]:
    if len(lines) < 5:
        raise ValueError("Некорректный формат входных данных")

    depth = len(lines) - 3

    hallway = tuple(lines[1][1 + i] for i in range(11))

    # Комнаты: берём символы с позиций 3,5,7,9 из строк ниже
    rooms = []
    for room_index in range(4):
        col = 3 + room_index * 2
        cells = [lines[2 + i][col] for i in range(depth)]
        rooms.append(tuple(cells))

    return hallway, tuple(rooms)

# Проверяет, достигнута ли целевая конфигурация
def is_goal_state(hallway: Tuple[str, ...], rooms: Tuple[Tuple[str, ...], ...]) -> bool:
    if any(ch != '.' for ch in hallway):
        return False
    for i, room in enumerate(rooms):
        target = chr(ord('A') + i)
        if any(c != target for c in room):
            return False
    return True

# Возвращает все возможные ходы из текущего состояния
def get_possible_moves(state: Tuple[Tuple[str, ...], Tuple[Tuple[str, ...], ...]]):
    hallway, rooms = state
    depth = len(rooms[0])

    # Движение из коридора в комнату
    for hall_pos, pod in enumerate(hallway):
        if pod == '.':
            continue

        target_room_idx = ord(pod) - ord('A')
        target_room = rooms[target_room_idx]

        # Можно войти только если нет чужих типов
        if any(ch not in ('.', pod) for ch in target_room):
            continue

        # Проверяем, есть ли свободное самое глубокое место
        for room_pos in range(depth - 1, -1, -1):
            if target_room[room_pos] == '.':
                break
        else:
            continue

        door_pos = ROOM_DOORS[target_room_idx]
        # Проверка, свободен ли путь
        start, end = sorted((hall_pos, door_pos))
        if any(hallway[i] != '.' for i in range(start + 1, end)):  # <-- исправлено здесь
            continue

        steps = abs(hall_pos - door_pos) + (room_pos + 1)
        cost = steps * MOVE_COST[pod]

        new_hallway = list(hallway)
        new_hallway[hall_pos] = '.'
        new_rooms = [list(r) for r in rooms]
        new_rooms[target_room_idx][room_pos] = pod

        yield (tuple(new_hallway), tuple(tuple(r) for r in new_rooms)), cost

    # Движение из комнаты в коридор
    for room_idx, room in enumerate(rooms):
        # Найдём верхнего амфипода
        for depth_pos, pod in enumerate(room):
            if pod != '.':
                break
        else:
            continue

        target_letter = chr(ord('A') + room_idx)

        # Если гость в своей комнате и под ним все свои — остаётся
        if pod == target_letter and all(r == target_letter for r in room[depth_pos:]):
            continue

        door_pos = ROOM_DOORS[room_idx]

        # Все позиции для остановки
        for stop_pos in HALL_STOP_POSITIONS:
            if hallway[stop_pos] != '.':
                continue

            start, end = sorted((door_pos, stop_pos))
            if any(hallway[i] != '.' for i in range(start + 1, end)):
                continue

            steps = (depth_pos + 1) + abs(stop_pos - door_pos)
            cost = steps * MOVE_COST[pod]

            new_hallway = list(hallway)
            new_hallway[stop_pos] = pod
            new_rooms = [list(r) for r in rooms]
            new_rooms[room_idx][depth_pos] = '.'

            yield (tuple(new_hallway), tuple(tuple(r) for r in new_rooms)), cost

# Решает задачу о сортировке в лабиринте
def solve_labyrinth(lines: List[str]) -> int:
    start_state = parse_labyrinth(lines)
    queue = [(0, start_state)]
    min_cost = {start_state: 0}

    while queue:
        current_cost, state = heapq.heappop(queue)

        if min_cost.get(state, float('inf')) < current_cost:
            continue

        if is_goal_state(*state):
            return current_cost

        for next_state, move_cost in get_possible_moves(state):
            total_cost = current_cost + move_cost
            if total_cost < min_cost.get(next_state, float('inf')):
                min_cost[next_state] = total_cost
                heapq.heappush(queue, (total_cost, next_state))

    return -1


def main():
    lines = [line.rstrip('\n') for line in sys.stdin if line.strip()]
    result = solve_labyrinth(lines)
    print(result)


if __name__ == "__main__":
    main()
