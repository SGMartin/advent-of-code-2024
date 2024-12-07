import itertools
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


def is_valid_test(test: list) -> bool:

    is_valid_test = False

    res = test[0]
    nums_to_operate = test[1:]
    required_operators = len(nums_to_operate) - 1

    # # These cannot be changed
    # fixed_operators = dict.fromkeys(range(required_operators))

    # # quick and dirty checks
    # # All add to prod
    # if math.prod(nums_to_operate) == res:
    #     is_valid_test = True

    # # All add to res
    # elif sum(nums_to_operate) == res:
    #     is_valid_test = True

    # # If a full product does not reach res, it won't be valid ever
    # elif math.prod(nums_to_operate) < res:
    #     is_valid_test = False

    # # Here there be dragons
    # else:
        # # Find the fixed operators first
        # # since only sum and prod are allowed,
        # # left num is always num or greater

        # for i in range(required_operators):
        #     x = nums_to_operate[i]
        #     y = nums_to_operate[i + 1]

        #     if x * y > res:
        #         fixed_operators[i] = sum

        # # Check if fixing the operators already satisfied the test
        # found_fixed_operators = [val for val in fixed_operators.values() if val]

        # if len(found_fixed_operators) == required_operators:
        #     if calculate(nums=nums_to_operate, operators=fixed_operators) == res:
        #         is_valid_test = True
        #     else:
        #         is_valid_test = False

        # Brute force the remaining operators
        # else:
            # remaining_operator_indices = [i for i, val in fixed_operators.items() if val is None]
            # remaining_combinations = itertools.product([sum, math.prod], repeat=len(remaining_operator_indices))

            # for combination in remaining_combinations:
            #     current_operators = fixed_operators.copy()
            #     for idx, operator in zip(remaining_operator_indices, combination):
            #         current_operators[idx] = operator

            #     if calculate(nums=nums_to_operate, operators=current_operators) == res:
            #         is_valid_test = True
            #         break

    print("Brute force combinations for remaining operators...")
    # Generate all combinations of sum and prod for the required number of operators
    combinations = itertools.product([sum, math.prod], repeat=required_operators)

    all_combinations = []

    for combination in combinations:
        # Create a dictionary with keys as the operator positions and values as the operator
        operators_dict = dict(zip(range(required_operators), combination))
        all_combinations.append(operators_dict)

    for combination in all_combinations:
        if calculate(nums=nums_to_operate, operators=combination) == res:
            is_valid_test = True

    return is_valid_test


def calculate(nums, operators):
    res = 0
    for k, op in operators.items():
        if k == 0:
            res += op(nums[k:k+2])
        else:
            res = op([res, nums[k + 1]])
    return res


part_1_sum = 0
for test in tests:
    if is_valid_test(test=test):
        print(test[0])
        part_1_sum += test[0]

print(f"Part 1 answer is {part_1_sum}")

# I refuse to do part 2 this way, I'm gonna die