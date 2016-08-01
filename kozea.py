#!/usr/bin/env python
from flask import current_app, Flask, render_template, request
from jinja2.exceptions import TemplateNotFound
import mandrill
import requests


app = Flask(__name__)
app.config.from_envvar('KOZEA_CONFIG', silent=True)

ACCESS_TOKEN = app.config.get('ACCESS_TOKEN')
MANDRILL_KEY = app.config.get('MANDRILL_KEY')


@app.errorhandler(404)
@app.errorhandler(TemplateNotFound)
def page_not_found(e):
    return render_template('404.html')


@app.route('/')
@app.route('/<page>')
def page(page='index'):
    if page == 'index':
        return get_insta_media()
    return render_template('{}.html'.format(page), page=page)


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


def get_insta_media():
    """ Care with access_token. It may expire one day. """
    request = requests.get(
        "https://api.instagram.com/v1/users/self/media/recent/"
        "?access_token={}&count=4".format(ACCESS_TOKEN)).json()
    render_insta = []
    for media in request.get('data', []):
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
