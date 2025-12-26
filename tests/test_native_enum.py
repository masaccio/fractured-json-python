import pytest

from fractured_json import NativeEnum


class FakeDotNetEnum:  # noqa: D101
    Name = "Example"

    @staticmethod
    def GetEnumNames():  # noqa: ANN205, D102, N802
        return ["Alpha", "Beta"]

    @staticmethod
    def GetEnumValues():  # noqa: ANN205, D102, N802
        return [10, 20]


def test_from_dotnet_type():
    cls = NativeEnum.from_dotnet_type(FakeDotNetEnum)
    assert isinstance(cls, type)
    assert hasattr(cls, "ALPHA")
    assert hasattr(cls, "BETA")
    assert cls.ALPHA.value == 10
    assert cls.BETA.value == 20


def test_type_caching():
    cls1 = NativeEnum.from_dotnet_type(FakeDotNetEnum)
    cls2 = NativeEnum.from_dotnet_type(FakeDotNetEnum)
    assert cls1 is cls2  # cached

    assert cls1.from_value(20) is cls1.BETA
    assert cls1.from_name("Alpha") is cls1.ALPHA

    assert cls1.names() == ["ALPHA", "BETA"]
    assert set(cls1.values()) == {10, 20}


def test_eq_and_hash():
    cls = NativeEnum.from_dotnet_type(FakeDotNetEnum)
    a = cls.ALPHA
    b = cls.BETA

    # equality between members
    assert a == cls.from_value(10)
    assert a != b

    # equality to integer value (legacy behavior)
    assert a == 10
    assert a != 11

    # hash stable and usable as dict key
    d = {a: "x", b: "y"}
    assert d[a] == "x"
    assert d[cls.from_value(20)] == "y"


def test_exceptions():
    cls = NativeEnum.from_dotnet_type(FakeDotNetEnum)

    with pytest.raises(ValueError, match=r"is not a valid value for Example"):
        cls.from_value(999)

    with pytest.raises(ValueError, match=r"is not a valid name for Example"):
        cls.from_name("Invalid")
