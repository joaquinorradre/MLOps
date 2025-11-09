"""
cli.py
------
Command Line Interface (CLI) for data preprocessing utilities.
It organizes commands into groups (clean, numeric, text, struct)
to make data transformation accessible via the terminal.
"""

import ast
import click
from .preprocessing import (
    remove_missing_values,
    fill_missing_values,
    normalize_values,
    standardize_values,
    clip_values,
    convert_to_integers,
    logarithmic_transform,
    tokenize_text,
    select_alphanumeric,
    remove_stopwords,
    shuffle_list,
    flatten_list,
    remove_duplicates,
)


@click.group()
def cli():
    """Data preprocessing CLI tool."""


@cli.group()
def clean():
    """Data cleaning functions."""


@cli.group()
def numeric():
    """Numerical data processing functions."""


@cli.group()
def text():
    """Text processing functions."""


@cli.group()
def struct():
    """Data structure manipulation functions."""


# ========== CLEAN GROUP ==========
@clean.command()
@click.argument("values", type=str)
def remove_missing(values):
    """Remove missing values from list.

    Example: python -m src.cli clean remove-missing "[1, None, 2, '', 3]"
    """
    try:
        parsed_values = ast.literal_eval(values)
    except Exception as e:
        click.echo(f"Error: invalid input syntax ({e})")
        raise click.ClickException("Invalid syntax")

    result = remove_missing_values(parsed_values)
    click.echo(result)


@clean.command()
@click.argument("values", type=str)
@click.option("--fill-value", default=0, help="Value to fill missing entries")
def fill_missing(values, fill_value):
    """Fill missing values with specified value.

    Example: python -m src.cli clean fill-missing "[1, None, 2]" --fill-value 0
    """
    parsed_values = ast.literal_eval(values)
    result = fill_missing_values(parsed_values, fill_value)
    click.echo(result)


# ========== NUMERIC GROUP ==========
@numeric.command()
@click.argument("values", type=str)
@click.option("--min-val", default=0.0, help="Minimum value for normalization")
@click.option("--max-val", default=1.0, help="Maximum value for normalization")
def normalize(values, min_val, max_val):
    """Normalize numerical values using min-max method.

    Example: python -m src.cli numeric normalize "[1, 2, 3, 4, 5]" --min-val 0 --max-val 1
    """
    parsed_values = ast.literal_eval(values)
    result = normalize_values(parsed_values, min_val, max_val)
    click.echo(result)


@numeric.command()
@click.argument("values", type=str)
def standardize(values):
    """Standardize numerical values using z-score method.

    Example: python -m src.cli numeric standardize "[1, 2, 3, 4, 5]"
    """
    parsed_values = ast.literal_eval(values)
    result = standardize_values(parsed_values)
    click.echo(result)


@numeric.command()
@click.argument("values", type=str)
@click.option("--min-val", default=0, help="Minimum value to clip")
@click.option("--max-val", default=1, help="Maximum value to clip")
def clip(values, min_val, max_val):
    """Clip numerical values to specified range.

    Example: python -m src.cli numeric clip "[-1, 0.5, 2, 3]" --min-val 0 --max-val 1
    """
    parsed_values = ast.literal_eval(values)
    result = clip_values(parsed_values, min_val, max_val)
    click.echo(result)


@numeric.command()
@click.argument("values", type=str)
def to_integers(values):
    """Convert string values to integers.

    Example: python -m src.cli numeric to-integers "['1', '2.5', 'abc', '4']"
    """
    parsed_values = ast.literal_eval(values)
    result = convert_to_integers(parsed_values)
    click.echo(result)


@numeric.command()
@click.argument("values", type=str)
def log_transform(values):
    """Transform values to logarithmic scale.

    Example: python -m src.cli numeric log-transform "[1, 2, 10, 100]"
    """
    parsed_values = ast.literal_eval(values)
    result = logarithmic_transform(parsed_values)
    click.echo(result)


# ========== TEXT GROUP ==========
@text.command()
@click.argument("input_text", type=str)
def tokenize(input_text):
    """Tokenize text into words, keeping alphanumeric characters and lowercasing.

    Example: python -m src.cli text tokenize "Hello, World! 123"
    """
    result = tokenize_text(input_text)
    click.echo(result)


@text.command()
@click.argument("input_text", type=str)
def remove_punctuation(input_text):
    """Remove punctuation, keeping only alphanumeric characters and spaces.

    Example: python -m src.cli text remove-punctuation "Hello, World!"
    """
    result = select_alphanumeric(input_text)
    click.echo(result)


@text.command()
@click.argument("input_text", type=str)
@click.option(
    "--stopwords", default="", help="Comma-separated list of stopwords to remove"
)
def remove_stopword(input_text, stopwords):
    """Remove stopwords from text.

    Example: python -m src.cli text remove-stopwords "this is a test" --stopwords "is,a"
    """
    stopwords_list = (
        [word.strip() for word in stopwords.split(",")] if stopwords else []
    )
    result = remove_stopwords(input_text, stopwords_list)
    click.echo(result)


# ========== STRUCT GROUP ==========
@struct.command()
@click.argument("values", type=str)
@click.option("--seed", default=None, type=int, help="Seed for reproducible shuffling")
def shuffle(values, seed):
    """Shuffle list values randomly.

    Example: python -m src.cli struct shuffle "[1, 2, 3, 4, 5]" --seed 42
    """
    parsed_values = ast.literal_eval(values)
    result = shuffle_list(parsed_values, seed)
    click.echo(result)


@struct.command()
@click.argument("values", type=str)
def flatten(values):
    """Flatten a list of lists.

    Example: python -m src.cli struct flatten "[[1, 2], [3, 4], [5]]"
    """
    parsed_values = ast.literal_eval(values)
    result = flatten_list(parsed_values)
    click.echo(result)


@struct.command()
@click.argument("values", type=str)
def unique(values):
    """Remove duplicate values from list.

    Example: python -m src.cli struct unique "[1, 2, 2, 3, 1]"
    """
    parsed_values = ast.literal_eval(values)
    result = remove_duplicates(parsed_values)
    click.echo(result)


if __name__ == "__main__": # pragma: no cover
    cli()
