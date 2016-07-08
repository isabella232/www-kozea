#!/usr/bin/env python
from flask import current_app, Flask, render_template, request
import mandrill
import requests


app = Flask(__name__)
app.config.from_envvar('KOZEA_CONFIG', silent=True)

ACCESS_TOKEN = app.config.get('ACCESS_TOKEN')
MANDRILL_KEY = app.config.get('MANDRILL_KEY')


@app.route('/')
@app.route('/<page>')
def page(page='index'):
    recorded_pages = [
        'index', 'about', 'activity', 'contact', 'expertise', 'legal',
        'references']
    if page in recorded_pages:
        if page == 'index':
            return get_insta_media()
        return render_template('{}.html'.format(page), page=page)
    return render_template('404.html')


@app.route('/make_contact', methods=['POST'])
def make_contact():
    mandrill_client = mandrill.Mandrill(MANDRILL_KEY)
    form = request.form
    message = {
        'to': [{'email': 'contact@kozea.fr'}],
        'subject': 'Prise de contact sur le site de Kozea',
        'from_email': 'contact@kozea.fr',
        'html': '<br>'.join([
            'Email : %s' % form['email'], 'Nom / Société: %s' % form['name'],
            'Demande : %s ' % form['question']])
    }
    if not current_app.debug:
        mandrill_client.messages.send(message=message)
    return ''


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
