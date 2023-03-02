from typing import List


class CommandDescription:
    def __init__(self, name: str, doc: str, shortcuts: List[str], func: callable):
        self.name = name
        self.doc = doc
        self.shortcuts = shortcuts
        self.func = func

    @classmethod
    def from_func(cls, func: callable, suffix="__command"):
        name = func.__name__[len(suffix):] if func.__name__.endswith(suffix) else func.__name__
        doc = func.__doc__
        shortcuts = func.shortcuts if hasattr(func, "shortcuts") else []
        return cls(name, doc, shortcuts, func)


if __name__ == '__main__':
    # option 1: creating a command description explicitly
    command1 = CommandDescription("name", "doc", ["shortcuts"], lambda: None)
    name = "dummy_command"
    doc = "dummy doc"
    shortcuts = ["dummy_shortcut"]
    func = lambda: "dummy func"
    command2 = CommandDescription(name, doc, shortcuts, func)

    # option 2: from a func, using a decorator
    def dummy__command():
        """dummy doc"""
        return "dummy func"


    command3 = CommandDescription.from_func(dummy__command)
