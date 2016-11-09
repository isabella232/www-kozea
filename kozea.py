#!/usr/bin/env python
from collections import OrderedDict

from flask import current_app, Flask, render_template, request
from jinja2.exceptions import TemplateNotFound
import mandrill
import requests


app = Flask(__name__)
app.config.from_envvar('KOZEA_CONFIG', silent=True)

ACCESS_TOKEN = app.config.get('ACCESS_TOKEN')
MANDRILL_KEY = app.config.get('MANDRILL_KEY')
TITLES = OrderedDict([
    ('index', 'Accueil'), ('about', 'À propos'),
    ('activity', 'Notre activité'), ('expertise', 'Notre expertise'),
    ('references', 'Nos références'), ('contact', 'Contact'),
    ('legal', 'Mentions légales')
])


@app.errorhandler(404)
@app.errorhandler(TemplateNotFound)
def page_not_found(e):
    return render_template('404.html')


@app.route('/')
@app.route('/<page>')
def page(page='index'):
    """Display each view."""
    kwargs = {}
    if page == 'index':
        request = requests.get(
            "https://api.instagram.com/v1/users/self/media/recent/"
            "?access_token={}&count=4".format(ACCESS_TOKEN)).json()
        render_insta = []
        for media in request.get('data', []):
            render_insta.append({
                'link': media.get('link'),
                'src': (
                    media.get('images').get('standard_resolution').get('url')),
                'title': media.get('caption').get('text')})
        kwargs = {'render_insta': render_insta}
    return render_template(
        '{}.html'.format(page), page=page, current_title=TITLES[page],
        titles=TITLES, **kwargs)


@app.route('/send_mail/<mail_type>', methods=['POST'])
def send_mail(mail_type):
    mandrill_client = mandrill.Mandrill(MANDRILL_KEY)
    form = request.form
    if mail_type == 'contact':
        subject = 'Prise de contact sur le site de Kozea'
        content = '<br>'.join([
            'Email : %s' % form['email'],
            'Nom / Société: %s' % form['name'],
            'Demande : %s ' % form['question']])
    else:
        subject = 'Inscription à la newsletter Kozea'
        content = 'Mail : %s' % form['email']
    message = {
        'to': [{'email': 'contact@kozea.fr'}],
        'subject': subject,
        'from_email': 'contact@kozea.fr',
        'html': content
    }
    if not current_app.debug:
        mandrill_client.messages.send(message=message)
    return ''


if __name__ == '__main__':
    from sassutils.wsgi import SassMiddleware
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'kozea': ('static', 'static', '/static')})
    app.run(debug=True, host='0.0.0.0')
