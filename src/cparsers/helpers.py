from .status import Status
from .error import ParserError
from .parser import Parser


def simplex(obj): return Parser.Simplex(obj)

def sequenceOf(*parsers): return Parser.SequenceOf(*parsers)

def choiceOf(*parsers): return Parser.ChoiceOf(*parsers)

def many(pattern, *, strict: bool = False): return Parser.Many(pattern, strict=strict)

def lazy(thunk): return Parser.Lazy(thunk)



def between(left: Parser, right: Parser):
    def operator(content: Parser):
        return Parser.SequenceOf(left, content, right).map(
            lambda status: status.result[1]
        )
    return operator

def separated(sep: Parser):
    def operator(content: Parser):
        def transformer(status: Status):
            gathered = []
            next = status
            while True:
                temp = content.transformer(next)
                if isinstance(temp, ParserError): break
                gathered.append(temp.result)
                next = temp
                temp = sep.transformer(next)
                if isinstance(temp, ParserError): break
                next = temp
            return next.chainResult(gathered, increment=0)
        return Parser(transformer)
    return operator
