#!/usr/bin/env python
from flask import Flask, redirect, render_template
from instagram.client import InstagramAPI


app = Flask(__name__)
app.config.from_envvar('KOZEA_SETTINGS')

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
    #Care with access_token. It may expire one day.
    instaAPI = InstagramAPI(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET, access_token=ACCESS_TOKEN)
    recent_media, next_ = instaAPI.user_recent_media(user_id=USER_ID, count=3)
    render_insta = []
    for media in recent_media:
        render_insta.append({
            'link': media.link,
            'src': media.get_low_resolution_url(),
            'title': media.caption.text})
    return render_template(
        'index.html', page='index', render_insta=render_insta)


if __name__ == '__main__':
    from sassutils.wsgi import SassMiddleware
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'kozea': ('static', 'static', '/static')})
    app.run(debug=True, host='0.0.0.0')
