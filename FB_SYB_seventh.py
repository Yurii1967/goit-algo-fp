# Monte Carlo
import random
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt


def simulate_two_dice(n_rolls: int, seed: int = 123) -> Counter:
    """Monte Carlo simulation of rolling two fair dice n_rolls times."""
    random.seed(seed)
    counts = Counter()
    for _ in range(n_rolls):
        s = random.randint(1, 6) + random.randint(1, 6)
        counts[s] += 1
    return counts


def main():
    N = 1_000_000  # кількість симуляцій
    sim_counts = simulate_two_dice(N, seed=123)
    sim_probs = {s: sim_counts.get(s, 0) / N for s in range(2, 13)}

    # Аналітика (кількість способів отримати суму / 36)
    analytic_counts = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
    analytic_probs = {s: c / 36 for s, c in analytic_counts.items()}

    # Таблиця порівняння
    rows = []
    for s in range(2, 13):
        mc = sim_probs[s]
        an = analytic_probs[s]
        diff_pp = abs(mc - an) * 100  # різниця у відсоткових пунктах
        rows.append({
            "Sum": s,
            "MonteCarlo %": mc * 100,
            "Analytic %": an * 100,
            "Abs diff (pp)": diff_pp,
            "Counts": sim_counts.get(s, 0)
        })

    df = pd.DataFrame(rows)

    # Красивий друк у консоль
    print(df.to_string(
        index=False,
        formatters={
            "MonteCarlo %": lambda x: f"{x:8.4f}",
            "Analytic %":   lambda x: f"{x:8.4f}",
            "Abs diff (pp)":lambda x: f"{x:8.4f}",
        }
    ))

    # Графік: Monte Carlo vs Analytic
    sums = list(range(2, 13))
    mc_vals = [sim_probs[s] * 100 for s in sums]
    an_vals = [analytic_probs[s] * 100 for s in sums]

    plt.figure(figsize=(9, 4.8))
    plt.plot(sums, mc_vals, marker="o", label="Monte Carlo (%)")
    plt.plot(sums, an_vals, marker="s", label="Analytic (%)")
    plt.xticks(sums)
    plt.xlabel("Sum of two dice")
    plt.ylabel("Probability (%)")
    plt.title(f"Two dice: Monte Carlo vs Analytic (N={N:,} rolls)")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.show()

    # Графік: абсолютна похибка (в п.п.)
    absdiff = [abs(sim_probs[s] - analytic_probs[s]) * 100 for s in sums]
    plt.figure(figsize=(9, 4.2))
    plt.bar(sums, absdiff)
    plt.xticks(sums)
    plt.xlabel("Sum of two dice")
    plt.ylabel("Absolute difference (percentage points)")
    plt.title("Absolute error: Monte Carlo vs Analytic")
    plt.grid(True, axis="y", alpha=0.25)
    plt.show()


if __name__ == "__main__":
    main()
