def is_valid_report(report: list, allowed_error=True, ignore_index=-1) -> bool:

    is_good_report = True

    # Generate the actual report based on idx
    if ignore_index >= 0:
        report_to_eval = [x for i, x in enumerate(report) if i != ignore_index]
    else:
        report_to_eval = report

    # Presort it
    ascending_report = sorted(report_to_eval, reverse=False)
    descending_report = sorted(report_to_eval, reverse=True)

    if not (ascending_report == report_to_eval or descending_report == report_to_eval):
        is_good_report = False

    for previous_value, next_value in zip(report_to_eval, report_to_eval[1::]):
        if abs(previous_value - next_value) not in range(1, 4):
            is_good_report = False

    if not is_good_report and allowed_error:

        if ignore_index >= len(report):
            is_good_report = False
        else:
            # Remove the offending position
            new_index = ignore_index + 1
            is_good_report = is_valid_report(
                report=report,
                allowed_error=True,
                ignore_index=new_index
                )

    return is_good_report

with open("puzzle_input.txt", "r") as file:
    reports = [list(map(int, line.strip().split())) for line in file]


valid_part1_reports = [True for report in reports if is_valid_report(report, allowed_error=False)]
valid_part2_reports = [True for report in reports if is_valid_report(report, allowed_error=True)]

print(f"Part 1 answer is {sum(valid_part1_reports)}")
print(f"Part 2 answer is {sum(valid_part2_reports)}")
