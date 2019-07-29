from datetime import datetime


def str_to_date(strdate):
    return datetime.strptime(strdate, "%d/%m/%Y").date()