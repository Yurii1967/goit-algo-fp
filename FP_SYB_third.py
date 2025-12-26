# Реалізація алгоритму Дейкстри для зваженого графа з використанням бінарноїь купи heapq
import heapq
from math import inf


def dijkstra(graph: dict, start):
    """
    graph: dict[vertex] -> list[(neighbor, weight)]
    start: стартова вершина

    Повертає:
      dist: dict[vertex] -> найкоротша відстань від start
      prev: dict[vertex] -> попередник у найкоротшому шляху (для відновлення маршруту)
    """
    dist = {v: inf for v in graph}
    prev = {v: None for v in graph}

    dist[start] = 0
    heap = [(0, start)]  # (distance, vertex)

    while heap:
        current_dist, u = heapq.heappop(heap)

        # Якщо це "застарілий" запис у купі — пропускаємо
        if current_dist != dist[u]:
            continue

        for v, w in graph[u]:
            if w < 0:
                raise ValueError("Алгоритм Дейкстри не працює з від'ємними вагами ребер.")

            new_dist = current_dist + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, prev


def reconstruct_path(prev: dict, start, target):
    """Відновлює шлях start -> target за масивом prev. Повертає список вершин."""
    if start == target:
        return [start]

    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    if path and path[0] == start:
        return path
    return []  # якщо target недосяжна


if __name__ == "__main__":
    # 1) Створюємо зважений граф (список суміжності)
    # Формат: вершина: [(сусід, вага), ...]
    graph = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("C", 1), ("D", 5)],
        "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
        "D": [("B", 5), ("C", 8), ("E", 2), ("F", 6)],
        "E": [("C", 10), ("D", 2), ("F", 3)],
        "F": [("D", 6), ("E", 3)],
    }

    start_vertex = "A"

    # 2) Обчислюємо найкоротші шляхи від стартової вершини
    dist, prev = dijkstra(graph, start_vertex)

    # 3) Виводимо результати
    print(f"Найкоротші відстані від {start_vertex}:")
    for v in sorted(dist):
        if dist[v] == inf:
            print(f"  {start_vertex} -> {v}: недосяжно")
        else:
            print(f"  {start_vertex} -> {v}: {dist[v]}")

    # 4) (Опційно) демонстрація відновлення маршруту
    target = "F"
    path = reconstruct_path(prev, start_vertex, target)
    if path:
        print(f"\nШлях {start_vertex} -> {target}: {' -> '.join(path)} (довжина = {dist[target]})")
    else:
        print(f"\nШлях {start_vertex} -> {target}: недосяжно")
