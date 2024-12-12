with open("example.txt", "r") as fil:
    garden = [row.rstrip() for row in fil.readlines()]


def count_areas_and_borders(grid):
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]  # Initialize the visited grid

    def dfs(r, c, char):
        # Initialize area size and border length
        area_size = 1
        borders = 0
        visited[r][c] = True

        # Check all 4 neighbors (up, down, left, right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:  # Inside grid bounds
                if grid[nr][nc] == char and not visited[nr][nc]:  # Same region
                    sub_area, sub_borders = dfs(nr, nc, char)
                    area_size += sub_area
                    borders += sub_borders
                elif grid[nr][nc] != char:  # Neighbor of different type
                    borders += 1
            else:  # Out of grid bounds (grid boundary)
                borders += 1

        return area_size, borders

    # Initialize counters
    areas = []
    borders = []

    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:  # New region found
                area_size, border_length = dfs(i, j, grid[i][j])
                areas.append(area_size)
                borders.append(border_length)

    areas_and_borders = [(area, border) for area, border in zip(areas, borders)]
    return areas_and_borders


total_fence_needed = count_areas_and_borders(garden)
total_fence_needed = [area*perimeter for area, perimeter in total_fence_needed]

print(f"Part 1 answer is {sum(total_fence_needed)}")