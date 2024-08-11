# Help me finish the code:
# please only code one mixin at a time
# For each mixin ask what I want it to do and which libraries to use, which args / kwargs to accept
# I want the settings to be loaded on init. using python-dotenv. And also just from the env if they were present there
# 2) I want the App to work similarly with Settings, with Toml config and with
# I have this Idea: there will be a dotdict / namedtuple "settings"
# 3) I want an easy way for the developers to specify which field the .env / config should include. and maybe types of those optionally.
# Should it be a Config dataclass? With pydantic? With mongoengine?
# Probably a good idea. How do usually people do this? pydantic is good because we'll able to integrate it with FastAPI as well..
# 4) App should have a .name value and all the .env names should start with it - capitalized
#
