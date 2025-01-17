class FuncExpr:
    func_name = 'UNKNOWN'
    func_args = tuple()

    def __str__(self):
        args_list = ','.join(self.func_args)
        return f'={self.func_name}({args_list})'


class SumExpr(FuncExpr):
    func_name = 'sum'

    def __init__(self, *args):
        self.func_args = args


def xl_sum(start, end):
    return SumExpr(f'{start}:{end}')
