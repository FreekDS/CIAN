# Git CI Analyzer 
[![Git Analyzer CI](https://github.com/FreekDS/git-ci-analyzer/actions/workflows/ci-main.yml/badge.svg)](https://github.com/FreekDS/git-ci-analyzer/actions/workflows/ci-main.yml) [![Circle CI](https://circleci.com/gh/FreekDS/git-ci-analyzer.svg?style=svg)](https://app.circleci.com/pipelines/github/FreekDS/git-ci-analyzer)

> A command line tool to analyze CI workflows in git repositories written in Python 3.10.

---

The goal for this project is to create a command line tool that is capable of analyzing CI implementations in Git repositories.
For the time being, the tool is capable of analyzing TravisCI builds and GitHub Actions builds. 
CircleCI is implemented partially.

By default, JSON output will be generated that contains useful information such as the amount of failing builds, 
the amount of successful builds, the average duration of each build...

## Installation
In order to install this tool, you have to follow the next steps
1. Clone this repository to your local machine <br>
   ```shell
   git clone https://github.com/FreekDS/git-ci-analyzer.git
    ```
2. Go to the cloned directory
    ```shell
   cd git-ci-analyzer/
   ```
3. Install the required dependencies
    ```shell
   pip install -r requirements.txt
   ```

### Requirements
In order to be able to install everything, make sure the following is installed on your machine
1. Python 3.10 (this is the Python version where the tool is written in, it might also work with lower Python versions)
2. pip
3. To access private repositories, and to have a higher rate limit, the following environment variables should be set
   > GH_TOKEN=<your_github_token> <br>
   > CIRCLE_CI=<your_circleci_token> <br>
   > TRAVIS_CI=<your_travis_token>
   
   They can be set by creating a ```.env``` file. This file is loaded automatically.<br>
   It is advised to set at least the `GH_TOKEN` as this increases the rate limit for the GitHub API signifcantly.

## Usage
To view the usage of the tool, run
````shell
python gitci.py -h
````

There is only one required argument: the repository slugs.
A slug describes the repository you want to analyze.
It is formatted as follows
> [{provider}/]{username}/{repository_name}

The provider argument in this slug is optional. By default, the default provider is used (GitHub, see option `-p`)
For example, the slugs that point to this repository are the following

> FreekDS/git-ci-analyzer <br>
> gh/FreekDS/git-ci-analyzer <br>
> github/FreekDS/git-ci-analyzer <br>

Multiple slugs can be passed in at once. The slugs should be separated by a space.

The default provider can be specified using the optional `-p` argument.
For the moment, the allowed `-p` values are `github` and `gh`.

### Examples

`````shell
python gitci.py FreekDS/git-ci-analyzer
python gitci.py gh/FreekDS/git-ci-analyzer godotengine/godot
python gitci.py FreekDS/git-ci-analyzer -p github
`````

## Features
At the moment, the following features are present:
1. Detect which CI tools are implemented in a repository.
2. Perform basic analysis
   1. Total build count
   2. Amount of successful builds
   3. Amount of failing builds
   4. Average build duration
   5. Amount of builds per event that triggered it
   6. Information on builds for each CI tool separated
3. Output to JSON


## Tests
Tests are located in the `tests/` folder.
They are pytest based and can be executed with
````shell
pytest .
````

## License

This repository is MIT licensed.
See the [LICENSE](./LICENSE) file for more information.
