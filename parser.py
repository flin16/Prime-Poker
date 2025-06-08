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
            if value == float(expected):
                return value
            else:
                return False


def is_valid_input(text: str) -> bool:
    parser = Lark(grammar, parser="lalr", transformer=CalcTransformer())
    try:
        parser.parse(text)
        return True
    except Exception:
        return False


def evaluate_expression(text: str) -> int | None:
    parser = Lark(grammar, parser="lalr", transformer=CalcTransformer())
    try:
        return int(str(parser.parse(text)))
    except Exception as e:
        return None


examples = [
    "2 * 3 * 4",  # 24
    "2 ^ 3",  # 8
    "2 ^ 3 * 5",  # 40
    "2 * 3 ^ 2",  # 18 ✅
    "2 ^ 3 * 3 * 5 = 120",  # True
    "2 * 3 ^ 2 = 18",  # True
    "2 ^ 3 ^ 2",  # ❌
]


def test1():
    parser = Lark(grammar, parser="lalr", transformer=CalcTransformer())
    for ex in examples:
        try:
            result = parser.parse(ex)
            print(f"{ex:25} => {result}")
        except Exception as e:
            print(f"{ex:25} => ❌ Error: {e}")


def test2():
    for ex in examples:
        print(is_valid_input(ex), ex)


def test3():
    res = evaluate_expression("2 * 3 ^ 2 = 18")
    print(type(res))
    print(res)


if __name__ == "__main__":
    ...
