# scripts.py
from .test import process_file
from .complile_flip700 import compile_flip700
from .complile_yemk import compile_yemk
from .complile_phl import compile_phl
from .complile_live import compile_live

available_scripts = {
    'test': process_file,
    'compile_flip700': compile_flip700,
    'compile_yemk': compile_yemk,
    'compile_phl': compile_phl,
    'compile_live': compile_live,
}