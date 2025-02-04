from cparsers.status import Status
from cparsers.string import StringParser
from cparsers.parser import Parser

import cparsers.string

def test_word():
    p = StringParser.word('hello')

    s = Status('hello')

    r = p.run(s)

    assert r.result == 'hello'

def test_regex():
    p = StringParser.regex(r'^[0-9]{2}[a-z]{2}')

    s = Status('24rg')

    r = p.run(s)

    assert r.result == '24rg'

def test_helpers():

    p = cparsers.string.uint()

    s = Status('2137')

    r = p.run(s)

    assert r.result == 2137

    p = cparsers.string.sint()

    s = Status('-3621')

    r = p.run(s)

    assert r.result == -3621

def test_expr():

    integer = cparsers.string.sint()

    add = Parser.ChoiceOf(
        Parser.SequenceOf(Parser.Lazy(lambda: term), cparsers.string.regex(r'^\+'), Parser.Lazy(lambda: add)),
        Parser.Lazy(lambda: term),
    )

    term = Parser.ChoiceOf(
        Parser.SequenceOf(cparsers.string.word('('), Parser.Lazy(lambda: add), cparsers.string.word(')')),
        integer,
    )

    s = Status('1+(2+1)')

    r = add.run(s)

    print(r)

    assert 1 == 2