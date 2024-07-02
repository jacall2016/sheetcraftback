from .complile_flip700 import compile_flip700
from .test import process_file

available_scripts = {
    'test': process_file,
    'compile_flip700': compile_flip700,
    # Add other scripts here as needed
}