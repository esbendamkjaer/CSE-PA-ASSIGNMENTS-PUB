from tree_sitter import Language, Parser
from os import path

def build():
    Language.build_library(
        'build/languages.so',
        [
            'libs/tree-sitter-java',
        ]
    )

def parse():
    JAVA_LANGUAGE = Language('build/languages.so', 'java')
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)

    return parser

if not path.exists('build/languages.so'):
    build()

# Parse
parser = parse()
