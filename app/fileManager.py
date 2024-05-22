import os
import re
from datetime import datetime, timedelta


def clean_old_records(diretorio):
    allfilles = os.listdir(diretorio)
    for file in allfilles:
        if is_file_older_than(file, 12 * 60):
            print(diretorio)
            print(file)
            os.remove(diretorio + file)


def is_file_older_than(file_name, minutes):
    match = re.search(r'\d{2}-\d{2}-\d{4}_\d{6}', file_name)
    if match is None:
        return False

    timestamp_str = match.group()
    timestamp = datetime.strptime(timestamp_str, "%d-%m-%Y_%H%M%S")
    now_minus_x_minutes = datetime.now() - timedelta(minutes=minutes)

    return timestamp < now_minus_x_minutes
