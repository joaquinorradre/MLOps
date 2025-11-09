# MLOps - Fundamentals of Continuous Integration

This project is part of an academic practice to learn the **fundamentals of Continuous Integration (CI)**.

## 🎯 Practice Objective

The main objective is to understand the basic elements of Continuous Integration:
- **Linting**: Search for syntax errors to guarantee code correctness
- **Automatic formatting**: Ensure code has consistent formatting
- **Testing**: Automatic tests to verify that code works correctly

## 🛠️ Tools Used

This project uses the following MLOps tools following best practices:

- **Click**: To create command line interfaces
- **Black**: To automatically format Python code
- **Pylint**: To analyze code and find syntax errors
- **Pytest**: To run project tests
- **Pytest-cov**: To measure test coverage

## 📁 Project Structure

```
MLOps/
├── src/                    # Source folder with project logic
├── tests/                  # Folder with test files
├── main.py                 # Main program file
├── pyproject.toml          # Project configuration and dependencies
├── .python-version         # Specific Python version (3.11)
└── README.md              # This documentation file
```

## 🚀 How to use this project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/joaquinorradre/MLOps.git
   cd MLOps
   ```

2. **Install dependencies**:
   ```bash
   uv sync .
   ```

3. **Run the main program**:
   ```bash
   python main.py
   ```

4. **Use the CLI tool for data preprocessing**:
   ```bash
   python -m src.cli --help
   ```

## 💻 CLI Examples

The project includes a powerful CLI tool for data preprocessing with 4 main groups of commands:

### 🧹 Data Cleaning
```bash
# Remove missing values (None, empty strings)
python -m src.cli clean remove-missing "[1, None, 2, '', 3]"
# Output: [1, 2, 3]

# Fill missing values with a default value
python -m src.cli clean fill-missing "[1, None, 2]" --fill-value 0
# Output: [1, 0, 2]
```

### 🔢 Numeric Processing
```bash
# Normalize values between 0 and 1
python -m src.cli numeric normalize "[1, 2, 3, 4, 5]" --min-val 0 --max-val 1
# Output: [0.0, 0.25, 0.5, 0.75, 1.0]

# Standardize using z-score
python -m src.cli numeric standardize "[1, 2, 3, 4, 5]"
# Output: [-1.265, -0.632, 0.0, 0.632, 1.265]

# Clip values to a range
python -m src.cli numeric clip "[-1, 0.5, 2, 3]" --min-val 0 --max-val 1
# Output: [0, 0.5, 1, 1]

# Convert strings to integers
python -m src.cli numeric to-integers "['1', '2.5', 'abc', '4']"
# Output: [1, 2, 4]

# Apply logarithmic transformation
python -m src.cli numeric log-transform "[1, 2, 10, 100]"
# Output: [0.0, 0.693, 2.303, 4.605]
```

### 📝 Text Processing
```bash
# Tokenize text (clean and lowercase)
python -m src.cli text tokenize "Hello, World! 123"
# Output: hello world 123

# Remove punctuation
python -m src.cli text remove-punctuation "Hello, World!"
# Output: Hello World

# Remove stopwords
python -m src.cli text remove-stopword "this is a test" --stopwords "is,a"
# Output: this test
```

### 🔄 Data Structure Manipulation
```bash
# Shuffle list with seed for reproducibility
python -m src.cli struct shuffle "[1, 2, 3, 4, 5]" --seed 42
# Output: [1, 4, 5, 3, 2]

# Flatten nested lists
python -m src.cli struct flatten "[[1, 2], [3, 4], [5]]"
# Output: [1, 2, 3, 4, 5]

# Remove duplicates while preserving order
python -m src.cli struct unique "[1, 2, 2, 3, 1]"
# Output: [1, 2, 3]
```

## ✅ Useful commands for CI

### Run linting of the code:
```bash
uv run python -m pylint src/*.py .
```

### Format the code:
```bash
uv run black src/*.py .
```

### Run tests:
```bash
uv run python -m pytest -v
```

### View test coverage:
```bash
uv run python -m pytest -v --cov=src

```

- How to structure a Python project following good practices
- MLOps fundamentals applied to a real project

## 👨‍🎓 Author

**Joaquín Orradre** - Student practicing MLOps and Continuous Integration

---

*This is an educational project focused on learning the fundamentals of Continuous Integration and MLOps best practices.*
