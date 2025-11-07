"""Integration tests for CLI commands using pytest and Click's CliRunner."""
# pylint: disable=redefined-outer-name

import ast
import pytest
from click.testing import CliRunner
from src.cli import cli as cli_group

@pytest.fixture
def runner():
    """Fixture to provide a shared CliRunner instance for CLI integration tests."""
    return CliRunner()

def run_and_parse(runner, argv):
    """Helper to run CLI and parse python-like output."""
    result = runner.invoke(cli_group, argv)
    assert result.exit_code == 0, f"CLI failed: {result.output}"
    output = result.output.strip()
    try:
        return ast.literal_eval(output)
    except (ValueError, SyntaxError):
        return output

# ========== CLEAN GROUP TESTS ==========
def test_cli_remove_missing(runner):
    """Test CLI remove missing values command."""
    argv = ['clean', 'remove-missing', "[1, None, 2, '', 3]"]
    parsed = run_and_parse(runner, argv)
    assert parsed == [1, 2, 3]

def test_cli_fill_missing_with_option(runner):
    """Test CLI fill missing values with custom fill value."""
    argv = ['clean', 'fill-missing', "[None, '', 5]", '--fill-value', '9']
    parsed = run_and_parse(runner, argv)
    assert parsed == [9, 9, 5]

def test_cli_fill_missing_default(runner):
    """Test CLI fill missing values with default fill value."""
    argv = ['clean', 'fill-missing', "[None, '', 5]"]
    parsed = run_and_parse(runner, argv)
    assert parsed == [0, 0, 5]

# ========== NUMERIC GROUP TESTS ==========
def test_cli_numeric_normalize_with_options(runner):
    """Test CLI normalize with custom min/max options."""
    argv = ['numeric', 'normalize', "[1, 2, 3]", '--min-val', '0', '--max-val', '10']
    parsed = run_and_parse(runner, argv)
    assert pytest.approx(min(parsed), rel=1e-9) == 0.0
    assert pytest.approx(max(parsed), rel=1e-9) == 10.0
    assert len(parsed) == 3

def test_cli_numeric_normalize_default(runner):
    """Test CLI normalize with default options."""
    argv = ['numeric', 'normalize', "[1, 2, 3, 4, 5]"]
    parsed = run_and_parse(runner, argv)
    assert pytest.approx(min(parsed), rel=1e-9) == 0.0
    assert pytest.approx(max(parsed), rel=1e-9) == 1.0

def test_cli_numeric_standardize(runner):
    """Test CLI standardize command."""
    argv = ['numeric', 'standardize', "[1, 2, 3, 4, 5]"]
    parsed = run_and_parse(runner, argv)
    mean = sum(parsed) / len(parsed)
    assert abs(mean) < 1e-9

def test_cli_numeric_clip(runner):
    """Test CLI clip command with options."""
    argv = ['numeric', 'clip', "[-1, 0.5, 2, 3]", '--min-val', '0', '--max-val', '1']
    parsed = run_and_parse(runner, argv)
    assert parsed == [0, 0.5, 1, 1]

def test_cli_numeric_to_integers(runner):
    """Test CLI convert to integers command."""
    argv = ['numeric', 'to-integers', "['1', '2.5', 'abc', '4']"]
    parsed = run_and_parse(runner, argv)
    assert parsed == [1, 2, 4]

def test_cli_numeric_log_transform(runner):
    """Test CLI logarithmic transform command."""
    argv = ['numeric', 'log-transform', "[1, 2, 10]"]
    parsed = run_and_parse(runner, argv)
    assert len(parsed) == 3
    assert all(isinstance(x, float) for x in parsed)

# ========== TEXT GROUP TESTS ==========
def test_cli_text_tokenize(runner):
    """Test CLI text tokenize command."""
    argv = ['text', 'tokenize', "Hello, World! 123"]
    parsed = run_and_parse(runner, argv)
    assert parsed == "hello world 123"

def test_cli_text_remove_punctuation(runner):
    """Test CLI remove punctuation command."""
    argv = ['text', 'remove-punctuation', "Hello, World!"]
    parsed = run_and_parse(runner, argv)
    assert parsed == "Hello World"

def test_cli_text_remove_stopwords(runner):
    """Test CLI remove stopwords command."""
    argv = ['text', 'remove-stopword', "This is a test", '--stopwords', 'is,a']
    parsed = run_and_parse(runner, argv)
    assert parsed == "this test"

def test_cli_text_remove_stopwords_no_option(runner):
    """Test CLI remove stopwords without stopwords option."""
    argv = ['text', 'remove-stopword', "This is a test"]
    parsed = run_and_parse(runner, argv)
    assert parsed == "this is a test"

# ========== STRUCT GROUP TESTS ==========
def test_cli_struct_shuffle_with_seed(runner):
    """Test CLI shuffle with seed option."""
    argv = ['struct', 'shuffle', "[1,2,3,4,5]", '--seed', '123']
    parsed1 = run_and_parse(runner, argv)
    parsed2 = run_and_parse(runner, argv)
    assert parsed1 == parsed2
    assert sorted(parsed1) == [1,2,3,4,5]

def test_cli_struct_shuffle_no_seed(runner):
    """Test CLI shuffle without seed option."""
    argv = ['struct', 'shuffle', "[1,2,3,4,5]"]
    parsed = run_and_parse(runner, argv)
    assert sorted(parsed) == [1,2,3,4,5]

def test_cli_struct_flatten(runner):
    """Test CLI flatten command."""
    argv = ['struct', 'flatten', "[[1,2],[2,3],[]]"]
    parsed = run_and_parse(runner, argv)
    assert parsed == [1,2,2,3]

def test_cli_struct_unique(runner):
    """Test CLI unique command."""
    argv = ['struct', 'unique', "[1,2,2,3,1]"]
    parsed = run_and_parse(runner, argv)
    assert parsed == [1,2,3]

# ========== ERROR HANDLING TESTS ==========
def test_cli_invalid_command(runner):
    """Test CLI with invalid command."""
    result = runner.invoke(cli_group, ['invalid', 'command'])
    assert result.exit_code != 0

def test_cli_invalid_syntax(runner):
    """Test CLI fails when given malformed list input."""
    result = runner.invoke(cli_group, ['clean', 'remove-missing', "[1,,2]"])
    assert result.exit_code != 0
    assert "Error" in result.output or "invalid" in result.output.lower()

def test_cli_remove_missing_invalid_input_shows_error(runner):
    """Test CLI remove-missing shows error message on invalid input."""
    result = runner.invoke(cli_group, ['clean', 'remove-missing', "[1,,2]"])
    # Debe fallar
    assert result.exit_code != 0
    # Pero debe mostrar el mensaje del echo previo
    assert "Error: invalid input syntax" in result.output


def test_cli_help_commands(runner):
    """Test CLI help functionality."""
    result = runner.invoke(cli_group, ['--help'])
    assert result.exit_code == 0
    assert 'Data preprocessing CLI tool' in result.output
