import math
import re

with open("puzzle_input.txt", "r") as fil:
    tests = [t.rstrip() for t in fil.readlines()]

tests = [
    [
        int(n) for n in re.findall(r"\d+", test)]
        for
        test in tests
    ]


def concat(num_list):
    num_strs = [str(n) for n in num_list]
    return int("".join(num_strs))

def is_valid_test(test: list, from_operator: int = 0, current_result: int = None, part_two: bool = False):

    test_target = test[0]
    nums = test[1:]

    max_operators = len(nums) - 1
    current_operator = from_operator

    # last operator was on prev. loop. Won't overflow don't worry
    if current_operator == max_operators:
        return current_result == test_target


    if current_result is None:
        current_result = nums[0]

    y = nums[current_operator + 1]

    if current_result > test_target:
        return False

    # Addition
    if is_valid_test(test, from_operator=current_operator + 1, current_result=current_result + y, part_two=part_two):
        return True

    # Multiplication
    if is_valid_test(test, from_operator=current_operator + 1, current_result=current_result * y, part_two=part_two):
        return True

    # If part2 problem
    if part_two:
        concat_result = concat([current_result, y])
        if concat_result > test_target:
            return False

        if is_valid_test(test, from_operator=current_operator + 1, current_result=concat_result, part_two=part_two):
            return True

    return False



part1_sum = 0
for test in tests:
    if is_valid_test(test):
        part1_sum += test[0]


print(f"Part 1 answer is {part1_sum}")

part2_sum = 0
for test in tests:
    if is_valid_test(test, part_two=True):
        part2_sum += test[0]

print(f"Part 2 answer is {part2_sum}")
