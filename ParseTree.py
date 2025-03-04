from typing import Tuple, Optional, Iterable


def double_quote(word: str):
    return '"%s"' % word.replace('\\', '\\\\').replace('"', r'\"')


class ParseTree:
    def __init__(self, name: str, children: Iterable['ParseTree'] = None, data: str = None):
        self.name: str = name
        self.children: Optional[Tuple[ParseTree]] = tuple(children) if children else None
        self.data: Optional[str] = data

    def __repr__(self, depth: int = 0):
        pad = ' ' * (4 * depth)
        if self.data:
            if self.name == self.data:
                return f'<leaf name={double_quote(self.name)}>'
            else:
                return f'<leaf name={double_quote(self.name)} data={double_quote(self.data)}>'
        elif self.children:
            data = f'<tree name={double_quote(self.name)}>\n'
            for child in self.children:
                if isinstance(child, ParseTree):
                    data += f'{pad}    {child.__repr__(depth=depth + 1)}\n'
                else:
                    data += f'{pad}{child}\n'
            data += f'{pad}</tree>'
            return data
        else:
            return f'<leaf name={double_quote(self.name)}>'
