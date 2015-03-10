from pony.orm import PrimaryKey, Required, Set
from Todo import db



class Todo(db.Entity):

    text = Required(unicode)
    tags = Set("Tag")

class Tag(db.Entity):

    name = Required(unicode, unique=True)
    tags = Set("Todo")