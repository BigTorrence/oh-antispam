#!/usr/bin/python
import collections

# FIXME: Automate the creation of this via the last run
# e.g. git log --since='Wed Dec 5 22:57:06 2012 +0000'
GIT_LOG_OUTPUT = open('/tmp/output').read()

ParsedLogItem = collections.namedtuple('ParsedLogItem', 'author full_string')

NextSteps = collections.namedtuple('NextSteps', 'people_to_ban')

def split_into_lines(s):
    ret = []
    this_one = []
    for line in s.split('\n'):
        line = line.rstrip()
        if line.startswith('commit'):
            if this_one:
                ret.append(this_one)
            this_one = []
        this_one.append(line)
    return ret

def parse(list_of_line_lists):
    for line_list in list_of_line_lists:
        assert (type(line_list) == list)
        yield parse_line_list(line_list)

def parse_line_list(l):
    full_string = '\n'.join(l)
    author = None
    for line in l:
        if line.startswith("Author:"):
            author = line.split()[1]
    assert author
    return ParsedLogItem(full_string=full_string, author=author)

def list_authors(data):
    for thing in sorted(set([datum.author for datum in data])):
        print "*", thing

def review_author(data):
    print 'Here is a list of authors:'
    list_authors(data)
    name = raw_input('Who do you want to review?')
    print name

def quit_placeholder():
    raise NotImplemented

def prompt_for_action():
    actions = {'a': (list_authors, 'List (a)uthors'),
               'r': (review_author, '(R)eview author to see if all their edits are spam'),
               'q': (quit_placeholder, '(Q)uit'),
               }
    msg = ' '.join([x[1] for x in actions.values()])
    inp = raw_input("What action to take? " + msg).strip()
    if (inp and inp[0] == 'q'):
        return 'q'

    # else...
    action = actions.get(inp.strip(), None)
    if action:
        return action[0]
    return None

def process():
    line_lists = split_into_lines(GIT_LOG_OUTPUT)
    data = list(parse(line_lists))
    while True:
        action = prompt_for_action()
        if action:
            if action == 'q':
                return
            action(data)
