# greedy_algorithm & dinamic_programming
from typing import Dict, List, Tuple

items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}


def greedy_algorithm(items: Dict[str, Dict[str, int]], budget: int) -> Tuple[List[str], int, int]:
    """
    Жадібний алгоритм: вибір за найбільшим співвідношенням calories/cost.
    Повертає (список вибраних страв, сумарна вартість, сумарні калорії).
    """
    # Формуємо список (name, cost, calories, ratio)
    ranked = []
    for name, data in items.items():
        cost = data["cost"]
        calories = data["calories"]
        ratio = calories / cost
        ranked.append((name, cost, calories, ratio))

    # Сортуємо за ratio спадно
    ranked.sort(key=lambda x: x[3], reverse=True)

    chosen = []
    total_cost = 0
    total_calories = 0

    for name, cost, calories, _ in ranked:
        if total_cost + cost <= budget:
            chosen.append(name)
            total_cost += cost
            total_calories += calories

    return chosen, total_cost, total_calories


def dynamic_programming(items: Dict[str, Dict[str, int]], budget: int) -> Tuple[List[str], int, int]:
    """
    Динамічне програмування (0/1 knapsack):
    максимізує калорії при обмеженні бюджету.
    Повертає (список вибраних страв, сумарна вартість, сумарні калорії).
    """
    names = list(items.keys())
    costs = [items[n]["cost"] for n in names]
    calories = [items[n]["calories"] for n in names]
    n = len(names)

    # dp[i][b] = max calories using first i items with budget b
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        c = costs[i - 1]
        cal = calories[i - 1]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]  # не беремо i-й
            if c <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - c] + cal)  # беремо i-й

    # Відновлення вибору
    chosen = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            chosen.append(names[i - 1])
            b -= costs[i - 1]

    chosen.reverse()

    total_cost = sum(items[name]["cost"] for name in chosen)
    total_calories = sum(items[name]["calories"] for name in chosen)
    return chosen, total_cost, total_calories


if __name__ == "__main__":
    budget = 100

    g_items, g_cost, g_cal = greedy_algorithm(items, budget)
    d_items, d_cost, d_cal = dynamic_programming(items, budget)

    print(f"Budget = {budget}\n")

    print("Greedy algorithm:")
    print("  Chosen:", g_items)
    print("  Total cost:", g_cost)
    print("  Total calories:", g_cal)
    print()

    print("Dynamic programming (optimal):")
    print("  Chosen:", d_items)
    print("  Total cost:", d_cost)
    print("  Total calories:", d_cal)
