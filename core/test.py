from datetime import datetime
import calendar

print(calendar.monthrange(2023, 11))

print(datetime(2023, 11, 1))


def print_month(year, month, day):
    day_of_week, month_range = calendar.monthrange(year, month)

    a = 1 - day_of_week
    week = []
    print(['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'])

    for i in range(a, month_range+1):
        if len(week) == 7:
            print(week)
            week = []
        if i <= 0:
            week.append('  ')
        else:
            if i < 10:
                week.append(f'0{i}')
            else:
                week.append(f'{i}')
    else:
        if week:
            for i in range(0, 7 - len(week)):
                week.append("  ")
            print(week)

print_month(2023,12,5)