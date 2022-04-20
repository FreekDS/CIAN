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

# ANTI-PATTERNS

SLOW_BUILD = 'slow_build'
BROKEN_RELEASE = 'broken_release'
LATE_MERGING = 'late_merging'
SKIP_FAILING_TESTS = 'skip_failing_tests'
ANTI_PATTERNS = [SLOW_BUILD, BROKEN_RELEASE, LATE_MERGING, SKIP_FAILING_TESTS]
