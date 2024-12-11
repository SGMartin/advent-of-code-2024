# I noticed a counter could work here but I already solved the problem.
# Let's refresh counters nevertheless
from collections import Counter

with open("puzzle_input.txt", "r") as fil:
    stones = [int(stone) for stone in fil.readline().split()]


def count_stones(stones, blinks):
    # Initialize counts using Counter
    stones = Counter(stones)

    for blink in range(blinks):
        new_stones = Counter()
        for stone_number, n_appearances in stones.items():
            if stone_number == 0:
                # Don't worry about keys, counters work around this
                new_stones[1] += n_appearances
            elif len(str(stone_number)) % 2 == 0:
                # Split stone into two
                stone_value = str(stone_number)
                stone_1, stone_2 = int(stone_value[:len(stone_value)//2]), int(stone_value[len(stone_value)//2:])
                new_stones[stone_1] += n_appearances
                new_stones[stone_2] += n_appearances
            else:
                new_stone_value = stone_number * 2024
                new_stones[new_stone_value] += n_appearances

        stones = new_stones

    return sum(stones.values())

blinks = 25
print(f"Part 1 answer is {count_stones(stones, blinks)} stones after {blinks} blinks")
blinks = 75
print(f"Part 2 answer is {count_stones(stones, blinks)} stones after {blinks} blinks")
