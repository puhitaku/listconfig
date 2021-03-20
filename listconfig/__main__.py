import os
import re

import click
import click_pathlib
import kconfiglib

from listconfig import dig


@click.command()
@click.argument('kconfig_path', type=click_pathlib.Path(exists=True))
@click.argument('dotconfig_path', type=click_pathlib.Path(exists=True))
@click.option('--arch', default=None)
def main(kconfig_path, dotconfig_path, arch):
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

    kconfig = kconfiglib.Kconfig(str(kconfig_path))

    if not dotconfig_path.is_file():
        print(f'Specified .config path {dotconfig_path} is not a file', file=sys.stderr)

    kconfig.load_config(str(dotconfig_path))
    dig(kconfig.top_node.list, 0)


main()
