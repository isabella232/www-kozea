#!/usr/bin/env python
import requests
from flask import Flask, redirect, render_template


app = Flask(__name__)
app.config.from_pyfile('kozea.cfg')

CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']
REDIRECT_URI = app.config['REDIRECT_URI']
USER_ID = app.config['USER_ID']
ACCESS_TOKEN = app.config['ACCESS_TOKEN']


@app.route('/')
@app.route('/<page>')
def page(page='index'):
    recorded_pages = [
        'index', 'about', 'activity', 'contact',
        'expertise', 'legal', 'references']
    if page in recorded_pages:
        if page == 'index':
            return get_insta_media()
        return render_template('{}.html'.format(page), page=page)
    return render_template('404.html')


def get_insta_media():
    """ Care with access_token. It may expire one day. """
    request = requests.get(
        "https://api.instagram.com/v1/users/self/media/recent/"
        "?access_token={}&count=3".format(ACCESS_TOKEN)).json()
    render_insta = []
    for media in request.get('data'):
        render_insta.append({
            'link': media.get('link'),
            'src': media.get('images').get('standard_resolution').get('url'),
            'title': media.get('caption').get('text')})
    return render_template(
        'index.html', page='index', render_insta=render_insta)


if __name__ == '__main__':
    from sassutils.wsgi import SassMiddleware
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'kozea': ('static', 'static', '/static')})
    app.run(debug=True, host='0.0.0.0')
