import csv

# import pandas as pd
import openpyxl

DAY_ROWS = [
    (15, 20, "Monday"),  # Monday
    (24, 28, "Tuesday"),  # Tuesday
    (32, 39, "Wednesday"),  # Wednesday
    (43, 50, "Thursday"),  # Thursday
    (54, 61, "Friday"),  # Friday
    (66, 73, "Weekend"),  # Weekend: Saturday & Sunday
]


def merged_size(cell, sheet):
    for rng in sheet.merged_cells:
        # print(cell.row, rng.left[0][0], ":", cell.column, rng.left[0][1])
        if cell.row == rng.left[0][0] and cell.column == rng.left[0][1]:
            return rng.size


filename = "schedule.xlsm"
wb = openpyxl.load_workbook(filename)
sheet = wb["Schedule"]
# row 14 is the first row of time headers, col B to AL

with open("tasks.csv", mode="w") as output_file:
    output_writer = csv.writer(
        output_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    output_writer.writerow(
        ["weekday", "location", "start_time", "end_time", "task_txt"]
    )
    for day in DAY_ROWS:
        print("=" * 80)
        rng_start = "B" + str(day[0])
        rng_end = "AJ" + str(day[1])
        for row in sheet[rng_start:rng_end]:
            for cl in row:
                if cl.value:
                    weekday = day[2]
                    location = sheet.cell(row=cl.row, column=1).value
                    start = sheet.cell(row=14, column=cl.column).value
                    mrg = merged_size(cl, sheet)
                    if mrg:
                        end = sheet.cell(
                            row=14, column=cl.column + mrg["columns"]
                        ).value
                    else:
                        end = sheet.cell(row=14, column=cl.column + 1).value
                    task = cl.value
                    output_writer.writerow([weekday, location, start, end, task])
                    print(weekday, location, start, end, task)
