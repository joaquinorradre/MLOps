"""Unit tests for preprocessing logic functions in src.preprocessing."""
# pylint: disable=redefined-outer-name,unused-argument

import math
from typing import List

import pytest

from src.preprocessing import (
    remove_missing_values,
    fill_missing_values,
    remove_duplicates,
    normalize_values,
    standardize_values,
    clip_values,
    convert_to_integers,
    logarithmic_transform,
    tokenize_text,
    select_alphanumeric,
    remove_stopwords,
    flatten_list,
    shuffle_list,
)

# ========== FIXTURES ==========
@pytest.fixture
def sample_numbers() -> List[float]:
    """Fixture returning a sample list of floats used in multiple tests."""
    return [1.0, 2.0, 3.0, 4.0, 5.0]

@pytest.fixture
def sample_mixed_data() -> List:
    """Fixture with mixed data including missing values."""
    return [1, None, '', float('nan'), 2, 'text', 3.5]

# ========== PARAMETRIZED TESTS (sin opciones requeridas) ==========
@pytest.mark.parametrize(
    "input_values,expected",
    [
        ([1, None, 2, '', 3], [1, 2, 3]),
        (['a', '', 'c', None], ['a', 'c']),
        ([1, 2, 3], [1, 2, 3]),  # no missing values
        ([None, '', float('nan')], []),  # all missing
    ],
)
def test_remove_missing_values_parametrized(input_values, expected):
    """Test remove_missing_values with various inputs."""
    result = remove_missing_values(input_values)
    assert result == expected

@pytest.mark.parametrize(
    "values",
    [
        ([1.0, 1.0, 1.0]),       # zero variance
        ([1.0, 2.0, 3.0]),       # simple case
        ([0.0, 5.0, 10.0]),      # different range
        ([-1.0, 0.0, 1.0]),      # with negatives
    ],
)
def test_standardize_properties(values):
    """Standardize should return mean ~ 0 and std ~ 1 (or zeros if variance zero)."""
    stdz = standardize_values(values)
    if len(set(values)) == 1:
        # zero variance -> returned list of zeros
        assert all(abs(x) < 1e-12 for x in stdz)
    else:
        mean = sum(stdz) / len(stdz)
        variance = sum((x - mean) ** 2 for x in stdz) / len(stdz)
        std_dev = math.sqrt(variance)
        assert abs(mean) < 1e-9
        assert pytest.approx(std_dev, rel=1e-6) == 1.0

def test_standardize_empty_list():
    """Test standardize_values returns empty list when input is empty."""
    result = standardize_values([])
    assert result == []

# ========== PARAMETRIZED TESTS (con opciones requeridas) ==========
@pytest.mark.parametrize(
    "values,fill_value,expected",
    [
        ([1, None, 3], 0, [1, 0, 3]),
        ([1, None, 3], 999, [1, 999, 3]),
        ([None, '', 5], -1, [-1, -1, 5]),
        ([], 42, []),  # empty list
    ],
)
def test_fill_missing_values_parametrized(values, fill_value, expected):
    """Test fill_missing_values with different fill values."""
    result = fill_missing_values(values, fill_value)
    assert result == expected

@pytest.mark.parametrize(
    "new_min,new_max",
    [
        (0.0, 1.0),
        (-1.0, 1.0),
        (0.0, 10.0),
        (-5.0, 5.0),
    ],
)
def test_normalize_values_with_options(sample_numbers, new_min, new_max):
    """Normalization should map min(sample_numbers) -> new_min and max -> new_max."""
    normalized = normalize_values(sample_numbers, new_min=new_min, new_max=new_max)
    assert pytest.approx(min(normalized), rel=1e-9) == new_min
    assert pytest.approx(max(normalized), rel=1e-9) == new_max
    # every value should be between new_min and new_max
    assert all(new_min - 1e-12 <= v <= new_max + 1e-12 for v in normalized)

def test_normalize_single_unique_value():
    """Test normalize_values when all values are identical."""
    values = [10, 10, 10]
    result = normalize_values(values, new_min=0, new_max=1)
    # Debe devolver todos iguales a new_min
    assert result == [0, 0, 0]

# ========== TESTS UNITARIOS ADICIONALES ==========
def test_remove_duplicates(sample_mixed_data):
    """Test remove duplicates using fixture."""
    values = [1, 2, 2, 3, 1, 4]
    assert remove_duplicates(values) == [1, 2, 3, 4]

def test_clip_values():
    """Test clip_values function."""
    values = [-5, 0.5, 2, 10]
    clipped = clip_values(values, min_val=0, max_val=2)
    assert clipped == [0, 0.5, 2, 2]

def test_convert_to_integers():
    """Test convert_to_integers function."""
    values = ['1', '2.5', 'abc', None, '4']
    conv = convert_to_integers(values)
    # '2.5' -> int(2.5) == 2
    assert conv == [1, 2, 4]

def test_logarithmic_transform():
    """Test logarithmic_transform function."""
    values = [-1, 0, 1, math.e, 100]
    logged = logarithmic_transform(values)
    # only positive values are transformed
    assert pytest.approx(logged[0]) == math.log(1)
    assert pytest.approx(logged[1]) == math.log(math.e)
    assert pytest.approx(logged[2]) == math.log(100)
    assert len(logged) == 3  # three positive values


def test_text_processing_tokenize_and_select():
    """Test text tokenization and alphanumeric selection."""
    text = "Hello, WORLD! 123"
    tok = tokenize_text(text)
    sel = select_alphanumeric(text)
    assert tok == "hello world 123"
    assert sel == "Hello WORLD 123"

def test_remove_stopwords_lowercased():
    """Test remove_stopwords function."""
    text = "This is a Test of stopwords"
    stopwords = ["is", "a", "of"]
    result = remove_stopwords(text, stopwords)
    # lowercased and stopwords removed
    assert result == "this test stopwords"

def test_flatten_list():
    """Test flatten_list function."""
    nested = [[1, 2], [3], [], [4, 5]]
    assert flatten_list(nested) == [1, 2, 3, 4, 5]

def test_shuffle_list_reproducible():
    """Test shuffle_list function with seed for reproducibility."""
    values = [1, 2, 3, 4, 5]
    s1 = shuffle_list(values, seed=42)
    s2 = shuffle_list(values, seed=42)
    assert s1 == s2
    # ensure it's a permutation of original
    assert sorted(s1) == sorted(values)

def test_normalize_edge_cases(sample_numbers):
    """Test normalization edge cases using fixture."""
    # Single value
    single = [5.0]
    result = normalize_values(single, 0.0, 1.0)
    assert result == [0.0]  # single value maps to min
    # Empty list
    assert normalize_values([]) == []

def test_normalize_invalid_input():
    """Test normalization raises error for invalid (non-list) input."""
    with pytest.raises((TypeError, ValueError)):
        normalize_values("not a list")
