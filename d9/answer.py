import re

with open("puzzle_input.txt", "r") as fil:
    hard_drive = re.findall("\d", fil.read())
    hard_drive = [int(x) for x in hard_drive]


def compress_disk(hdd):
    extended_disk = []
    # extend disk so that empty space equals -1
    for i, n in enumerate(hdd):
        extended_disk += [-1] * n if i % 2 else [i // 2] * n

    # get the ids of the free disk blocks
    free_blocks = [i for i, n in enumerate(extended_disk) if n == -1]
    for i in free_blocks:
        # Start removing empty space from the end of the disk until a new
        # disk block is found
        while extended_disk[-1] == -1:
            extended_disk.pop()
        # End of the disk
        if len(extended_disk) <= i:
            break

        # Get the last block and append it to the first empty block
        # them pop it out of the disk
        extended_disk[i] = extended_disk.pop()

    return sum(id * i for i, id in enumerate(extended_disk))


def defrag_disk(hdd):
    files = dict() 
    free_spaces = [] # (start, blocks)

    disk_position = 0
    for i, n in enumerate(hdd):
        if i % 2:
            free_spaces.append((disk_position, n))
        else:
            files[i // 2] = (disk_position, n) # {file_id:(start, blocks)}

        disk_position += n

    for file_id, (file_pos, file_size) in reversed(files.items()):
        for i, (space_pos, space_size) in enumerate(free_spaces):

            # Does not fit, try next block of empty sizes
            if file_size > space_size:
                continue

            # We cannot move files to the right, stop now
            if space_pos >= file_pos:
                break

            # Update the positions
            files[file_id] = (space_pos, file_size)
            # Fill the space blocks
            new_space_size = space_size - file_size

            # Remove the free space
            if new_space_size == 0:
                free_spaces.pop(i)
            else:
                # Move remaining free size to the right
                free_spaces[i] = (space_pos + file_size, new_space_size)

            break

    return sum(file_id * (2*p+l-1)*l//2 for file_id, (p, l) in files.items())


print(f"Part 1 answer is {compress_disk(hard_drive)}")
print(f"Part 2 answer is {defrag_disk(hard_drive)}")
