# read puzzle input

with open("puzzle_input.txt", "r") as fil:
    elven_lists = fil.readlines()

first_list, second_list = [], []

for line in elven_lists:
    lines = line.rstrip().split("  ")
 
    first_list.append(int(lines[0]))
    second_list.append(int(lines[1]))

# Sort the lists
first_list.sort()
second_list.sort()

# Calculate pairwise distances
total_distances = 0
for item1, item2 in zip(first_list, second_list):
    current_distance = abs(item1-item2)
    total_distances = total_distances + current_distance

print(f"Part1 answer is {total_distances}")

# similarity scores

total_similarity_score = 0
for item1 in first_list:
    appearances = second_list.count(item1)
    item_similarity = item1 * appearances
    total_similarity_score = total_similarity_score + item_similarity
    

print(f"Part 2 answer is {total_similarity_score}")
