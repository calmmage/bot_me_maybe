# def register_commands(cls):
#     cls.commands = {}
#     for name in cls.__dict__:
#         if name.endswith("__command"):
#             cls.commands[name[:-9]] = getattr(cls, name)
#     return cls
#
# @register_commands
# class MyClass:
#     def set_scenario__command(self, message):
#         self.parse_scenario(message)
#         return "Scenario set. New scenario:\n" + self.show_scenario()