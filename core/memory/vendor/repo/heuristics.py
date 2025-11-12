import re, json, pathlib

class Heuristics:
    def __init__(self, policy_path='config/policies.json'):
        p = pathlib.Path(policy_path)
        self.conf = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}

    def check_blockers(self, data: str):
        if not isinstance(data, str):
            return (False, '')
        s = data
        for rule in self.conf.get('immutable_rules', []):
            if rule.get('type') == 'regex_block':
                if re.search(rule.get('value', ''), s):
                    return (True, rule.get('reason', 'blocked'))
        return (False, '')
