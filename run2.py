import sys
from collections import deque, defaultdict


def solve(edges: list[tuple[str, str]]) -> list[str]:
    # Построение графа
    graph = defaultdict(set)
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)

    # Все шлюзы 
    gateways = sorted([n for n in graph if n.isupper()])
    result = []

    # Текущее положение вируса
    virus = 'a'

    def bfs(start):
        #Возвращает расстояния и предков от start до всех узлов
        dist = {start: 0}
        parent = {}
        q = deque([start])
        while q:
            node = q.popleft()
            for neigh in sorted(graph[node]): 
                if neigh not in dist:
                    dist[neigh] = dist[node] + 1
                    parent[neigh] = node
                    q.append(neigh)
        return dist, parent

    def find_nearest_gateway(virus):
        #Находит ближайший шлюз и путь к нему
        dist, parent = bfs(virus)
        reachable = [(g, dist[g]) for g in gateways if g in dist]
        if not reachable:
            return None, None
        min_d = min(d for g, d in reachable)
        candidates = sorted([g for g, d in reachable if d == min_d])
        target = candidates[0]
        # Восстанавливаем путь
        path = [target]
        while path[-1] != virus:
            path.append(parent[path[-1]])
        path.reverse()
        return target, path

    while True:
        # Проверяем все шлюзы на прямую связь с вирусом
        direct_links = [f"{g}-{virus}" for g in gateways if virus in graph[g]]
        if direct_links:
            cut = sorted(direct_links)[0]
            g, n = cut.split('-')
            graph[g].remove(n)
            graph[n].remove(g)
            result.append(cut)
        else:
            # Ищем ближайший шлюз и путь к нему
            target, path = find_nearest_gateway(virus)
            if not path:
                break 

            if len(path) > 1:
                next_node = path[1]
            else:
                next_node = virus

            # Проверяем, можно ли разорвать прямое соединение с выбранным шлюзом
            cut_candidates = []
            for g in gateways:
                for n in graph[g]:
                    cut_candidates.append(f"{g}-{n}")

            # Ищем все корректные варианты разрыва
            valid_cuts = []
            for c in cut_candidates:
                g, n = c.split('-')
                dist, _ = bfs(virus)
                if n in dist:
                    valid_cuts.append(c)

            if not valid_cuts:
                break

            # Берём лексикографически минимальный корректный вариант
            cut = sorted(valid_cuts)[0]
            g, n = cut.split('-')
            graph[g].remove(n)
            graph[n].remove(g)
            result.append(cut)

            virus = next_node

        dist, _ = bfs(virus)
        if all(g not in dist for g in gateways):
            break

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
