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
- `-s`, `--silent`: do not show progress
- `-r`, `--result`: select result of submission (default: 4)
    - `4`: '맞았습니다!'
