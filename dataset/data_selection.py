import csv
import datetime
import os
from collections import defaultdict
from aiohttp import TCPConnector, ClientSession, ClientResponseError
import asyncio
import json
import random
from dotenv import load_dotenv
from typing import Union
from pathlib import Path
import platform

# PARAMETERS
SAMPLE_SIZE = 30
ACTIVE_DAYS_THR = 30
COLLECT_DATE = datetime.datetime(2022, 5, 5, 12, 0, 0, 0)  # Data collection date: 2022-05-05 12:00
SEED = 170819991405
DATA_FILE = "dataset_with_info.csv"
CURRENT_DIR = Path(__file__).resolve().parent

# INITIALIZATION
load_dotenv()
random.seed(SEED)  # Seed, to be reproducible
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# GITHUB TOKEN MANAGER CLASS

class TokenMgr:
    T_PTR = 0
    TOKENS = []

    def __init__(self):
        t_count = int(os.getenv('GH_TOKEN_COUNT', 0))
        tokens_l = list()
        for i in range(t_count):
            token = os.getenv(f'GH_TOKEN_{i + 1}', None)
            if token:
                tokens_l.append(token)
        self.TOKENS = tokens_l
        self.travis_token = os.getenv('TRAVIS_CI')

    def __call__(self, *args, **kwargs):
        t = self.TOKENS[self.T_PTR]
        self.T_PTR += 1
        self.T_PTR %= len(self.TOKENS)
        return t


token_mgr = TokenMgr()

# DATA PREPROCESSING

latest_commit = datetime.datetime(1, 1, 1)
with open(DATA_FILE) as f:
    cs = csv.reader(f, delimiter=';')
    next(cs)
    repos = defaultdict(list)
    for repo_url, fc, lc, ci, start, end, interval, gap, nb_gaps, max_gap_size, diff in cs:
        lc_date = datetime.datetime.strptime(lc, "%d/%m/%Y %H:%M")
        if lc_date > latest_commit:
            latest_commit = lc_date
        repo = '/'.join(repo_url.split('/')[-2:])
        repos[repo].append(
            {
                'first_commit': fc,
                'last_commit': lc,
                'start': start,
                'end': end,
                'ci': ci
            }
        )
    repos = dict(repos)

repos_with_change = {k: v for k, v in repos.items() if len(v) == 2 and v[0]['ci'] != v[1]['ci']}

new_r = dict()
for repo, entries in repos_with_change.items():
    end1 = entries[0]["end"]
    end2 = entries[1]["end"]
    if end1 == "#NAME?" and end2 == "#NAME?":
        # Both are still active
        continue
    if end1 != "#NAME?" and end2 != "#NAME?":
        # Both are discontinued
        continue
    if end1 == "#NAME?":
        # Make sure first entry is discontinued
        entries = [entries[1], entries[0]]
    assert entries[0]["end"] != "#NAME?" and entries[1]["end"] == "#NAME?"
    new_r[repo] = entries

repos_with_change = new_r

travis_to_gha = {k: v for k, v in repos_with_change.items() if v[0]["ci"] == "Travis" and v[1]["ci"] == "GHA"}
gha_to_travis = {k: v for k, v in repos_with_change.items() if v[0]["ci"] == "GHA" and v[1]["ci"] == "Travis"}

# No change and has still CI (end is not known)
repos_without_change = {k: v for k, v in repos.items() if len(v) == 1 and v[0]["end"] == "#NAME?"}
repos_without_change_travis = {k: v for k, v in repos_without_change.items() if v[0]['ci'] == 'Travis'}
repos_without_change_gha = {k: v for k, v in repos_without_change.items() if v[0]['ci'] == 'GHA'}


# GITHUB API ACCESSOR METHODS

async def async_request(url, session, token) -> Union[bool or dict or list]:
    try:
        async with session.get(url, headers={
            'Authorization': f'token {token}',
            'User-Agent': 'FreekDS/git-ci-analyzer',
            'Travis-API-Version': '3'
        }) as response:
            rt = await response.read()
            if response.status == 404:
                return False
            return json.loads(rt)
    except ClientResponseError as e:
        if e.status == 404:
            return False


async def repos_info(repos, tokens):
    tasks = list()
    conn = TCPConnector(limit=20)
    async with ClientSession(connector=conn) as session:
        for r in repos:
            task = asyncio.ensure_future(
                async_request(f"https://api.github.com/repos/{r}", session, tokens())
            )
            tasks.append(task)
        return await asyncio.gather(*tasks)


# SAMPLE GHA -> TRAVIS REPOSITORIES
# there are fewer repos in this category then default sample size
# make sure the repos still exist though...
assert len(gha_to_travis) <= SAMPLE_SIZE

