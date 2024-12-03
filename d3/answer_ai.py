import re


def get_total_sum(operations: list) -> int:
    """
    Calculate the total sum of the product of pairs in the given list of operations.

    Args:
    operations (list): A list of tuples, where each tuple contains two numbers (as strings).

    Returns:
    int: The total sum of the products.
    """
    return sum(int(a) * int(b) for a, b in operations)


# Load puzzle input
with open("puzzle_input.txt", "r") as file:
    raw_data = file.read()

# Define regex patterns
mul_pattern = r"mul\((\d+),(\d+)\)"
do_pattern = r"do\(\)"
dont_pattern = r"don't\(\)"

# Find all "mul" operations in the entire input
valid_operations = re.findall(mul_pattern, raw_data)

# Part 1: Calculate the total sum of all mul operations
part1_answer = get_total_sum(valid_operations)
print(f"Part 1 answer is {part1_answer}")

# Part 2: Process segments based on "do()" and "don't()" markers
do_segments = re.split(dont_pattern, raw_data)

# Collect valid operations based on segments between "do()" and "don't()"
valid_operations_part2 = []

for segid, segment in enumerate(do_segments):
    # If the segment contains a "do()", start from that point onward
    if re.search(do_pattern, segment):
        start_pos = segment.index("do()") + len("do()")
        valid_operations_part2 += re.findall(mul_pattern, segment[start_pos:])
    # For the first segment, we just add all valid operations (no "do()" yet)
    elif segid == 0:
        valid_operations_part2 += re.findall(mul_pattern, segment)

# Part 2: Calculate the total sum of mul operations based on the segmented rules
part2_answer = get_total_sum(valid_operations_part2)
print(f"Part 2 answer is {part2_answer}")