import lib
from lark import Lark, Transformer, v_args

grammar = r"""
    start: expr ("=" INT)?           -> eq

    expr: factor ("*" factor)*          -> chain

    factor: INT "^" INT           -> power
          | INT                      -> number

    %import common.INT
    %import common.WS
    %ignore WS
"""


@v_args(inline=True)
class CalcTransformer(Transformer):
    def number(self, n):
        n = int(n)
        if not lib.is_prime(n):
            raise ValueError(f"{n} is not a prime number")
        return n

    def power(self, base, exp):
        base = int(base)
        exp = int(exp)
        if not lib.is_prime(base) or not lib.is_prime(exp):
            raise ValueError(f"Base {base} or exponent {exp} must be prime numbers")
        return base**exp

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
