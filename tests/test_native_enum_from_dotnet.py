import enum

from fractured_json import NativeEnum, FracturedJsonOptions


class FakeDotNetEnum:
    Name = "Example"

    @staticmethod
    def GetEnumNames():
        return ["Alpha", "Beta"]

    @staticmethod
    def GetEnumValues():
        return [10, 20]


def test_from_dotnet_type_creates_class_and_members():
    cls = NativeEnum.from_dotnet_type(FakeDotNetEnum)
    assert isinstance(cls, type)
    assert hasattr(cls, "ALPHA")
    assert hasattr(cls, "BETA")
    assert cls.ALPHA.value == 10
    assert cls.BETA.value == 20


def test_from_value_and_from_name_and_caching():
    cls1 = NativeEnum.from_dotnet_type(FakeDotNetEnum)
    cls2 = NativeEnum.from_dotnet_type(FakeDotNetEnum)
    assert cls1 is cls2  # cached

    assert cls1.from_value(20) is cls1.BETA
    assert cls1.from_name("Alpha") is cls1.ALPHA

    assert cls1.names() == ["ALPHA", "BETA"]
    assert set(cls1.values()) == {10, 20}


def test_fracturedjsonoptions_enum_roundtrip():
    opts = FracturedJsonOptions()
    # set using string name
    opts.comment_policy = "Remove"
    assert opts.comment_policy.name == "REMOVE"

    # set using NativeEnum member
    cls = NativeEnum.from_dotnet_type(opts._properties["comment_policy"]["prop"].PropertyType)
    member = cls.from_name("Preserve")
    opts.comment_policy = member
    assert opts.comment_policy is member

    # invalid value raises ValueError from setter
    try:
        opts.set("comment_policy", "Invalid")
    except ValueError as e:
        assert "Invalid value 'Invalid' for option comment_policy" in str(e)
    else:
        raise AssertionError("Expected ValueError")
