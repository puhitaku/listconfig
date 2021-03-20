import kconfiglib


__version__ = '0.0.1'


def value_str(sc):
    '''
    Returns the value part ('[*]', '<M>', '(foo)' etc.) of a menu entry.
    sc: Symbol or Choice.
    '''

    if sc.type in (kconfiglib.STRING, kconfiglib.INT, kconfiglib.HEX):
        return f'({sc.str_value})'

    # BOOL or TRISTATE

    # The choice mode is an upper bound on the visibility of choice symbols, so
    # we can check the choice symbols' own visibility to see if the choice is
    # in y mode
    if isinstance(sc, kconfiglib.Symbol) and sc.choice and sc.visibility == 2:
        # For choices in y mode, print '-->' next to the selected symbol
        return '-->' if sc.choice.selection is sc else '   '

    tri_val_str = (' ', 'M', '*')[sc.tri_value]

    if len(sc.assignable) == 1:
        # Pinned to a single value
        return f'-{tri_val_str}-'

    if sc.type == kconfiglib.BOOL:
        return f'[{tri_val_str}]'

    if sc.type == kconfiglib.TRISTATE:
        if sc.assignable == (1, 2):
            # m and y available
            return f'{{{tri_val_str}}}'
        return f'<{tri_val_str}>'


def node2str(node):
    prompt, cond = node.prompt
    if not kconfiglib.expr_value(cond):
        return None

    if node.item == kconfiglib.MENU:
        return f'[{prompt}]'

    if node.item == kconfiglib.COMMENT:
        return f'*** {prompt} ***'

    # Now node.item is a symbol or a choice
    if node.item.type == kconfiglib.UNKNOWN:
        return None

    res = f'{value_str(node.item):3} {prompt}'

    if node.item.name is not None:
        res += f' ({node.item.name})'

    return res


def dig(node, indent):
    count = 0

    while node:
        if node.prompt:
            s = node2str(node)
            if s is not None:
                count += 1
                print('  ' * indent + s)

        if node.list:
            if count == 0:
                dig(node.list, indent)
            else:
                dig(node.list, indent + 1)

        node = node.next

