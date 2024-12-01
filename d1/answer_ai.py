from collections import Counter

# Read and parse the puzzle input
with open("puzzle_input.txt", "r") as file:
    elven_data = [list(map(int, line.strip().split())) for line in file]

# Separate the numbers into two lists
first_list = sorted(item[0] for item in elven_data)
second_list = sorted(item[1] for item in elven_data)

# Part 1: Calculate total pairwise distances
total_distances = sum(abs(a - b) for a, b in zip(first_list, second_list))
print(f"Part 1 answer is {total_distances}")

# Part 2: Calculate total similarity score
second_list_counts = Counter(second_list)  # Count occurrences of each number in the second list
total_similarity_score = sum(item * second_list_counts[item] for item in first_list)
print(f"Part 2 answer is {total_similarity_score}")
