import argparse
import datetime

from analyzer.AntiPatterns import find_anti_patterns
from analyzer.config import PROVIDERS, ANTI_PATTERNS
from analyzer.CIDetector import detect_ci_tools
from analyzer.BuildCollector import collect_builds
from analyzer.Output import create_json, create_text_files, create_images
from analyzer.utils import format_date_str
from time import time


# ARGUMENT PARSER

def repository_slug_type(arg):
    parsed = arg.split('/')
    provider_included = len(parsed) > 2

    # provider is included in slug
    if provider_included:
        known_provider = parsed[0] in PROVIDERS
    else:
        known_provider = True

    if known_provider and len(parsed) >= 2:
        return arg
    else:
        raise argparse.ArgumentTypeError(
            f"Unknown provider '{parsed[0]}'" if known_provider else f"Invalid slug '{arg}'"
        )


def provider_type(p):
    if p in PROVIDERS:
        return p
    raise argparse.ArgumentTypeError(
        f"Unknown provider type '{p}' allowed values are '{PROVIDERS}'"
    )


def antipattern_type(a):
    if a in ANTI_PATTERNS:
        return a
    raise argparse.ArgumentTypeError(
        f"Unknown anti-pattern '{a}', allowed values are '{ANTI_PATTERNS}'"
    )


def start_date_type(d):
    try:
        d = datetime.datetime.strptime("%Y-%m-%d", d)
        return format_date_str(d)
    except TypeError:
        print(f"'{d}' is not in the format YYYY-MM-DD, using no date instead...")
        return None


parser = argparse.ArgumentParser()
parser.add_argument('repository_slugs', nargs='+', type=repository_slug_type,
                    help='One or more repository slugs. A slug is constructed as follows:'
                         '[{provider}/]{username}/{repository_name}'
                         'The provider is optional. If none is given, the default provider is assumed (see -p)')
parser.add_argument('-p', '--default-provider', default='github', type=provider_type,
                    help=f'Default provider. Allowed values are {PROVIDERS}')
parser.add_argument('-do', '--detect-only', action=argparse.BooleanOptionalAction, default=False,
                    help='Only detect CI tools in the specified repositories')
parser.add_argument('-a', '--anti-patterns', nargs='+', type=antipattern_type,
                    help=f'Select anti-patterns to detect, allowed values are {ANTI_PATTERNS}')
parser.add_argument('-nc', '--no-cache', action=argparse.BooleanOptionalAction, default=False,
                    help='Use this flag to disable cache usage')
parser.add_argument('-ncc', '--no-create-cache', action=argparse.BooleanOptionalAction, default=False,
                    help='Use this flag to disable cache creation')
parser.add_argument('-od', '--out-dir', type=str, help='Output path')
parser.add_argument('-v', '--verbose', action=argparse.BooleanOptionalAction, default=False,
                    help='Provide more information in console')
parser.add_argument('-d', '--start-date', type=start_date_type,
                    help='Date to start collecting data from, if none is provided, the latest three months are '
                         'collected')


# GENERAL FUNCTIONS

def analyze_repo(
        repo,
        anti_patterns=None,
        detect_only=False,
        use_cache=True,
        create_cache=True,
        verbose=False,
        out_dir=None,
        start_date=None
):
    start = time()
    print(f"===============\nStarting analysis on '{repo.path}'\n===============")
    print("Detecting CI...", end='') if verbose else None
    detected = detect_ci_tools(repo, use_cache, create_cache)
    print(f"Done ({round(time() - start, 2)}s)") if verbose else None

    if detect_only:
        print("Detected CI tools: ", detected)
        print(f"==== DONE, TOOK {round(time() - start, 2)}s ====\n")
        return detected

    print("Collecting builds...", end='') if verbose else None
    builds = collect_builds(repo, use_cache, create_cache, start_date)
    print(f"Done ({round(time() - start, 2)}s)") if verbose else None

    print("Gathering branch information...", end='') if verbose else None
    branch_info = repo.branch_information(use_cache, create_cache)
    default_branch = repo.default_branch
    print(f"Done ({round(time() - start, 2)}s)") if verbose else None

    print("Analyzing anti-patterns...", end='') if verbose else None
    anti_patterns = find_anti_patterns(builds, branch_info, default_branch, restriction=anti_patterns)
    print(f"Done ({round(time() - start, 2)}s)") if verbose else None

    print("Creating output files...", end='') if verbose else None
    if out_dir:
        create_images(anti_patterns, repo, out_dir)
        create_json(anti_patterns, repo, out_dir)
        create_text_files(anti_patterns, repo, out_dir)
    else:
        create_images(anti_patterns, repo)
        create_json(anti_patterns, repo)
        create_text_files(anti_patterns, repo)
    print(f"Done ({round(time() - start, 2)}s)") if verbose else None

    print(f"==== DONE, TOOK {round(time() - start, 2)}s ====\n")
    return detected, anti_patterns, branch_info, default_branch
