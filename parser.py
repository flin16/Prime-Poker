from lark import Lark, Transformer, v_args

grammar = r"""
    start: expr ("=" NUMBER)?           -> eq

    expr: factor ("*" factor)*          -> chain

    factor: NUMBER "^" NUMBER           -> power
          | NUMBER                      -> number

    %import common.NUMBER
    %import common.WS
    %ignore WS
"""


@v_args(inline=True)
class CalcTransformer(Transformer):
    def number(self, n):
        return float(n)

    def power(self, base, exp):
        return float(base) ** float(exp)

    def chain(self, first, *factors):
        result = first
        for f in factors:
            result *= f
        return result

    def eq(self, value, expected=None):
        if expected is None:
            return value
        else:
            return value == float(expected)


if __name__ == "__main__":
    parser = Lark(grammar, parser="lalr", transformer=CalcTransformer())

    examples = [
        "2 * 3 * 4",  # 24
        "2 ^ 3",  # 8
        "2 ^ 3 * 5",  # 40
        "2 * 3 ^ 2",  # 18 ✅
        "2 ^ 3 * 3 * 5 = 120",  # True
        "2 * 3 ^ 2 = 18",  # True
        "2 ^ 3 ^ 2",  # ❌ 幂嵌套不合法
    ]

    for ex in examples:
        try:
            result = parser.parse(ex)
            print(f"{ex:25} => {result}")
        except Exception as e:
            print(f"{ex:25} => ❌ Error: {e}")
