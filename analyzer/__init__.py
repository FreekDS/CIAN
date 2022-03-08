import argparse
from analyzer.config import PROVIDERS


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
parser.add_argument('-p', '--default-provider', default='github', type=provider_type,
                    help=f'Default provider. Allowed values are {PROVIDERS}')
parser.add_argument('-do', '--detect-only', action=argparse.BooleanOptionalAction,
                    help='Only detect CI tools in the specified repositories')
