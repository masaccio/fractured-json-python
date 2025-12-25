import re

import pytest

from fractured_json import _get_version


def test_version(script_runner):
    ret = script_runner.run(["fractured-json", "--version"], print_result=False)
    assert ret.success
    assert ret.stdout == _get_version() + "\n"
    assert ret.stderr == ""


def test_help(script_runner):
    ret = script_runner.run(["fractured-json", "--help"], print_result=False)
    assert ret.success
    assert "Format JSON into compact, human readable form" in ret.stdout
    assert "max-total-line-length N" in ret.stdout
    assert ret.stderr == ""


REF_UNICODE_TEST = """{
    "Thai": {
        "Abkhazia": "อับฮาเซีย", 
        "Afghanistan": "อัฟกานิสถาน", 
        "Albania": "แอลเบเนีย"
    }, 
    "Lao": {"Afghanistan": "ອັຟການິດສະຖານ"}, 
    "Uyghur": {"Albania": "ئالبانىيە"}, 
    "Hindi, Marathi, Sanskrit": {"Albania": "अल्बानिया"}, 
    "Western Armenian": {"Albania": "Ալբանիա"}
}
"""  # noqa: W291


def test_all_args(script_runner, pytestconfig):
    ret = script_runner.run(
        [
            "fractured-json",
            "--allow-trailing-commas",
            "--always-expand-depth=2",
            "--colon-before-prop-name-padding",
            "--colon-padding",
            "--comma-padding",
            "--comment-padding",
            "--comment-policy=PRESERVE",
            "--indent-spaces=2",
            "--json-eol-style=LF",
            "--max-compact-array-complexity=2",
            "--max-inline-complexity=2",
            "--max-prop-name-padding=2",
            "--max-table-row-complexity=2",
            "--max-total-line-length=100",
            "--min-compact-array-row-items=2",
            "--nested-bracket-padding",
            "--number-list-alignment=LEFT",
            "--prefix-string=::",
            "--preserve-blank-lines",
            "--simple-bracket-padding",
            "--table-comma-placement=BEFORE_PADDING_EXCEPT_NUMBERS",
            "--use-tab-to-indent",
            "--east-asian-chars",
            "tests/data/test-comments-0.jsonc",
        ],
        print_result=False,
    )

    ref_output = Path("tests/data/test-comments-0.ref-1.jsonc").read_text()
    if pytestconfig.getoption("test_verbose") and ret.stdout != ref_output:
        json_string_dbg = ">" + re.sub(r"\n", "<\n>", ret.stdout) + "<"
        ref_json_dbg = ">" + re.sub(r"\n", "<\n>", ref_output) + "<"
        print("===== TEST")
        print(json_string_dbg)
        print("===== REF")
        print(ref_json_dbg)
        print("=====")

    assert ret.stderr == ""
    assert ret.success
    assert ret.stdout == ref_output


def test_unicode(script_runner):
    ret = script_runner.run(
        [
            "fractured-json",
            "--east-asian-chars",
            "--no-ensure-ascii",
            "--crlf",
            "tests/data/test-issue-4a.json",
        ],
        print_result=False,
    )
    assert ret.stderr == ""
    assert ret.success
    ref = REF_UNICODE_TEST.replace("\n", "\r\n")
    assert ret.stdout == ref


def test_debug(script_runner):
    ret = script_runner.run(["fractured-json", "--debug", "tests/data/test-1.json"])
    assert "DEBUG:fractured_json.formatter:format_table_dict_list" in ret.stderr
    assert ret.success
    assert '"title": "Sample Konfabulator Widget"' in ret.stdout


@pytest.mark.script_launch_mode("subprocess")
def test_main(script_runner):
    ret = script_runner.run(["python3", "-m", "fractured-json", "--help"])
    assert ret.stderr == ""
    assert ret.success
    assert "[-h] [-V] [--output" in ret.stdout


@pytest.mark.script_launch_mode("subprocess")
def test_stdin(script_runner):
    with open("tests/data/test-bool.json") as fh:
        ret = script_runner.run(["fractured-json", "-"], stdin=fh)
        assert ret.stderr == ""
        assert ret.success
        assert ret.stdout == '{ "bools": {"true": true, "false": false} }\n'


def test_multifile(script_runner):
    ret = script_runner.run(
        ["fractured-json", "tests/data/test-bool.json", "tests/data/test-bool.json"],
    )
    assert ret.stderr == ""
    assert ret.success
    assert ret.stdout == '{ "bools": {"true": true, "false": false} }\n' * 2


def test_output(script_runner, tmp_path):
    tmp_file = tmp_path / "test.json"
    ret = script_runner.run(
        ["fractured-json", "tests/data/test-bool.json", "--output", str(tmp_file)],
    )
    assert ret.stderr == ""
    assert ret.success
    assert tmp_file.read_text() == '{ "bools": {"true": true, "false": false} }\n'


def test_output_mismatched_number_of_files(script_runner):
    ret = script_runner.run(
        [
            "fractured-json",
            "tests/data/test-bool.json",
            "--output",
            "foo",
            "--output",
            "bar",
        ],
    )
    assert ret.stderr == "fractured-json: the numbers of input and output file names do not match\n"
    assert ret.returncode == 1
