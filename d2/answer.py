with open("example.txt", "r") as file:
    reports = [list(map(int, line.strip().split())) for line in file]


# A report is considered safe if it's sorted ascending or
# descending and in 1-2 units intervals
valid_reports = 0
for report in reports:
    # Presort the lists
    ascending_report = sorted(report, reverse=False)
    descending_report = sorted(report, reverse=True)

    over_limit = False
    dampener_limit = True

    if not (ascending_report == report or descending_report == report):
        continue

    for previous_value, next_value in zip(report, report[1:]):
        if abs(previous_value - next_value) not in range(1, 4):
            if dampener_limit:
                dampener_limit = False
                report.remove(next_value)
                print("attempt to remove element")
                print(report)
            else:
                over_limit = True
                print("OVERLIMIT")
                print(report)
                break

    if not over_limit:
        valid_reports += 1
        print("VALID")
        print(report)

print(f"Part 1 answer is {valid_reports}")
