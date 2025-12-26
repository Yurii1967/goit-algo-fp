# Візуалізація обходу бінарного дерева без рекурсії
import uuid
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="#1a1a1a"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """Додає вузли/ребра в граф + координати для малювання."""
    if node is None:
        return

    graph.add_node(node.id, color=node.color, label=str(node.val))

    if node.left:
        graph.add_edge(node.id, node.left.id)
        l = x - 1 / (2 ** layer)
        pos[node.left.id] = (l, y - 1)
        add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)

    if node.right:
        graph.add_edge(node.id, node.right.id)
        r = x + 1 / (2 ** layer)
        pos[node.right.id] = (r, y - 1)
        add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)


def draw_tree(root, title="Binary Tree"):
    """Малює дерево з поточними кольорами вузлів."""
    graph = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(graph, root, pos)

    colors = [graph.nodes[n]["color"] for n in graph.nodes]
    labels = {n: graph.nodes[n]["label"] for n in graph.nodes}

    plt.figure(figsize=(10, 6))
    plt.title(title)
    nx.draw(
        graph,
        pos,
        labels=labels,
        node_color=colors,
        node_size=1800,
        arrows=False,
        font_size=12
    )
    plt.show()


def iter_nodes_preorder(root):
    """Повертає список вузлів у порядку (preorder) без рекурсії: root-left-right."""
    if root is None:
        return []
    out = []
    stack = [root]
    while stack:
        node = stack.pop()
        out.append(node)
        # важливо: правий штовхаємо першим, щоб лівий обробився раніше
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out


def iter_nodes_levelorder(root):
    """Повертає список вузлів у порядку BFS без рекурсії."""
    if root is None:
        return []
    out = []
    q = deque([root])
    while q:
        node = q.popleft()
        out.append(node)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return out


def gradient_hex_colors(n, start=(20, 20, 20), end=(200, 230, 255)):
    """
    Генерує n кольорів HEX #RRGGBB від темного (start) до світлого (end).
    """
    if n <= 0:
        return []
    if n == 1:
        r, g, b = start
        return [f"#{r:02X}{g:02X}{b:02X}"]

    colors = []
    for i in range(n):
        t = i / (n - 1)
        r = round(start[0] + (end[0] - start[0]) * t)
        g = round(start[1] + (end[1] - start[1]) * t)
        b = round(start[2] + (end[2] - start[2]) * t)
        colors.append(f"#{r:02X}{g:02X}{b:02X}")
    return colors


def reset_colors(root, base="#1a1a1a"):
    """Скинути всі кольори вузлів до базового."""
    for node in iter_nodes_levelorder(root):
        node.color = base


def visualize_traversal_steps(root, order_nodes, traversal_name="Traversal"):
    """
    Візуалізує кожен крок обходу.
    Кожен відвіданий вузол отримує унікальний колір з градієнту.
    """
    reset_colors(root, base="#1a1a1a")

    colors = gradient_hex_colors(len(order_nodes))
    for step, (node, c) in enumerate(zip(order_nodes, colors), start=1):
        node.color = c
        draw_tree(root, title=f"{traversal_name}: крок {step} (відвідано: {node.val})")


# ---------- Приклад дерева ----------
#        10
#      /    \
#     5      15
#    / \    /  \
#   2   7  12  20

if __name__ == "__main__":
    root = Node(10)
    root.left = Node(5)
    root.right = Node(15)
    root.left.left = Node(2)
    root.left.right = Node(7)
    root.right.left = Node(12)
    root.right.right = Node(20)

    # DFS (у глибину) — стек, без рекурсії
    dfs_nodes = iter_nodes_preorder(root)
    visualize_traversal_steps(root, dfs_nodes, traversal_name="DFS (глибина, стек)")

    # BFS (у ширину) — черга, без рекурсії
    bfs_nodes = iter_nodes_levelorder(root)
    visualize_traversal_steps(root, bfs_nodes, traversal_name="BFS (ширина, черга)")
