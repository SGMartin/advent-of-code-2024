def is_valid_report(report: list, allowed_error=True, ignore_index=-1) -> bool:
    # Remove element at ignore_index if specified
    report_to_eval = [x for i, x in enumerate(report) if i != ignore_index] if ignore_index >= 0 else report

    # Check if report is sorted in ascending or descending order
    if report_to_eval != sorted(report_to_eval) and report_to_eval != sorted(report_to_eval, reverse=True):
        return False

    # Check if consecutive differences are within range [1, 3]
    if not all(abs(prev - next_) in range(1, 4) for prev, next_ in zip(report_to_eval, report_to_eval[1:])):
        return False

    return True


def count_valid_reports(reports: list, allowed_error=True) -> int:
    valid_reports = 0
    for report in reports:
        if is_valid_report(report, allowed_error=False):  # Part 1: no error allowed
            valid_reports += 1
        elif allowed_error:  # Part 2: check after ignoring one element
            for idx in range(len(report)):
                if is_valid_report(report, allowed_error=False, ignore_index=idx):
                    valid_reports += 1
                    break
    return valid_reports


# Read input
with open("puzzle_input.txt", "r") as file:
    reports = [list(map(int, line.strip().split())) for line in file]

# Count valid reports for Part 1 and Part 2
valid_part1_reports = count_valid_reports(reports, allowed_error=False)
valid_part2_reports = count_valid_reports(reports, allowed_error=True)

# Print results
print(f"Part 1 answer is {valid_part1_reports}")
print(f"Part 2 answer is {valid_part2_reports}")