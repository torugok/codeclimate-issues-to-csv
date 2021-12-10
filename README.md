# Codeclimate Issues to CSV

## Install deps (poetry required)

```sh
poetry install
```

## Run script

```sh
python ./app/codeclimate-issues.py -t <your-codeclimate-token> -r <your-codeclimate-repository-id> -o <you-file.csv>
```

## TODO
- [ ] use multiple asyncio tasks (ratelimit?)
- [ ] convert project to setuptools
