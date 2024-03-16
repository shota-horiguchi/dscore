

class Table(object):

    def __init__(self, rows, headers, floatfmt):
        print(rows[0])
        self.rows = [list(map(lambda x: format(x, floatfmt) if isinstance(x, float) else x, row)) for row in rows]
        self.headers = headers
        self.floatfmt = floatfmt
        self.alignfunc = ['r' if self.is_number(r) else 'l' for r in self.rows[0]]
        assert all([len(row) == len(headers) for row in self.rows]), len(headers)

    def __str__(self):
        to_print = []
        lengths = [max([len(row[i]) for row in self.rows] + [len(self.headers[i])]) for i in range(len(self.headers))]
        to_print.append(self._make_line(self.headers, lengths))
        to_print.append(self._make_line(['-' * l for l in lengths], lengths))
        for row in self.rows:
            to_print.append(self._make_line(row, lengths))
        return '\n'.join(to_print)

    def _make_line(self, row, lengths):
        return '  '.join([e.rjust(l) if func == 'r' else e.ljust(l) for e, l, func in zip(row, lengths, self.alignfunc)])
    
    @classmethod
    def is_number(cls, s):
        if s.count('.') > 1:
            return False
        if all([n.isdigit() for n in s.lstrip('-').split('.')]):
            return True
        return False


def table(rows, headers, floatfmt):
    return Table(rows, headers, floatfmt)
