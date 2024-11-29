from itertools import permutations, combinations
import time
import random

def tsp_bruteforce(graph):
    n = len(graph)
    vertices = list(range(n))
    min_cost = float('inf')

    for perm in permutations(vertices[1:]):
        cost = graph[0][perm[0]]
        for i in range(len(perm) - 1):
            cost += graph[perm[i]][perm[i + 1]]
        cost += graph[perm[-1]][0]
        min_cost = min(min_cost, cost)

    return min_cost

def tsp_bellman_held_karp(graph):
    n = len(graph)
    A = [[float('inf')] * (1 << n) for _ in range(n)]
    A[0][1] = 0

    for m in range(2, n + 1):
        for subset in combinations(range(1, n), m - 1):
            subset = (0,) + subset
            mask = sum(1 << x for x in subset)
            for v in subset[1:]:
                mask_without_v = mask & ~(1 << v)
                A[v][mask] = min(
                    A[w][mask_without_v] + graph[w][v]
                    for w in subset if w != v
                )

    mask_full = (1 << n) - 1
    result = min(A[v][mask_full] + graph[v][0] for v in range(1, n))
    return result

def format_table(benchmarks, algos, results):
    num_benchmarks = len(benchmarks)
    num_algos = len(algos)

    max_benchmark_len = max(len(b) for b in benchmarks)
    max_result_lens = [max(len(str(results[i][j])) for i in range(num_benchmarks)) for j in range(num_algos)]

    max_space_between_algos_results = [max(max_result_lens[i], len(algo)) for i, algo in enumerate(algos)]
    max_space_between_benchmark_title = max(max_benchmark_len, 9)

    header = f"| Benchmark{' ' * (max_benchmark_len - 9)} |"
    for algo, max_len in zip(algos, max_space_between_algos_results):
        header += f" {algo}{' ' * (max_len - len(algo))} |"
    print(header)

    header_line = f"|{'-' * (max_space_between_benchmark_title + 2)}|"
    for max_len in max_space_between_algos_results:
        header_line += f"{'-' * (max_len + 2)}|"
    print(header_line)

    for i in range(num_benchmarks):
        benchmark = benchmarks[i]
        row = f"| {benchmark}{' ' * (max_space_between_benchmark_title - len(benchmark))} |"
        for j in range(num_algos):
            row += f" {results[i][j]}{' ' * (max_space_between_algos_results[j] - len(str(results[i][j])))} |"
        print(row)

def table_tsp(graphs):
    benchmarks = []
    bf_res = []
    bhk_res = []

    for i, graph in enumerate(graphs):
        benchmarks.append(f"Graph {i + 1} ({len(graph)} nodes)")

        start = time.time()
        tsp_bruteforce(graph)
        bf_time = time.time() - start

        start = time.time()
        tsp_bellman_held_karp(graph)
        bhk_time = time.time() - start

        bf_res.append(f"{bf_time:.6f}s")
        bhk_res.append(f"{bhk_time:.6f}s")

    format_table(
        benchmarks,
        ["Brute-force", "Held-Karp"],
        list(zip(bf_res, bhk_res))
    )

def generate_graph(n):
    return [[random.randint(1, 100) if i != j else 0 for j in range(n)] for i in range(n)]

graphs = [generate_graph(n) for n in range(2, 14)]
table_tsp(graphs)

def test():
    graph = [
        [0, 1, 3, 2],
        [1, 0, 4, 6],
        [3, 4, 0, 5],
        [2, 6, 5, 0]
    ]

    expected_res = 12
    bf_res = tsp_bruteforce(graph)
    bhk_res = tsp_bellman_held_karp(graph)

    print("\nTest:")
    print(f"Brute-force: {bf_res}")
    print(f"Held-Karp: {bhk_res}")
    print("Pass" if bf_res == bhk_res == expected_res else "Fail")

test()

# | Benchmark           | Brute-force | Held-Karp |
# |---------------------|-------------|-----------|
# | Graph 1 (2 nodes)   | 0.000023s   | 0.000035s |
# | Graph 2 (3 nodes)   | 0.000011s   | 0.000046s |
# | Graph 3 (4 nodes)   | 0.000022s   | 0.000050s |
# | Graph 4 (5 nodes)   | 0.000036s   | 0.000101s |
# | Graph 5 (6 nodes)   | 0.000172s   | 0.000199s |
# | Graph 6 (7 nodes)   | 0.001078s   | 0.000466s |
# | Graph 7 (8 nodes)   | 0.008665s   | 0.001088s |
# | Graph 8 (9 nodes)   | 0.064201s   | 0.002394s |
# | Graph 9 (10 nodes)  | 0.618548s   | 0.005590s |
# | Graph 10 (11 nodes) | 4.684051s   | 0.008064s |
# | Graph 11 (12 nodes) | 49.642148s  | 0.021423s |
# | Graph 12 (13 nodes) | 654.137872s | 0.047923s |