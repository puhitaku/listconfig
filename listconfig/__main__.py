import os
import re
import sys
from contextlib import contextmanager

import click
import click_pathlib
import kconfiglib

from listconfig import print_tree


@contextmanager
def quietify(verbose):
    if verbose:
        yield None
        return

    try:
        with open(os.devnull, 'w') as devnull:
            sys.stderr = devnull
            yield None
    finally:
        sys.stderr = sys.__stderr__


@click.command()
@click.argument('kconfig_path', type=click_pathlib.Path(exists=True))
@click.argument('dotconfig_path', type=click_pathlib.Path(exists=True))
@click.option('--arch', default=None, help='ARCH in Linux kernel. Inferred by default.')
@click.option('--help-lines', '-l', default=2, help='Number of lines to pick from a config help.')
@click.option('--verbose', '-v', is_flag=True, help='Enable warnings during Kconfig analysis.')
def main(kconfig_path, dotconfig_path, arch, help_lines, verbose):
    if not kconfig_path.is_file():
        print(f'Specified Kconfig path {kconfig_path} is not a file', file=sys.stderr)
        return sys.exit(1)

    ksrc = kconfig_path.parent

    if 'srctree' not in os.environ:
        os.environ['srctree'] = str(ksrc)

    if 'CC' not in os.environ:
        os.environ['CC'] = 'gcc'

    if arch is None:
        r = re.compile('Linux/([^ ]+) ')
        with open(dotconfig_path, 'r') as f:
            detected = None

            for l in f.readlines()[:5]:
                res = r.search(l)
                if res is None:
                    continue
                detected = res.groups()[0]

            if detected is None:
                print('Specified .config has no expected header', file=sys.stderr)
                print('Please specify --arch={arch} manually', file=sys.stderr)
                sys.exit(1)

            arch = detected

    if 'SRCARCH' not in os.environ:
        os.environ['SRCARCH'] = os.environ.get('ARCH', arch)

    with quietify(verbose):
        kconfig = kconfiglib.Kconfig(str(kconfig_path))

    if not dotconfig_path.is_file():
        print(f'Specified .config path {dotconfig_path} is not a file', file=sys.stderr)

    with quietify(verbose):
        kconfig.load_config(str(dotconfig_path))

    print_tree(kconfig.top_node.list, help_lines)


main()
