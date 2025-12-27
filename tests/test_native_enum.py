from fractured_json import CommentPolicy, NumberListAlignment


def test_eq_and_hash():
    assert CommentPolicy.REMOVE != CommentPolicy.PRESERVE
    assert NumberListAlignment.LEFT == 0
    a = dict()
    a[CommentPolicy.REMOVE] = "test"
    assert list(a.keys())[0].name == "REMOVE"
    assert list(a.keys())[0].value == 1
