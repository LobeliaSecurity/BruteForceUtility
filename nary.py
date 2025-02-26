import functools


class Numeric:
    class Maximum(Exception):
        def __init__(self, arg=""):
            self.arg = arg

    def __init__(self, radix: int, nextDigit, startDecimal=0) -> None:
        self.radix = radix
        self.decimal = startDecimal
        self.nextDigit = nextDigit
        self.startDecimal = startDecimal

    def increment(self) -> None:
        self.decimal += 1
        if self.decimal == self.radix:
            self.carry()

    def carry(self) -> None:
        self.decimal = self.startDecimal
        if self.nextDigit:
            self.nextDigit.increment()
        else:
            raise Numeric.Maximum


class Nary:
    def __init__(self, radix_list: list = None, digitArray: list = None) -> None:
        if radix_list:
            self.digitArray = [Numeric(radix_list[0], None)]
            for radix in radix_list[1:]:
                self.digitArray.append(Numeric(radix, self.digitArray[-1]))
        elif digitArray:
            self.digitArray = digitArray

    def increment(self):
        yield self
        try:
            while True:
                self.digitArray[-1].increment()
                yield self
        except Numeric.Maximum:
            return self

    def countPattern(self):
        return functools.reduce(
            lambda x, y: x * y, [x.radix for x in self.digitArray], 1
        )