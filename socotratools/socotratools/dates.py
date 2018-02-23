import datetime
import time
import pytz


# Converts string representation to epoch in appropriate timezone
# Example - convert 1/1/1983 0:00 PST to timestamp
# date_to_millis('1/1/1983', 'Americas/Los Angeles', '%m/%d/%Y')
def date_to_millis(date_input, tz_str, date_format):
    stead_tz = pytz.timezone(tz_str)
    parsed_date = time.strptime(date_input, date_format)
    year, month, day = parsed_date[0:3]
    date_without_timezone = datetime.datetime(year, month, day, 0, 0, 0)
    local_datetime = stead_tz.localize(date_without_timezone)
    epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
    unix_timestamp = int((local_datetime - epoch).total_seconds()) * 1000
    return unix_timestamp
