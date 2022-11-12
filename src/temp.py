# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pathlib import Path


def parse_path(path_str: str) -> str:
    return str(Path(path_str))

    
print("DEBUG")

print(str(parse_path('./assets/chest_osrs.png')))