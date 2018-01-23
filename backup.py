from boj import BOJ
import sys
from getpass import getpass
import os


if __name__ == '__main__':
    for arg in sys.argv:
        print(arg)

    myboj = BOJ()

    login_id = input('BOJ login_id: ')
    password = getpass('BOJ password: ')

    success = myboj.login(login_id, password)

    if not success:
        print('Error: invalid id or password')
        exit(1)

    dir = 'BOJ-' + myboj.user_id

    try:
        os.mkdir(dir, 0o755)
    except FileExistsError:
        pass

    submit_ids = myboj.get_submit_ids(result_id=4)

    for submit_id in submit_ids:
        submit = myboj.get_sourcecode(submit_id)

        filename = '%s-%s-%s.%s' % (submit_id, submit['problem_id'], submit['lang'], submit['ext'])
        f = open(os.path.join(dir, filename), 'w')
        f.write(submit['sourcecode'])
        f.close()
