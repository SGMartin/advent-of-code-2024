def make_diagonal(lines):
    # Collect the top-left to bottom-right diagonals starting from each column in the first row
    top_right_diagonals = [
        "".join(lines[i][j + i] for i in range(len(lines) - j))
        for j in range(len(lines))  # Start from each column in the first row
    ][::-1]  # Reverse the order to go from bottom-left to top-right

    bottom_left_diagonals = [
        "".join(lines[j + i][i] for i in range(len(lines) - j))
        for j in range(1, len(lines))  # Start from each row below the first
    ]

    # Combine the diagonals
    diagonal = top_right_diagonals + bottom_left_diagonals
    return diagonal

def is_cross_a(data, i, j):
    d1 = data[i-1][j-1] + data[i+1][j+1]  # Top-left and bottom-right diagonal
    d2 = data[i-1][j+1] + data[i+1][j-1]  # Top-right and bottom-left diagonal

    # Check two conditions:
    # a) the first diagonal forms either "MS" or "SM"
    # b) the two diagonals are either the same or reversed versions of each other
    if (d1 == "MS" or d1 == "SM") and (d1 == d2 or d1[::-1] == d2):
        return True

    return False

with open("puzzle_input.txt", "r") as fil:
    full_text = [line.strip() for line in fil.readlines()]

word = "XMAS"
# Part 1
xmas_count = 0

for line in full_text:
    # count forward, horizontal
    xmas_count += line.count(word)
    # count reversed
    reverse_line = line[::-1]
    xmas_count += reverse_line.count(word)

# Transpose the text by collecting characters column-wise
transposed_text = [
    "".join(row[x] for row in full_text)  # Create a string by taking the x-th character 
    for x in range(len(full_text[0]))    # Iterate through each column
]

# Now count vertical, forward and reverse
for line in transposed_text:
    # forward
    xmas_count += line.count(word)
    # reverse
    reverse_line = line[::-1]
    xmas_count += reverse_line.count(word)

# Now only diagonals left
diagonals_forward = make_diagonal(full_text)

for line in diagonals_forward:
    xmas_count += line.count(word)
    reverse_line = line[::-1]
    xmas_count += reverse_line.count(word)

# Backwards diagonals by giving the bottom line first
diagonals_backwards = make_diagonal(full_text[-1::-1])

for line in diagonals_backwards:
    xmas_count += line.count(word)
    reverse_line = line[::-1]
    xmas_count += reverse_line.count(word)


# PART 2 ---- an "A" always anchors the 
# M.S
# .A.
# M.S
new_xmas_count = 0

for row in range(1, len(full_text) - 1):
    # iterate over columns
    for col in range(1, len(full_text[0])-1):
        if full_text[row][col] == "A":  # Found the anchor!
            if is_cross_a(full_text, row, col):
                new_xmas_count += 1


print(f"Part 1 answer is {xmas_count}")
print(f"Part 2 answer is {new_xmas_count}")
