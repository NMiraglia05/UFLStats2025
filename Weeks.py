def week():
    import datetime

    weeks={
        (datetime.datetime(2025, 4, 28), datetime.datetime(2025, 5, 4)): 6,
        (datetime.datetime(2025, 5, 5), datetime.datetime(2025, 5, 11)): 7,
        (datetime.datetime(2025, 5, 12), datetime.datetime(2025, 5, 18)): 8,
        (datetime.datetime(2025, 5, 19), datetime.datetime(2025, 5, 25)): 9,
        (datetime.datetime(2025, 5, 26), datetime.datetime(2025, 6, 1)): 10
    }

    date=datetime.datetime.today()

    for(start,end), week_number in weeks.items():
        if start <= date <= end:
            weeknumber=week_number
            break
        else:
            week=0

    return weeknumber
