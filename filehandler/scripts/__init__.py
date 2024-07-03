# scripts.py
from .test.test import process_file
from .compile.complile_flip700 import compile_flip700
from .compile.complile_yemk import compile_yemk
from .compile.complile_phl import compile_phl
from .compile.complile_live import compile_live
from .concatinate.analysis_concatinator import concatenate_analysis

available_scripts = {
    'test': process_file,
    'compile_flip700': compile_flip700,
    'compile_yemk': compile_yemk,
    'compile_phl': compile_phl,
    'compile_live': compile_live,
    'concatenate_analysis': concatenate_analysis
}