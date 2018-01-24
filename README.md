# BOJ-backup

Backup your [BOJ](https://www.acmicpc.net) submission codes!

# How to use

```sh
git clone git@github.com:Jhuni0123/BOJ-backup.git
cd BOJ-backup
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

python3 backup.py # --help
```

### options
- `-l`, `--limit`: limit the number of codes to backup from recent code
- `-r`, `--result`: select result of submission (default: 4)
    - `-1`: 모든 결과
    - `4`: 맞았습니다!!
    - `5`: 출력 형식
    - `6`: 틀렸습니다
    - `7`: 시간 초과
    - `8`: 메모리 초과
    - `9`: 출력 초과
    - `10`: 런타임 에러
    - `11`: 컴파일 에러
