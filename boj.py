import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode


class BOJ:
    host = 'www.acmicpc.net'

    @staticmethod
    def url(path):
        return 'https://' + BOJ.host + path

    def __init__(self):
        self.session = requests.Session()
        self.user_id = None

    def login(self, login_id, password):
        # try to login
        data = {'login_user_id': login_id, 'login_password': password}
        self.session.post(BOJ.url('/signin'), data=data)

        # check login by get user_id
        r = self.session.get(BOJ.url('/'))
        soup = BeautifulSoup(r.text, 'html5lib')
        tag = soup.find('a', class_='username')
        if tag is None:
            return False
        else:
            self.user_id = tag.text
            return True

    def get_submission_list(self, result_id=None, limit=None):
        params = {'user_id': self.user_id}
        if result_id is not None:
            params['result_id'] = result_id

        next = '/status/?' + urlencode(params)

        lim_str = '?'
        if limit is not None:
            lim_str = str(limit)

        submissions = []

        def prompt_process():
            print('\rCollecting submission list (%d/%s)' % (len(submissions), lim_str), end='')

        while next:
            prompt_process()
            r = self.session.get(BOJ.url(next))
            soup = BeautifulSoup(r.text, 'html5lib')

            table_body = soup.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                submissions.append({'submission_id': cols[0].text.strip(), 'problem_id': cols[2].text.strip()})
                if len(submissions) == limit:
                    break
            if len(submissions) == limit:
                break

            next_tag = soup.find('a', id='next_page')
            if next_tag is None:
                next = None
            else:
                next = next_tag.get('href')
        prompt_process()
        print('..Done!')
        return submissions

    def get_submission_info(self, submission_id):
        url = BOJ.url('/source/' + submission_id)
        r = self.session.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        sourcecode = soup.find('textarea', id='source').text

        lang_id = int(soup.find('input', id='language').get('value'))
        tds = soup.find('tbody').tr.find_all('td')
        problem_id = tds[2].text.strip()
        lang = tds[7].text.strip()

        return {'problem_id': problem_id, 'sourcecode': sourcecode, 'lang': lang, 'ext': BOJ.lang_to_ext(lang_id)}

    @staticmethod
    def lang_to_ext(lang):
        if lang == 0 or lang == 59 or lang == 75 or lang == 77:
            return "c"
        elif lang == 1 or lang == 41 or lang == 49 or lang == 60 or lang == 88 or \
                lang == 66 or lang == 67 or lang == 84 or lang == 85:
            return "cpp"
        elif lang == 3:
            return "java"
        elif lang == 9 or lang == 62:
            return "cs"
        elif lang == 4 or lang == 65 or lang == 68:
            return "rb"
        elif lang == 8 or lang == 42:
            return "pl"
        elif lang == 6 or lang == 28 or lang == 32 or lang == 73:
            return "py"
        elif lang == 5:
            return "sh"
        elif lang == 17 or lang == 34 or lang == 38:
            return "js"
        elif lang == 22:
            return "ml"
        elif lang == 44:
            return "rs"
        elif lang == 12:
            return "go"
        elif lang == 16:
            return "lua"
        elif lang == 27:
            return "asm"
        elif lang == 72:
            return "R"
        else:
            return "txt"
