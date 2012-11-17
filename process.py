import email.message
import email.mime.text
import email.mime.multipart

import email


# Prefer quoted printable
email.Charset.add_charset('utf-8', email.Charset.QP, email.Charset.QP, 'utf-8')


# ** message ID could include some unique info

def dump2msg(val):
    '''d (input) is a dictionary provided by json-parsing
    mails to Monitoring-private.'''
    msg = email.mime.multipart.MIMEMultipart()
    msg['From'] = 'all@openhatch.org'
    body = ''
    for tag in val['tags']:
        body += tag['text'] + '\n\n'
    for answer in val['answer_data']:
        for key in ['text', 'title']:
            item = answer[key]
            if item:
                body += item + '\n\n'
    for person_key in [
        'irc_nick',
        'homepage_url',
        'contact_blurb',
        'bio']:
        item = val['person'][person_key]
        if item:
            body += item + '\n\n'
    msg.attach(email.mime.text.MIMEText(
            body,
            'text',
            'utf-8'))
    return msg

if __name__ == '__main__':
    import sys
    import json
    val = json.loads(sys.stdin.read())
    sys.stdout.write(dump2msg(val).as_string())
