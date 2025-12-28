from benchmark import benchmark
from datetime import datetime

small = benchmark(prompt="Hello!")
medium = benchmark(prompt="Explain transformers in detail.")
large = benchmark(prompt="Write a 2000 word essay on the history of AI.")

with open("BENCHMARK.md", "w") as f:
    f.write(f"# LLM Benchmark Report\n")
    f.write(f"Generated: {datetime.now()}\n\n")

    for size, result in [("Small", small), ("Medium", medium), ("Large", large)]:
        f.write(f"## {size} Prompt\n")
        for k, v in result.items():
            f.write(f"- **{k}**: {v}\n")
        f.write("\n")
