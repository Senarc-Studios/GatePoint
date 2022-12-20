"""
The MIT License (MIT)

Copyright (c) 2022-present BenitzCoding

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from typing import Optional, Tuple, Dict

import argparse
import sys
from pathlib import Path

import gateway
import importlib.metadata
import aiohttp
import platform


def show_version() -> None:
    entries = []

    entries.append('- Python v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(sys.version_info))
    version_info = gateway.version_info
    entries.append('- gatepoint v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(version_info))
    if version_info.releaselevel != 'final':
        version = importlib.metadata.version('gatepoint')
        if version:
            entries.append(f'    - gatepoint metadata: v{version}')

    entries.append(f'- aiohttp v{aiohttp.__version__}')
    uname = platform.uname()
    entries.append('- system info: {0.system} {0.release} {0.version}'.format(uname))
    print('\n'.join(entries))


def core(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.version:
        show_version()
    else:
        parser.print_help()

_gitignore_template = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Our configuration files
config.py
"""

# certain file names and directory names are forbidden
# see: https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247%28v=vs.85%29.aspx
# although some of this doesn't apply to Linux, we might as well be consistent
_base_table: Dict[str, Optional[str]] = {
    '<': '-',
    '>': '-',
    ':': '-',
    '"': '-',
    # '/': '-', these are fine
    # '\\': '-',
    '|': '-',
    '?': '-',
    '*': '-',
}

# NUL (0) and 1-31 are disallowed
_base_table.update((chr(i), None) for i in range(32))

_translation_table = str.maketrans(_base_table)


def to_path(parser: argparse.ArgumentParser, name: str, *, replace_spaces: bool = False) -> Path:
    if isinstance(name, Path):
        return name

    if sys.platform == 'win32':
        forbidden = (
            'CON',
            'PRN',
            'AUX',
            'NUL',
            'COM1',
            'COM2',
            'COM3',
            'COM4',
            'COM5',
            'COM6',
            'COM7',
            'COM8',
            'COM9',
            'LPT1',
            'LPT2',
            'LPT3',
            'LPT4',
            'LPT5',
            'LPT6',
            'LPT7',
            'LPT8',
            'LPT9',
        )
        if len(name) <= 4 and name.upper() in forbidden:
            parser.error('invalid directory name given, use a different one')

    name = name.translate(_translation_table)
    if replace_spaces:
        name = name.replace(' ', '-')
    return Path(name)

def parse_args() -> Tuple[argparse.ArgumentParser, argparse.Namespace]:
    parser = argparse.ArgumentParser(prog='gatepoint', description='Tools for helping with gatepoint.')
    parser.add_argument('-v', '--version', action='store_true', help='shows the library version')
    parser.set_defaults(func=core)

    return parser, parser.parse_args()


def main() -> None:
    parser, args = parse_args()
    args.func(parser, args)


if __name__ == '__main__':
    main()