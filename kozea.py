#!/usr/bin/env python
from collections import OrderedDict
from json import JSONDecodeError
from xml.etree import ElementTree as etree

import mandrill
import requests
from flask import (Flask, abort, current_app, redirect, render_template,
                   request, session, url_for)
from jinja2.exceptions import TemplateNotFound

app = Flask(__name__)
app.secret_key = 'change_me!'
app.config.from_envvar('KOZEA_CONFIG', silent=True)

ACCESS_TOKEN = app.config.get('ACCESS_TOKEN')
MANDRILL_KEY = app.config.get('MANDRILL_KEY')
TITLES = OrderedDict([
    ('index', 'Accueil'), ('about', 'À propos'),
    ('activity', 'Notre activité'), ('expertise', 'Notre expertise'),
    ('references', 'Nos références'), ('contact', 'Contact'),
    ('legal', 'Mentions légales'),
    ('options', 'Options de confidentialité')
])


@app.errorhandler(404)
@app.errorhandler(TemplateNotFound)
def page_not_found(e):
    return render_template(
        '404.html', titles=TITLES, page='error404', current_title='404'), 404


@app.route('/')
@app.route('/<page>')
def page(page='index'):
    """Display each view."""
    kwargs = {}
    if page == 'index':
        try:
            json = requests.get(
                "https://api.instagram.com/v1/users/self/media/recent/"
                "?access_token={}&count=4".format(ACCESS_TOKEN),
                timeout=3).json()
        except (requests.exceptions.ReadTimeout, JSONDecodeError):
            json = {}
        render_insta = []
        for media in json.get('data', []):
            render_insta.append({
                'link': media.get('link', ''),
                'src': (
                    media.get('images').get('standard_resolution').get('url')),
                'title': media.get('caption', {}).get('text', '')})
        try:
            tree = etree.fromstring(requests.get(
                'https://kozeagroup.wordpress.com/category/kozea/feed/',
                timeout=3).text)
        except requests.exceptions.ReadTimeout:
            channel = []
        else:
            channel, = tree
        render_wordpress = []
        for child in channel:
            if child.tag == 'item':
                item = {}
                for grandchild in child:
                    if grandchild.tag == 'title':
                        item['title'] = grandchild.text
                    elif grandchild.tag == 'link':
                        item['link'] = grandchild.text
                render_wordpress.append(item)
        kwargs = {
            'render_insta': render_insta,
            'render_wordpress': render_wordpress}
    try:
        return render_template(
            '{}.html'.format(page), page=page, current_title=TITLES[page],
            titles=TITLES, **kwargs)
    except KeyError:
        abort(404)


@app.route('/send_mail/<mail_type>', methods=['POST'])
def send_mail(mail_type):
    assert mail_type == 'contact'
    mandrill_client = mandrill.Mandrill(MANDRILL_KEY)
    form = request.form
    subject = 'Prise de contact sur le site de Kozea'
    content = '<br>'.join([
        'Email : %s' % form['email'],
        'Nom / Société: %s' % form['name'],
        'Demande : %s ' % form['question']])
    message = {
        'to': [{'email': 'contact@kozea.fr'}],
        'subject': subject,
        'from_email': 'contact@kozea.fr',
        'html': content
    }
    if not current_app.debug:
        mandrill_client.messages.send(message=message)
    return ''


@app.route('/cookies', methods=['POST'])
def cookies():
    if request.form.get('allow'):
        session['analytics'] = session['facebook'] = True
        return 'ok'
    elif request.form.get('deny'):
        session['analytics'] = session['facebook'] = False
        return 'ok'

    for cookie in ('analytics', 'facebook'):
        session[cookie] = bool(request.form.get(cookie))
    return redirect(url_for('page'))


if __name__ == '__main__':
    from sassutils.wsgi import SassMiddleware
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'kozea': ('static', 'static', '/static')})
    app.run(debug=True, host='0.0.0.0')
