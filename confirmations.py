import os
import datetime
import sendgrid
import pystache


def send_email_with_score(score, title, address):
    with open('mail_templates/score_html.mst') as template:
        a = {'date': unicode(datetime.datetime.now().strftime("%d.%m.%Y g.%H:%M")),
             'score': score,
             'title': title}
        tpl = unicode(template.read(), 'utf-8')
        content = pystache.render(tpl, **a)
    #with open('score_text.mst') as template:
    #    tpl = unicode(template.read(), 'utf-8')
    #    content2 = pystache.render(tpl, **a)

    sg = sendgrid.SendGridClient('app27722588@heroku.com', 'oqycemvj')

    message = sendgrid.Mail()
    message.add_to(address)
    message.set_subject('Your score from test %s'%title)
    message.set_html(content)
    #message.set_text(content2)
    message.set_from('results@questions2.com')
    status, msg = sg.send(message)