from RadwanORM.orm import Fields
from datetime import datetime

class Todo :
    text = Fields.String(max_len=300)
    created_at = Fields.String()
    is_done = Fields.Bool(default=False)

