import imaplib
import environ

env = environ.Env()

# it will read the .env file located in same folder path
environ.Env.read_env()


server  = env('IMAP_SERVER')
user = env('EMAIL_USER')
password = env('EMAIL_PASSWORD')


def connect(server, user, password):
    imap_conn = imaplib.IMAP4_SSL(server)
    imap_conn.login(user, password)
    return imap_conn

def delete_email(instance, email_id):
    typ, delete_response = instance.fetch(email_id, '(FLAGS)')
    typ, response = instance.store(email_id, '+FLAGS', r'(\Deleted)')
    
def purge_email(instance):
    typ, response = instance.expunge()
    
keywords_list = ['You won', 'Trip']

for keyword in keywords_list:
    conn = connect(server, user, password)
    conn.select('Inbox')
    typ, msg = conn.search(None, '(BODY "' + keyword + '")')
    msg = msg[0].split()
    for email_id in msg:
        delete_email(conn, email_id)
    purge_email(conn)
    print('Complete!')
    