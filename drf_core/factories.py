from factory.django import DjangoModelFactory as ModelFactory # noqa
from factory import ( # noqa
    SubFactory,
    Iterator,

    # https://factoryboy.readthedocs.io/en/latest/reference.html#traits
    Faker,

    # https://factoryboy.readthedocs.io/en/latest/reference.html#lazyfunction
    LazyFunction,

    # https://factoryboy.readthedocs.io/en/latest/reference.html#lazyattribute
    LazyAttribute,

    # https://factoryboy.readthedocs.io/en/latest/reference.html#factory.lazy_attribute
    lazy_attribute,


    # https://factoryboy.readthedocs.io/en/latest/reference.html#sequence
    Sequence,

    # https://factoryboy.readthedocs.io/en/latest/reference.html#factory.sequence
    sequence,
    LazyAttributeSequence,
    Trait,
    Dict,
    List,

    # https://factoryboy.readthedocs.io/en/latest/reference.html#traits
    Trait,
)

from factory.fuzzy import ( # noqa
    # https://factoryboy.readthedocs.io/en/latest/fuzzy.html#fuzzytext
    FuzzyText,

    # https://factoryboy.readthedocs.io/en/latest/fuzzy.html#fuzzychoice
    FuzzyChoice,

    # https://factoryboy.readthedocs.io/en/latest/fuzzy.html#fuzzyinteger
    FuzzyInteger,

    # https://factoryboy.readthedocs.io/en/latest/fuzzy.html#fuzzydecimal
    FuzzyDecimal,

    # https://factoryboy.readthedocs.io/en/latest/fuzzy.html#fuzzyfloat
    FuzzyFloat,

    # https://factoryboy.readthedocs.io/en/latest/fuzzy.html#fuzzydate
    FuzzyDate,

    # https://factoryboy.readthedocs.io/en/latest/fuzzy.html#fuzzydatetime
    FuzzyDateTime,
)


class FuzzyBoolean(FuzzyChoice):
    def __init__(self):
        super().__init__(choices=[True, False])
