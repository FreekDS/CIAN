import argparse
import os

from dotenv import load_dotenv
from analyzer.Repository.GithubRepo import GithubRepo
from analyzer.CIDetector import detect_ci_tools
from analyzer.BuildCollector import collect_builds

PROVIDERS = [
    'github',
    'gh'
]


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


parser = argparse.ArgumentParser()
parser.add_argument('repository_slugs', nargs='+', type=repository_slug_type,
                    help='One or more repository slugs. A slug is constructed as follows:'
                         '[{provider}/]{username}/{repository_name}'
                         'The provider is optional. If none is given, the default provider is assumed (see -p)')
parser.add_argument('-p', '---default-provider', default='github', type=provider_type,
                    help=f'Default provider. Allowed values are {PROVIDERS}')

if __name__ == '__main__':
    load_dotenv()
    GithubRepo.init_github_token(os.getenv('GH_TOKEN'))

    args = parser.parse_args()

    repositories = []

    # Create actual Repository objects
    for r in args.repository_slugs:
        split = r.split('/')

        has_provider = len(split) > 2

        provider = split[0] if has_provider else args.default_provider
        slug = '/'.join(split[1:]) if has_provider else r

        print(slug, provider)

        if provider in ['gh', 'github']:
            repositories.append(GithubRepo(slug))

    for repo in repositories:
        print("Collecting data...\r", end='', flush=True)

        detected = detect_ci_tools(repo)
        builds = collect_builds(repo)

        print(repo.path, "CI summary")
        print("Detected CI tools:", detected)
        print(f"Detected {len(builds)} builds of various tools")
