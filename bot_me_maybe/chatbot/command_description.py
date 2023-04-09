from typing import List


class CommandDescription:
    def __init__(self, name: str, func: callable, doc: str = None, shortcuts: List[str] = None):
        self.name = name
        self.doc = (doc or "").strip()
        self.shortcuts = shortcuts or []
        self.func = func

    @classmethod
    def from_func(cls, func: callable, suffix="__command"):
        name = func.__name__[len(suffix):] if func.__name__.endswith(suffix) else func.__name__
        doc = func.__doc__
        shortcuts = func.shortcuts if hasattr(func, "shortcuts") else []
        return cls(name=name, func=func, doc=doc, shortcuts=shortcuts)


def command(shortcuts=None):
    def command_decorator(func):
        func.is_command = True
        func.shortcuts = shortcuts
        return func

    return command_decorator


def register_commands(suffix='__command'):
    """Class decorator, that register all commands in the class
    method is considered a command if it ends with suffix (default: __command)
    or has attribute is_command (added by @command() decorator)
    """

    def register_commands_decorator(cls):
        cls.commands = {}
        for name in cls.__dict__:
            func = getattr(cls, name)
            if (not hasattr(func, 'is_command') and name.endswith(suffix)) or (
                    hasattr(func, 'is_command') and func.is_command):
                key = name[:len(suffix)] if name.endswith(suffix) else name
                cls.commands[key] = name
        return cls

    return register_commands_decorator


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
