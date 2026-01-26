import datetime


def get_current_time():
    current_data = datetime.datetime.now()
    timestamp = int(current_data.timestamp())
    date = datetime.datetime.fromtimestamp(timestamp)
    now_strftime = date.strftime('%a %d %b %Y, %I:%M%p')
    return now_strftime
