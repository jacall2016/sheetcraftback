# scripts.py
from .test import process_file
from .complile_flip700 import compile_flip700

available_scripts = {
    'test': process_file,
    'compile_flip700': compile_flip700,
}