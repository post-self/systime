from datetime import (
    date,
    datetime,
)

from flask import (
    Flask,
    render_template,
)
from pyluach import dates

from systime import Systime


HOLIDAY_REPLACEMENTS = {
    'Succos': 'Sukkot',
    'Shmini Atzeres': 'Shemini Atzeret',
    'Simchas Torah': 'Simchat Torah',
    'Chanuka': 'Hanukkah',
    'Shavuos': 'Shavuot',
    'Taanis Esther': 'Taanit Esther',
}


app = Flask('systime')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/1/today')
def today():
    return from_date(date.today().isoformat())

@app.route('/api/1/now')
def now():
    return from_datetime(datetime.now().isoformat())

@app.route('/api/1/systime/<systime>')
def from_systime(systime):
    s = Systime.from_string(systime)
    if s.time is None:
        return from_date(s.to_date().isoformat())
    else:
        return from_datetime(s.to_datetime().isoformat())

@app.route('/api/1/date/<date_str>')
def from_date(date_str):
    g = date.fromisoformat(date_str)
    s = Systime.from_date(g)
    h = dates.GregorianDate.from_pydate(g).to_heb()
    return {
        'systime': {
            'string': s.to_string(),
            'year': s.year,
            'day': s.day,
            'time': None,
        },
        'gregorian': {
            'string': g.isoformat(),
            'year': g.year,
            'month': g.month,
            'day': g.day,
            'day_of_week': f'{g:%A}',
            'time': None,
        },
        'hebrew': {
            'string': f'{h:%-d %B, %Y}',
            'year': h.year,
            'month': h.month,
            'day': h.day,
            'fast': HOLIDAY_REPLACEMENTS.get(h.fast_day(), h.fast_day()),
            'festival': HOLIDAY_REPLACEMENTS.get(h.festival(), h.festival()),
            'holiday': HOLIDAY_REPLACEMENTS.get(h.holiday(), h.holiday()),
            'shabbat': h.shabbos() == h,
        },
    }

@app.route('/api/1/datetime/<datetime_str>')
def from_datetime(datetime_str):
    g = datetime.fromisoformat(datetime_str)
    s = Systime.from_datetime(g)
    h = dates.GregorianDate.from_pydate(g.date()).to_heb()
    return {
        'systime': {
            'string': s.to_string(),
            'year': s.year,
            'day': s.day,
            'time': s.time,
        },
        'gregorian': {
            'string': g.isoformat(),
            'year': g.year,
            'month': g.month,
            'day': g.day,
            'day_of_week': f'{g:%A}',
            'time': g.time().isoformat(),
        },
        'hebrew': {
            'string': f'{h:%-d %B, %Y}',
            'year': h.year,
            'month': h.month,
            'day': h.day,
            'fast': HOLIDAY_REPLACEMENTS.get(h.fast_day(), h.fast_day()),
            'festival': HOLIDAY_REPLACEMENTS.get(h.festival(), h.festival()),
            'holiday': HOLIDAY_REPLACEMENTS.get(h.holiday(), h.holiday()),
            'shabbat': h.shabbos() == h,
        },
    }
