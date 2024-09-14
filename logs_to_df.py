import re

def logs_to_df(line):
    columns = ['client', 'userid', 'datetime', 'method', 'request', 'status', 'size', 'referer', 'user_agent']
    common_regex = r'^(?P<client>[^\s]+) \S+ (?P<userid>[^\s]+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-)'
    combined_regex = r'^(?P<client>[^\s]+) \S+ (?P<userid>[^\s]+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-) "(?P<referrer>[^"]*)" "(?P<useragent>[^"]*)'
    matches = re.findall(combined_regex, line)
    if matches:
        log_line = matches[0]
# Process log_line further
    else:
        # Handle the case where no match is found
        log_line = None
    return log_line