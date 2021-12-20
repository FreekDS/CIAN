import json
from typing import Any

from analyzer.utils.OutputCommand import OutputCommand


class JsonOutput(OutputCommand):

    def __init__(self, analysis_results=None) -> None:
        super(JsonOutput, self).__init__('json', analysis_results)

    def execute(self, repo_name, filename='output.json', indent=2, **kwargs) -> Any:
        out_dict = {
            'repo': repo_name,
            'analysis': self.analysis_results
        }
        formatted_json = json.dumps(out_dict, indent=indent)
        if kwargs.get('skip', False) is False:
            print('writing output to', filename, '...', end=' ')
            with open(filename, 'w') as f:
                f.write(formatted_json)
            print('done')
        return formatted_json
