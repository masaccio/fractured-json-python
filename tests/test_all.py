import itertools
from pathlib import Path
from typing import Any

from fractured_json import Formatter, FracturedJsonOptions

TEST_RANGE = [-1, 2, 4]
ALL_OPTION_COMBOS = {
    "always_expand_depth": TEST_RANGE,
    "max_compact_array_complexity": TEST_RANGE,
    "max_inline_complexity": TEST_RANGE,
    "max_prop_name_padding": TEST_RANGE,
    "max_table_row_complexity": TEST_RANGE,
    "max_total_line_length": [80, 160],
    "min_compact_array_row_items": TEST_RANGE,
    "number_list_alignment": ["LEFT", "RIGHT", "DECIMAL", "NORMALIZE"],
    "table_comma_placement": ["BEFORE_PADDING", "AFTER_PADDING", "BEFORE_PADDING_EXCEPT_NUMBERS"],
}

FRACTURED_JSON_TEST_DIR = Path("FracturedJson/Tests/StandardJsonFiles")
FRACTURED_JSON_TESTS = {
    p.name: p.read_text(encoding="utf-8-sig") for p in FRACTURED_JSON_TEST_DIR.glob("*.json")
}


def dict_combinations(options: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate all combinations from dict where values are lists/ranges of allowed values."""
    keys_list = list(options.keys())
    value_lists = []

    for key, allowed_vals in options.items():
        if isinstance(allowed_vals, range):
            value_lists.append(list(allowed_vals))
        elif isinstance(allowed_vals, list):
            value_lists.append(allowed_vals)
        else:
            raise ValueError(f"Unsupported value type for {key}: {type(allowed_vals)}")

    combinations = []
    for combo in itertools.product(*value_lists):
        combinations.append(dict(zip(keys_list, combo)))

    return combinations


ALL_TEST_COMBINATIONS = {}


def no_test_all_combinations():
    all_combinations = dict_combinations(ALL_OPTION_COMBOS)
    for test_file, test_input in FRACTURED_JSON_TESTS.items():
        for test_options in all_combinations:
            options = FracturedJsonOptions(**test_options)
            formatter = Formatter(options=options)
            test_output = formatter.reformat(test_input)
            key = hash(test_output)
            if key not in ALL_TEST_COMBINATIONS:
                ALL_TEST_COMBINATIONS[key] = {"test_file": test_file, "options": test_options}

    for test in ALL_TEST_COMBINATIONS.values():
        test_name = "TEST_DATA_" + test["test_file"].split(".")[0]
        print(f"  run_test_combination({test_name}), {test['options']})")
