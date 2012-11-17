import subprocess
import os
import sys
sys.path.append('/usr/bin')
import sb_filter
import mock
import StringIO

def is_spammy(username):
    fake_stdout = StringIO.StringIO()
    fake_stdin = StringIO.StringIO(open('msgs/' + username).read())
    @mock.patch('sys.stdin', fake_stdin)
    @mock.patch('sys.stdout', fake_stdout)
    @mock.patch('sys.argv', ['sb_filter'])
    def do_work():
        sb_filter.main()
        output = fake_stdout.getvalue()
        lines = output.split('\n')
        for line in lines:
            if line.startswith('X-Spam'):
                if 'spam;' in line:
                    return (True, output)
                return (False, output)
        return (False, output)
    return do_work()

def train_as_ham(username):
    p = subprocess.Popen(['sb_filter', '-g'],
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    p.communicate(input=open('msgs/' + username).read())

def main():
    for username in os.listdir('msgs'):
        if username == '.gitignore':
            continue
        classification, content = is_spammy(username)
        if classification:
            my_file = open('/tmp/myfile', 'w')
            my_file.write(content)
            my_file.close()
            os.system("less /tmp/myfile")
            was_spam = raw_input("Was it spam? y/N> ").lower()[:1]
            if was_spam == 'y':
                print 'WAHOO'
                print 'We would delete', username
            else:
                print 'FALSE POSITIVE'
                print 'Training...'
                train_as_ham(username)

if __name__ == '__main__':
    main()
