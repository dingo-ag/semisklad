from django.core.mail import send_mail
from django.template.loader import render_to_string
from semisklad.settings.local import SITE_URL
from django.core.mail import EmailMessage


def worker_post_save(sender, **kwargs):
    if kwargs.get('created', False):
        user = kwargs.get('instance')
        message_context = {
            'name': user.name,
            'image_link': 'images/SOM.png',
            'login': user.email,
            'site_url': SITE_URL
        }
        html_text = render_to_string('emails/registration_successful.html', context=message_context)
        print(html_text)
        email = EmailMessage('Theme', html_text, 'dingo_dnu@mail.ru', ['dingo_dnu@mail.ru'])
        email.content_subtype = "html"
        # email.attach_file('static/images/SOM.png', mimetype='image/png')
        email.send()
