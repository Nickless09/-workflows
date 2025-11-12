# python/arithmetic_pkg/__init__.py
# This package will contain the compiled extension named 'arithmetic' (arithmetic.so)

try:
    # if CI or packaging copied the extension into this folder, import it
    from .arithmetic import sum as _sum
except Exception as e:
    def _sum(a, b):
        raise ImportError("compiled arithmetic extension not found") from e

def sum(a, b):
    return _sum(a, b)
