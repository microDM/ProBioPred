# Contributing to ProBioPred

Thank you for your interest in contributing to ProBioPred!

## How to contribute

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create a branch** for your changes: `git checkout -b your-feature-name`
4. **Make your changes** and test them
5. **Commit** with a clear message: `git commit -m "Add/fix: description"`
6. **Push** to your fork: `git push origin your-feature-name`
7. **Open a Pull Request** against the `main` branch

## Development setup

```bash
conda create -n probiopred python=3.10
conda activate probiopred
conda install -c bioconda blast
conda install -c conda-forge libsvm
pip install -e .
```

You will also need RGI (Resistance Gene Identifier) for antibiotic resistance detection. See the main README for full installation instructions.

## Code style

- Use Python 3
- Follow PEP 8 where practical
- Add docstrings to new functions

## Reporting issues

If you find a bug or have a suggestion, please open an issue on GitHub with:

- A clear description of the problem
- Steps to reproduce (for bugs)
- Your environment (OS, Python version, etc.)

## Questions

For questions about ProBioPred, you can open an issue or contact the maintainers.
