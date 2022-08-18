import datetime
from django.core.validators import MaxValueValidator


def max_value_current_year(value):

    def current_year():
        return datetime.date.today().year

    return MaxValueValidator(current_year())(value)
