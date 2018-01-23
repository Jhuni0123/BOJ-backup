from boj import BOJ
from getpass import getpass
import os
import argparse


def process_argument():
    parser = argparse.ArgumentParser(description='Backup BOJ source codes.')
    parser.add_argument('-s', '--silent', action='store_true',
                        help='do not show progress')
    parser.add_argument('-l', '--limit', type=int, default=None,
                        help='limit the number of codes to backup from recent code')
    parser.add_argument('-r', '--result', type=int, default=4,
                        help='result_id')
    return parser.parse_args()


if __name__ == '__main__':
    args = process_argument()

    myboj = BOJ()

    # login
    login_id = input('BOJ login_id: ')
    password = getpass('BOJ password: ')

    success = myboj.login(login_id, password)

    if not success:
        print('error: invalid id or password')
        exit(1)

    submit_ids = myboj.get_submit_ids(args.result, args.limit, args.silent)

    # backup
    dirname = 'BOJ-' + myboj.user_id

    try:
        os.mkdir(dirname, 0o755)
    except FileExistsError:
        pass

    if not args.silent:
        print("Backing-up in '%s/'" % dirname)

    for idx, submit_id in enumerate(submit_ids):
        submit = myboj.get_sourcecode(submit_id)

        filename = '%s-%s-%s.%s' % (submit_id, submit['problem_id'], submit['lang'], submit['ext'])
        f = open(os.path.join(dirname, filename), 'w')
        f.write(submit['sourcecode'])
        f.close()
        if not args.silent:
            print("\r(%d/%d) '%s' saved.     " % (idx+1, len(submit_ids), filename), end='')
    if not args.silent:
        print('\nDone!')
