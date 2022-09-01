from django import template
from jdatetime import datetime
from pytz import timezone

register = template.Library()

#iran_tz = timezone('Asia/Tehran')


@register.filter(name='time_duration_calculator')
def time_duration_calculator(time):
    time_difference = abs(datetime.now() - time)
    if time_difference.days == 0:
        return "امروز"
    elif time_difference.days < 7:
        return f"{time_difference.days} روز پیش  "
    elif time_difference.days < 30:
        weeks = time_difference.days // 7
        return f"{weeks} هفته پیش  "
    elif time_difference.days < 365:
        months = time_difference.days // 30
        return f"{months} ماه پیش  "
    elif time_difference.days >= 365:
        years = time_difference.days // 365
        return f"{years} سال پیش   "


@register.filter(name='date_format')
def date_format(date):
    return date.strftime("%Y %B %d")