from datetime import datetime


def str_to_date(strdate):
    """
    Converts a string to a date

    Args:
        strdate: string to be converted

    Returns:
        Date from strdate
    """
    return datetime.strptime(strdate, "%d/%m/%Y").date()
