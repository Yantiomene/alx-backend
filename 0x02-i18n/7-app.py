#!/usr/bin/env python3
"""Basic Flask and Babel app setup"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from pytz import timezone
import pytz.exceptions


class Config(object):
    """Configuration class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale():
    """Determine the best match with supported languages"""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    if g.user:
        locale = g.user.get('locale')
        if locale in app.config['LANGUAGES']:
            return locale

    locale = request.headers.get('locale', None)
    if locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Determine and return the timezone"""
    tz = request.args.get('timezone', None)
    if tz:
        try:
            return timezone(tz).zone
        except pytz.exception.UnkownTimeZoneError:
            pass
    if g.user:
        try:
            tz = g.user.get('timezone')
            return timezone(tz).zone
        except pytz.exception.UnkownTimeZoneError:
            pass
    d_tz = app.config['BABEL_DEFAULT_TIMEZONE']
    return default_tz


def get_user():
    """Get the user dict or None"""
    log_id = request.args.get('login_as')
    if log_id:
        return users.get(int(log_id))
    return None


@app.before_request
def before_request() -> None:
    """Execute before any request"""
    user = get_user()
    g.user = user


@app.route("/")
def index():
    """Hello world"""
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)
