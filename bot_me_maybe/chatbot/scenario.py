# get a scenario from telegram and parse it into an object
SCENARIO_TOKEN = '/scenario'

# parse scenario
import re

new_item = re.compile(r'^ *(-.*)\n?', re.MULTILINE)


def parse_scenario(scenario_str):
    first_line, scenario_str = scenario_str.split('\n', 1)
    if first_line.startswith('/'):
        first_line = first_line.split(maxsplit=1)[1]
    goal = first_line.strip() or None

    # split into items
    scenario_list = []
    match = new_item.search(scenario_str)
    while match:
        location = match.start(1)
        item = scenario_str[:location].strip()
        scenario_str = scenario_str[location + 1:].strip()
        if item:
            scenario_list.append(item)
        match = new_item.search(scenario_str)
    scenario_list.append(scenario_str)
    return {'goal': goal, 'stages': scenario_list}


class Scenario:
    def __init__(self, stages, goal=None):
        self.stages = stages
        self.goal = goal
        self.stage = 0
        self.finished = False

    def next_stage(self):
        if self.stage < len(self.stages) - 1:
            self.stage += 1
        else:
            self.finished = True

    def previous_stage(self):
        if self.stage > 0:
            self.stage -= 1
        else:
            raise ValueError('Already at the first stage')

    def __str__(self):
        return f"""Scenario:
    stage: {self.stage}
    finished: {self.finished}
    """

    def get_stage(self, index):
        return self.stages[index]

    def get_stages(self):
        return tuple(self.stages)

    def update_goal(self, goal):
        self.goal = goal

    def describe(self):
        res = ""
        if self.goal:
            res += f"Goal: {self.goal}\n"
        # todo: enumerate instead?
        # res += '- ' + '\n- '.join(self.get_stages())
        for i, stage in enumerate(self.get_stages()):
            res += f"{i}) {stage}\n"
        return res

    @classmethod
    def from_string(cls, scenario_str):
        scenario_list = parse_scenario(scenario_str)
        return cls(scenario_list)


if __name__ == '__main__':
    sample_telegram_message = f"""{SCENARIO_TOKEN} Do a thing!
    - asd
    blah
    - asd
     - asd
    - asdb
    -asd
     -argtb
    """
    scenario_list = parse_scenario(sample_telegram_message)
    print(scenario_list)
    # initialise stage

    # Option 1: create a scenario from a list of stages
    scenario = Scenario(scenario_list)

    # Option 2: create a scenario from a string

