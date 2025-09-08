from typing import Callable, Any, Self

from .status import Status
from .error import ParserError

class Parser:
    '''Default parser class.\nImplements: `.map`, `.chain`, `.match` and `.reassign`'''

    def __init__(self, transformer: Callable[[Status], Status]):
        self.__transformer: Callable[[Status], Status] = transformer

    @property
    def transformer(self) -> Callable[[Status], Status]:
        '''READ ONLY. Return current parser transformer'''
        return self.__transformer

    def run(self, status: Status) -> Status:
        '''Execute parser on `status` and return structured data'''
        return self.__transformer(status)

    def map(self, function: Callable[[Status], Any]) -> Self:
        '''Map parser result using `function`.\n`function` should return only data'''
        def wrapper(status: Status) -> Status:
            current = self.run(status)
            if isinstance(current, ParserError): return current
            return current.chainResult(function(current), increment=0)
        return Parser(wrapper)

    def chain(self, function: Callable[[Status], Self]) -> Self:
        '''Chain next parser based on returned status'''
        def wrapper(status: Status) -> Status:
            current = self.run(status)
            if isinstance(current, ParserError): return current
            nextParser = function(current)
            return nextParser.run(current)
        return Parser(wrapper)    
    
    def match(self, cases: dict[Any, Self]) -> Self:
        '''Select parser from `cases` based on last status'''
        def wrapper(status: Status) -> Status:
            current = self.run(status)
            if isinstance(current, ParserError): return current

            nextParser = cases[current.result]
            return nextParser.run(current)
        return Parser(wrapper)
        
    def reassign(self, parser: Self):
        '''Assign new transformer'''
        self.__transformer = parser.transformer