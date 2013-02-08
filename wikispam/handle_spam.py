#!/usr/bin/python
import collections

# FIXME: Automate the creation of this via the last run
# e.g. git log --since='Wed Dec 5 22:57:06 2012 +0000'
GIT_LOG_OUTPUT = open('/tmp/output').read()

ParsedLogItem = collections.namedtuple('ParsedLogItem', 'author full_string commit')

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
        if line.startswith("commit "):
            commit = line.split()[1]
    assert author
    assert commit
    return ParsedLogItem(full_string=full_string, author=author, commit=commit)

def list_authors(data):
    for thing in sorted(set([datum.author for datum in data])):
        print "*", thing

def review_author(data):
    print 'Here is a list of authors:'
    list_authors(data)
    name = raw_input('Who do you want to review?')
    just_by_them = [k for k in data
                    if k.author.lower() == name.lower()]
    for commit in just_by_them:
        print commit
    looks_spammy = raw_input("Looks like all spam? y/N ")
    if (looks_spammy.strip() and (looks_spammy[0].lower() == 'y')):
        print "OK. Next steps:"
        print "Block them:", ("https://openhatch.org/wiki/Special:Block?wpTarget=" + name + "&wpExpiry=infinite&wpExpiry-other=&wpReason=Spamming+links+to+external+sites&wpReason-other=&wpCreateAccount=1&wpDisableEmail=1&wpAutoBlock=1&wpWatch=1&wpHardBlock=1&wpEditToken=5aaacea7cd97694641472b712f0ad9b6%2B\&title=Special%3ABlock%2FGchragegarr&redirectparams=&wpPreviousTarget=Gchragegarr&wpConfirm=")

def quit_placeholder():
    raise NotImplemented

def prompt_for_action():
    nexts = NextSteps(people_to_ban=[])
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
