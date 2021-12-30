# CI TOOLS

CIRCLE_CI = "CircleCI"
GH_ACTIONS = "Github Actions"
TRAVIS_CI = "TravisCI"

CI_TOOLS = [GH_ACTIONS, TRAVIS_CI, CIRCLE_CI]

# GITHUB CONFIG

GH_PROVIDERS = ['github', 'gh']
GH_SKIP_JOBS = ['Set up job', r'Run actions/.+@v\d+', r'Post Run actions/.+@v\d+', 'Complete job']

# GENERAL

PROVIDERS = [*GH_PROVIDERS]
