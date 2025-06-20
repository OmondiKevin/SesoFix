# Contributing to SesoFix

Thank you for your interest in contributing to SesoFix! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct: be respectful, considerate, and collaborative.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git

### Setting Up Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/SesoFix.git
   cd SesoFix
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following the coding standards below

3. Add tests for your changes if applicable

4. Run tests to ensure your changes don't break existing functionality:
   ```bash
   python -m unittest discover tests
   ```

5. Commit your changes:
   ```bash
   git commit -m "Add your meaningful commit message here"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a pull request from your fork to the main repository

## Coding Standards

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Write docstrings for all functions, classes, and modules
- Include type hints where appropriate
- Keep functions focused on a single responsibility
- Add comments for complex logic

## Pull Request Process

1. Ensure your code follows the coding standards
2. Update documentation if necessary
3. Include a clear description of the changes in your pull request
4. Link any related issues in your pull request description
5. Be responsive to feedback and be willing to make changes if requested

## Adding New Features

When adding new features, please consider the following:

1. Discuss major changes in an issue before implementing
2. Ensure the feature is well-tested
3. Update documentation to reflect the new feature
4. Consider backward compatibility

## Reporting Bugs

When reporting bugs, please include:

1. A clear description of the bug
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Environment details (OS, Python version, etc.)
6. Any relevant logs or error messages

## Documentation

Improvements to documentation are always welcome! This includes:

- Fixing typos or clarifying existing documentation
- Adding examples or tutorials
- Improving API documentation
- Adding diagrams or visual aids

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.