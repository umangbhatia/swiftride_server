import csv
import datetime
import calendar


def multilinear_regression(date, time):
    day, month, year = (int(x) for x in date.split('-'))
    date_format_org = datetime.date(int(year),int(month),int(day))
    day_name_org = calendar.day_name[date_format_org.weekday()]
    with open('bus_data.csv','rt') as f:
        data = csv.reader(f)
        line_count = 0
        for row in data:
            line_count = line_count + 1
            if line_count > 1:
                date_csv = row[0]
                day, month, year = (int(x) for x in date_csv.split('-'))
                date_format_csv = datetime.date(int(year),int(month),int(day))
                day_name_csv = calendar.day_name[date_format_csv.weekday()]
                if day_name_org == day_name_csv and time == row[1]:
                    crowd = float(row[2])
                    crowd_level_predicted = True

    if crowd_level_predicted:
        if crowd <= 0.33:
            crowd_level = [crowd,1]
        elif 0.33 < crowd <= 0.66:
            crowd_level = [crowd,2]
        else:
            crowd_level = [crowd,3]
    else:
        crowd_level = [0,0]
    return crowd_level
