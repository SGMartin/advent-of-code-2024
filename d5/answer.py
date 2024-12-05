def is_in_order(rules: dict, pages: list) -> bool:
    # Reverse pages since we check dependencies
    reversed_pages = pages[::-1]
    for pid, page in enumerate(reversed_pages):
        # Get the list of pages that must come before the current page
        must_appear_before = rules.get(page, [])

        for next_page in must_appear_before:
            if next_page not in pages:
                continue

            # Find the position of the next page in the reversed list
            next_page_pos = reversed_pages.index(next_page)
            if next_page_pos <= pid:
                return False  # Found a page out of order

    return True


def bubble_sort_pages(rules: dict, pages: list) -> list:
    reverse_pages = pages[::-1]
    total_pages = len(reverse_pages)

    for i in range(total_pages):
        item_swap = False
        for j in range(0, total_pages - i - 1):
            first_page = reverse_pages[j]
            second_page = reverse_pages[j + 1]

            # Check if the first page must appear after the second page
            if first_page in rules and second_page in rules[first_page]:
                reverse_pages[j], reverse_pages[j + 1] = reverse_pages[j + 1], reverse_pages[j]
                item_swap = True

        if not item_swap:
            break  # If no swaps were made, we are done!

    return reverse_pages[::-1]  # Reverse back to the original order


# Read the input file and prepare the list of manuals
with open("puzzle_input.txt") as fil:
    full_text = fil.readlines()

# Separate the rules and manuals
printing_rules_raw = [entry.rstrip() for entry in full_text[0:full_text.index("\n")]]
manuals = [manual.rstrip() for manual in full_text[full_text.index("\n") + 1:]]
manuals = [[int(page) for page in manual.split(",")] for manual in manuals]

# Create a dictionary to store page dependencies
page_dependencies = {}

for rule in printing_rules_raw:
    key, value = map(int, rule.split('|'))
    # Reverse map
    page_dependencies.setdefault(value, []).append(key)

# Filter the manuals based on whether they are in the correct order
correct_manuals = [
    manual 
    for manual in manuals 
    if is_in_order(rules=page_dependencies, pages=manual)
    ]

incorrect_manuals = [
    manual
    for manual in manuals
    if not is_in_order(rules=page_dependencies, pages=manual)
    ]

# Part 1: Sum the middle items of the correct manuals
middle_items_sum = 0
for manual in correct_manuals:
    middle_items_sum += manual[len(manual) // 2]

# Part 2: Sort the incorrect manuals and sum their middle items
fixed_manuals = [bubble_sort_pages(page_dependencies, manual) for manual in incorrect_manuals]
next_middle_item_sum = 0
for manual in fixed_manuals:
    next_middle_item_sum += manual[len(manual) // 2]

# Print the results
print(f"Part 1 answer is {middle_items_sum}")
print(f"Part 2 answer is {next_middle_item_sum}")
