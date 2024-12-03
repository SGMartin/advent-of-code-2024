import re


def get_total_sum(mults: list) -> int:
    total_sum = 0

    for operation in mults:
        result = int(operation[0]) * int(operation[1])
        total_sum += result

    return total_sum


with open("puzzle_input.txt", "r") as fil:
    raw_set = fil.readlines()

# Combine all lines into a single string
raw_set = "".join(raw_set)

mul_pattern = r"mul\((\d+),(\d+)\)"
do_pattern = r"do\(\)"
dont_pattern = r"don't\(\)"

valid_operations = re.findall(pattern=mul_pattern, string=raw_set)

print(f"Part 1 answer is {get_total_sum(valid_operations)}")

# Now match with start of from do() until don't()
# Segment string based on don't pattern
do_segments = re.split(pattern=dont_pattern, string=raw_set)

valid_operations = []
for segid, segment in enumerate(do_segments):
    # Segment starting from don't but with a do inside:
    if re.search(pattern=do_pattern, string=segment):

        # Find the index of "do()" and add the full length of "do"
        start_pos = segment.index("do()") + len("do()")
        valid_operations += re.findall(pattern=mul_pattern, string=segment[start_pos:])
    # must be the first segment since no do's and splitted by don't
    # beware of empty don't() / don't() segments withouts any do! Only the first one
    # is do! by default
    else:
        if segid == 0:
            valid_operations += re.findall(pattern=mul_pattern, string=segment)

print(f"Part 2 answer is {get_total_sum(valid_operations)}")