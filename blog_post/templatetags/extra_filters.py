from django import template
from jdatetime import datetime
from pytz import timezone

register = template.Library()

iran_tz = timezone('Asia/Tehran')


@register.filter(name='time_duration_calculator')
def time_duration_calculator(time):
    time_difference = abs(datetime.now(iran_tz) - time)
    if time_difference.days == 0:
        return "امروز"
    elif time_difference.days < 7:
        return f" روز پیش{time_difference.days}"
    elif time_difference.days < 30:
        weeks = time_difference.days // 7
        return f" هفته پیش{weeks}"
    elif time_difference.days < 365:
        months = time_difference.days // 30
        return f" ماه پیش{months}"
    elif time_difference.days >= 365:
        years = time_difference.days // 365
        return f" سال پیش{years}"


@register.filter(name='date_format')
def date_format(date):
    return date.strftime("%Y %B %d")