#!/usr/bin/env python
from flask import Flask, redirect, request, render_template
from instagram.client import InstagramAPI
from instagram.oauth2 import OAuth2AuthExchangeError


app = Flask(__name__)
app.config.from_envvar('KOZEA_SETTINGS')

CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']
REDIRECT_URI = app.config['REDIRECT_URI']


@app.route('/<page>')
def page(page='index'):
    recorded_pages = ['index', '404', 'about', 'activity', 'contact',
        'expertise', 'legal', 'references']
    if page in recorded_pages:
        return render_template('{}.html'.format(page), page=page)
    else:
        return render_template('404.html')

@app.route('/')
@app.route('/index')
def index():
    instaAPI = InstagramAPI(client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
    try:
        access_token = instaAPI.exchange_code_for_access_token(
            request.args.get('code'))[0]
    except OAuth2AuthExchangeError:
        redirect_uri = instaAPI.get_authorize_login_url(
            scope = ['public_content'])
        return redirect(redirect_uri)
    instaAPI = InstagramAPI(client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET, access_token=access_token)
    recent_media, next_ = instaAPI.user_recent_media(
        user_id=instaAPI.user().id, count=3)
    render_insta = []
    for media in recent_media:
        render_insta.append({
            'link': media.link,
            'src': media.get_low_resolution_url(),
            'title': media.caption.text})
    return render_template('index.html', page='index',
        render_insta=render_insta)


if __name__ == '__main__':
    from sassutils.wsgi import SassMiddleware
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'kozea': ('static', 'static', '/static')})
    app.run(debug=True, host='0.0.0.0')