new_gha_to_travis = {}
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
future = asyncio.ensure_future(
    repos_info(list(gha_to_travis.keys()), token_mgr)
)
loop.run_until_complete(future)
results = future.result()

for i, (k, v) in enumerate(gha_to_travis.items()):
    if not results[i]:
        continue
    new_gha_to_travis[k] = v
gha_to_travis = new_gha_to_travis


# SAMPLE CREATION FUNCTIONS

async def is_repo_active(r, session, tokens):
    collect_date = COLLECT_DATE.strftime('%Y-%m-%dT%H:%M:%SZ')
    url = f"https://api.github.com/repos/{r}/commits?until={collect_date}&per_page=1"
    result = await async_request(url, session, tokens())
    if not result or not isinstance(result, list):
        return False
    commit = result[0]
    date = commit.get('commit', {}).get('author', {}).get('date')
    if not date:
        return False
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    days = abs((COLLECT_DATE - date).days)
    return days <= ACTIVE_DAYS_THR


async def are_repos_active(repo_names, tokens):
    tasks = list()
    conn = TCPConnector(limit=20)
    async with ClientSession(connector=conn) as session:
        for r in repo_names:
            task = asyncio.ensure_future(
                is_repo_active(r, session, tokens)
            )
            tasks.append(task)
        active_or_not = await asyncio.gather(*tasks)
    active_repos = list()
    for index, r in enumerate(repo_names):
        if active_or_not[index]:
            active_repos.append(r)
    return active_repos


def filter_active_repos(repo_names, tokens):
    a_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(a_loop)
    fu = asyncio.ensure_future(
        are_repos_active(repo_names, tokens)
    )
    a_loop.run_until_complete(fu)
    return fu.result()


def filter_has_travis_builds(repo_names, tokens):
    a_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(a_loop)
    fu = asyncio.ensure_future(
        do_repos_have_travis_builds(repo_names, tokens)
    )
    a_loop.run_until_complete(fu)
    return fu.result()


async def do_repos_have_travis_builds(repo_names, tokens):
    tasks = list()
    conn = TCPConnector(limit=20)
    async with ClientSession(connector=conn) as session:
        for r in repo_names:
            task = asyncio.ensure_future(
                repo_has_travis_builds(r, session, tokens.travis_token)
            )
            tasks.append(task)
        build_or_not = await asyncio.gather(*tasks)
    repos_with_builds = list()
    for index, r in enumerate(repo_names):
        if build_or_not[index]:
            repos_with_builds.append(r)
    return repos_with_builds


async def repo_has_travis_builds(r, session, token):
    rep = r.replace('/', '%2F')
    url = f"https://api.travis-ci.com/repo/{rep.replace('/', '%2F')}/builds?limit=1"
    r = await async_request(url, session, token)
    if r is False or not isinstance(r, dict):
        return False
    pagination_info = r.get('@pagination', {})
    if not pagination_info:
        return False
    return int(pagination_info.get('count', 0)) > 0


def create_sample(size, repos_dict, tokens, filter_travis=False):
    possible_repos = list(repos_dict.keys())

    selected = list()
    while len(selected) != size and possible_repos:
        required_count = size - len(selected)

        selected_sample = random.sample(possible_repos, min(required_count, len(possible_repos)))
        active_sample = filter_active_repos(selected_sample, tokens)
        if filter_travis:
            active_sample = filter_has_travis_builds(active_sample, tokens)
        selected += active_sample

        possible_repos = [r for r in possible_repos if r not in selected_sample]

    return {k: v for k, v in repos_dict.items() if k in selected}


# SAMPLE FROM TRAVIS -> GHA

travis_to_gha_sample = create_sample(SAMPLE_SIZE, travis_to_gha, token_mgr, filter_travis=True)

# SAMPLE FROM SINGLE CI REPOSITORIES

single_ci_repos_travis = create_sample(SAMPLE_SIZE, repos_without_change_travis, token_mgr, filter_travis=True)
single_ci_repos_gha = create_sample(SAMPLE_SIZE, repos_without_change_gha, token_mgr)


# GENERATE OUTPUT FILES (json + csv)

def write_csv(filename, data):
    with open(f"{CURRENT_DIR}/output/csv/{filename}.csv", 'w') as out_file:
        out_file.write("repo;ci;start;end\n")
        for r, vals in data.items():
            for val in vals:
                out_file.write(f"{r};{val['ci']};{val['start']};{val['end']}\n")


def write_json(filename, data):
    with open(f"{CURRENT_DIR}/output/json/{filename}.json", 'w') as out_file:
        out_file.write(json.dumps(data, indent=2))


objs = [
    ('gha_only', single_ci_repos_gha),
    ('travis_only', single_ci_repos_travis),
    ('gha_to_travis', gha_to_travis),
    ('travis_to_gha', travis_to_gha_sample)
]

for o in objs:
    write_json(*o)
    write_csv(*o)
