import json

from dotenv import load_dotenv
from analyzer.Repository.GithubRepo import GithubRepo
from analyzer.CIDetector import detect_ci_tools
from analyzer.BuildCollector import collect_builds
from analyzer.config import GH_PROVIDERS
from analyzer.AntiPatterns import find_anti_patterns
from analyzer.Output import create_images
from analyzer import parser


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

    for repo in repositories:
        # print("Collecting data...\r", end='', flush=True)

        print("detecting... ", end='')
        detected = detect_ci_tools(repo)
        print("Done")

        print("collecting...", end='')
        builds = collect_builds(repo)
        print("Done")

        print("gather branch info...", end='')
        branch_info = repo.branch_information()

        print("Detecting antipatterns... ", end='')
        anti_patterns = find_anti_patterns(builds, branch_info)
        print("Done")

        print(repo.path, "CI summary")
        print("Detected CI tools:", detected)
        print(f"Detected {len(builds)} builds of various tools")

        print("Anti patterns info:\n", json.dumps(anti_patterns, indent=2))

        create_images(anti_patterns, repo)

        # print(json.dumps(analyse_builds(builds), indent=4))
