import re
import pandas as pd

def preprocessor(raw_text):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:\u202f)?[AP]M\s-\s"
    messages = re.split(pattern, raw_text)[1:]
    dates = re.findall(pattern, raw_text)
    dates = [d.replace('\u202f', ' ') for d in dates]
    users = []
    msg_text = []
    for message in messages:
        entry = re.split(r'([^:]+):\s', message)
        if len(entry) > 2:
            users.append(entry[1].strip())        # username
            msg_text.append(entry[2].strip())     # message content
        else:
            users.append("group_notification")
            msg_text.append(entry[0].strip())
    data= pd.DataFrame({
        "date": dates,
        "user": users,
        "message": msg_text
    })
    data["date"] = pd.to_datetime(data["date"], format="%m/%d/%y, %I:%M %p - ")
    data["month_num"] = data["date"].dt.month
    data["year"] = data["date"].dt.year
    data["only_date"] = data["date"].dt.date
    data["day_name"] = data["date"].dt.day_name()
    data["month"] = data["date"].dt.month_name()
    data["day"] = data["date"].dt.day
    data["hour"] = data["date"].dt.hour
    data["minute"] = data["date"].dt.minute
    period = []
    for hour in data[["day_name", "hour"]]["hour"]:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    data["period"] = period
    return data



