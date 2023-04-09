from dataclasses import dataclass
from bmmb.data.database.config import Configuration, create_database


@dataclass
class User:
    id: str
    name: str
    age: int


config_path = "sample_config.toml"
config = Configuration(config_path)
db = create_database(config)

users_table_name = "users"

# Register the User model with the database
db.register_model(users_table_name, User)

# Get a Table instance for users
users = db.get_table(users_table_name)

# Put a user in the table
users.put("user1", User(id="user1", name="Alice", age=30))

# Get a user from the table
user = users.get("user1")
print(user)

# Edit a user
users.edit("user1", User(id="user1", name="Alice", age=31))

# Delete a user
users.delete("user1")
