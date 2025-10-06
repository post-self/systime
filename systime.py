from datetime import (
    date,
    datetime,
    timedelta,
)
import re


SYSTIME_START = 2124
SECONDS_PER_DAY = 86400
SYSTIME_RE = r'^systime (?P<year>-?\d+)\+(?P<day>\d+)(\.(?P<time>\d+))?$'


class Systime:

    def __init__(self, year: int=None, day: int=None, time: float=None):
        self.year = year
        self.day = day
        self.time = time

    def __repr__(self) -> str:
        return self.to_string()

    @classmethod
    def from_date(cls, d: date):
        td = d - date(year=d.year, month=1, day=1)
        year = d.year - SYSTIME_START
        return cls(year=year, day=td.days + 1)

    @classmethod
    def from_datetime(cls, d: datetime):
        result = cls.from_date(d.date())
        result.time = (d.hour * 3600 + d.minute * 60 + d.second) / SECONDS_PER_DAY
        return result

    @classmethod
    def from_string(cls, s: str):
        match = re.match(SYSTIME_RE, s)
        if match is None:
            raise SystimeFormatError()
        year = match.group('year')
        day = match.group('day')
        time = match.group('time')
        if year is None or day is None:
            raise SystimeFormatError()
        yearnum = int(year)
        daynum = int(day)
        timenum = None
        if time is not None:
            timenum = float('0.'+time)
        return cls(year=yearnum, day=daynum, time=timenum)

    def to_date(self) -> date:
        return date(self.year + SYSTIME_START, 1, 1) + timedelta(days=self.day - 1)

    def to_datetime(self) -> datetime:
        if self.time is None:
            raise NoTimeException()
        return datetime.combine(
            date(self.year + SYSTIME_START, 1, 1),
            time(0)) + timedelta(days=self.day, seconds=self.time * SECONDS_PER_DAY)

    def to_string(self, resolution: int=2) -> str:
        result = f'systime {self.year}+{self.day}'
        if self.time is not None:
            result += f'.{int(self.time * 10**resolution)}'
        return result


class NoTimeException(Exception):
    pass


class SystimeFormatError(Exception):
    pass
