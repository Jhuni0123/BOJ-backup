from boj import BOJ
from getpass import getpass
import os
import argparse
import textwrap
import requests


def process_argument():
    parser = argparse.ArgumentParser(description='Backup BOJ source codes.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-l', '--limit', type=int, default=None,
                        help='limit the number of codes to backup from recent code')
    parser.add_argument('-r', '--result', type=int, default=4,
                        help=textwrap.dedent('''\
                        select result of submission (default: 4)
                        -1: 모든 결과
                         4: 맞았습니다!!
                         5: 출력 형식
                         6: 틀렸습니다
                         7: 시간 초과
                         8: 메모리 초과
                         9: 출력 초과
                        10: 런타임 에러
                        11: 컴파일 에러
                        '''))
    parser.add_argument('-v', '--verbose', default=False, action='store_true',
                        help='print details of backup')
    return parser.parse_args()


if __name__ == '__main__':
    args = process_argument()

    myboj = BOJ()

    # login
    login_id = input('BOJ login_id: ')
    password = getpass('BOJ password: ')

    try:
        success = myboj.login(login_id, password)

        if not success:
            print('error: invalid id or password')
            exit(1)

        submission_list = myboj.get_submission_list(args.result, args.limit, args.verbose)

        # backup
        dirname = 'BOJ-' + myboj.user_id

        try:
            os.mkdir(dirname, 0o755)
        except FileExistsError:
            pass

        print("Backing-up in '%s/'" % dirname)

        for idx, submit in enumerate(submission_list):
            submit = {**myboj.get_submission_info(submit['submission_id']), **submit}

            filename = '%s-%s-%s.%s' % (submit['submission_id'], submit['problem_id'], submit['lang'], submit['ext'])
            f = open(os.path.join(dirname, filename), 'w')
            f.write(submit['sourcecode'])
            f.close()
            if args.verbose:
                print("(%d/%d) %35s saved." % (idx+1, len(submission_list), filename))
        print('\nDone!')
    except requests.exceptions.ConnectionError:
        print('error: network connection is not reliable')
    except Exception as e:
        print(e)
        print('error: unexpected error occurd. The structure of boj pages may changed.')
