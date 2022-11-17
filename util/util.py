from typing import Any
def get_setting(val: str, param: dict) -> Any | None:
    if val in param:
        return param[val]
    else:
        return None

    
