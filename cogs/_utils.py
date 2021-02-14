from string import Template


def strfdelta(tdelta, fmt):
    """strftime but operated with :class:`datetime.timedelta` instead

    :param tdelta: timedelta object targeted
    :param fmt: format string
    :return: a formatted string
    """

    class DeltaTemplate(Template):
        delimiter = "%"

    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    return DeltaTemplate(fmt).substitute(**d)
