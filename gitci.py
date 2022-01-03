import os
import json

from dotenv import load_dotenv
from analyzer.Repository.GithubRepo import GithubRepo
from analyzer.CIDetector import detect_ci_tools
from analyzer.BuildCollector import collect_builds
from analyzer.Analysis import analyse_builds
from analyzer import parser
from analyzer.config import GH_PROVIDERS


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

        if provider in GH_PROVIDERS:
            repositories.append(GithubRepo(slug))

    for repo in repositories:
        # print("Collecting data...\r", end='', flush=True)

        print("detecting...")
        detected = detect_ci_tools(repo)

        print("collecting...")
        builds = collect_builds(repo)

        print(repo.path, "CI summary")
        print("Detected CI tools:", detected)
        print(f"Detected {len(builds)} builds of various tools")

        print(json.dumps(analyse_builds(builds), indent=4))
