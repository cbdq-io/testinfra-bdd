"""Lines of Code feature tests."""
import json
import shutil
import subprocess

import pytest
from pytest_bdd import given, parsers, scenario, then, when

radon_executable = shutil.which('radon')
radon_command = [
    radon_executable,
    'raw',
    '--json',
    '.'
]

radon_report = subprocess.check_output(radon_command).decode('utf-8')  # nosec
radon_report = json.loads(radon_report)
python_files = []

for _ in radon_report:
    python_files.append((_,))


@pytest.mark.parametrize(
    ['python_file'],
    python_files,
)
@scenario('../features/lines_of_code.feature', 'Check Lines of Code in Radon Report')
def test_check_lines_of_code_in_radon_report(python_file):
    """Check Lines of Code in Radon Report."""


@given('a Radon report', target_fixture='radon_stats')
def a_radon_report(python_file):
    """a Radon report."""
    return {}


@when('Python source file is file')
def python_source_file_is_file(python_file, radon_stats):
    """Python source file is file."""
    radon_stats['file_name'] = python_file
    radon_stats['lines_of_code'] = radon_report[python_file]['loc']


@then(parsers.parse('lines of code must not be greater than {max_lines_of_code:d}'))
def lines_of_code_must_not_be_greater_than_max_lines_of_code(max_lines_of_code, radon_stats):
    """lines of code must not be greater than <max_lines_of_code>."""
    file_name = radon_stats['file_name']
    lines_of_code = radon_stats['lines_of_code']
    message = f'{file_name} has {lines_of_code} which exceeds {max_lines_of_code}.'
    assert lines_of_code <= max_lines_of_code, message
