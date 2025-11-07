"""
preprocessing.py
----------------
This module provides various data preprocessing functions for cleaning, transforming,
and manipulating data of different types (numeric, textual, and structural).
"""

import math
import random
import re
from typing import List, Any, Optional


def remove_missing_values(values: List[Any]) -> List[Any]:
    """Remove None, '', and nan values from list."""
    result = []
    for value in values:
        if (
            value is not None
            and value != ""
            and not (isinstance(value, float) and math.isnan(value))
        ):
            result.append(value)
    return result


def fill_missing_values(values: List[Any], fill_value: Any = 0) -> List[Any]:
    """Fill missing values with specified value."""
    result = []
    for value in values:
        if (
            value is None
            or value == ""
            or (isinstance(value, float) and math.isnan(value))
        ):
            result.append(fill_value)
        else:
            result.append(value)
    return result


def remove_duplicates(values: List[Any]) -> List[Any]:
    """Remove duplicate values while preserving order."""
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def normalize_values(
    values: List[float], new_min: float = 0.0, new_max: float = 1.0
) -> List[float]:
    """Normalize values using min-max scaling."""
    if not values:
        return []

    old_min = min(values)
    old_max = max(values)

    if old_max == old_min:
        return [new_min] * len(values)

    return [
        (new_min + (x - old_min) * (new_max - new_min) / (old_max - old_min))
        for x in values
    ]


def standardize_values(values: List[float]) -> List[float]:
    """Standardize values using z-score method."""
    if not values:
        return []

    mean_val = sum(values) / len(values)
    variance = sum((x - mean_val) ** 2 for x in values) / len(values)
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        return [0.0] * len(values)

    return [(x - mean_val) / std_dev for x in values]


def clip_values(values: List[float], min_val: float, max_val: float) -> List[float]:
    """Clip values to specified range."""
    return [max(min_val, min(max_val, x)) for x in values]


def convert_to_integers(values: List[str]) -> List[int]:
    """Convert string values to integers, excluding non-numerical values."""
    result = []
    for value in values:
        try:
            result.append(int(float(value)))
        except (ValueError, TypeError):
            continue
    return result


def logarithmic_transform(values: List[float]) -> List[float]:
    """Transform positive values to logarithmic scale."""
    return [math.log(x) for x in values if x > 0]


def tokenize_text(text: str) -> str:
    """Tokenize text into words, keeping only alphanumeric characters and lowercasing."""
    # Keep only alphanumeric characters and spaces
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    # Convert to lowercase and normalize whitespace
    return " ".join(cleaned.lower().split())


def select_alphanumeric(text: str) -> str:
    """Select only alphanumeric characters and spaces."""
    return re.sub(r"[^a-zA-Z0-9\s]", "", text)


def remove_stopwords(text: str, stopwords: List[str]) -> str:
    """Remove stop words from lowercased text."""
    words = text.lower().split()
    filtered_words = [
        word for word in words if word not in [sw.lower() for sw in stopwords]
    ]
    return " ".join(filtered_words)


def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """Flatten a list of lists."""
    result = []
    for sublist in nested_list:
        result.extend(sublist)
    return result


def shuffle_list(values: List[Any], seed: Optional[int] = None) -> List[Any]:
    """Randomly shuffle list values with optional seed."""
    result = values.copy()
    if seed is not None:
        random.seed(seed)
    random.shuffle(result)
    return result
