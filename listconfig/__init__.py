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
        return ' ->' if sc.choice.selection is sc else '   '

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
        return None, None

    if node.item == kconfiglib.MENU:
        return f'[{prompt}]', None

    if node.item == kconfiglib.COMMENT:
        return f'*** {prompt} ***', None

    # Now node.item is a symbol or a choice
    if node.item.type == kconfiglib.UNKNOWN:
        return None, None

    res = f'{value_str(node.item):3} {prompt}'

    if node.item.name is not None:
        res += f' ({node.item.name})'

    if hasattr(node, 'help') and node.help is not None:
        lines = [l for l in node.help.split('\n') if l.strip()]
        l = lines[0]
        if len(lines) == 2:
            l += f' {lines[1]}'
        elif len(lines) > 2:
            l += f' {lines[1]} ...'
        return res, l

    return res, None


def dig(node, indent):
    lines = []
    count = 0

    while node:
        if node.prompt:
            s, help = node2str(node)
            if s is not None and not s.startswith('*** Compiler:'):
                count += 1
                lines.append(('  ' * indent + s, help))
                # print('  ' * indent + s)

        if node.list:
            if count == 0:
                lines += dig(node.list, indent)
            else:
                lines += dig(node.list, indent + 1)

        node = node.next

    return lines


def print_tree(node):
    lines = dig(node, 0)
    longest = max(len(t[0]) for t in lines)
    
    for t in lines:
        print(t[0] + ' ' * (longest - len(t[0])), end=' ')
        if t[1] is None:
            print()
        else:
            print(t[1])

