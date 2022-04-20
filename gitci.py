from dotenv import load_dotenv
from analyzer.Repository.GithubRepo import GithubRepo
from analyzer.config import GH_PROVIDERS
from analyzer import parser, analyze_repo


if __name__ == '__main__':
    load_dotenv()

    args = parser.parse_args()

    repositories = []

    # Create actual Repository objects
    for r in args.repository_slugs:
        split = r.split('/')

        has_provider = len(split) > 2

        provider = split[0] if has_provider else args.default_provider
        slug = '/'.join(split[1:]) if has_provider else r

        if provider in GH_PROVIDERS:
            repositories.append(GithubRepo(slug))

    opts = {
        'detect_only': args.detect_only,
        'anti_patterns': args.anti_patterns,
        'use_cache': not args.no_cache,
        'create_cache': not args.no_create_cache,
        'out_dir': args.out_dir,
        'verbose': args.verbose,
        'start_date': args.start_date
    }

    for repo in repositories:
        results = analyze_repo(repo, **opts)
        print()
