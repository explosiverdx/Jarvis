# Contributing to Jarvis

Thank you for your interest in contributing to Jarvis! We welcome contributions of all kinds.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Jarvis.git`
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to your fork: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies with dev tools
pip install -r requirements.txt
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black jarvis/
flake8 jarvis/
pylint jarvis/
```

## Code Guidelines

- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings for all modules and functions
- Add unit tests for new features
- Keep functions focused and modular

## Creating Plugins

To create a new plugin:

1. Create a new file in `jarvis/automation/plugins/`
2. Inherit from `Plugin` base class
3. Implement `can_handle()` and `execute()` methods
4. Register the plugin in the plugin manager

Example:

```python
from jarvis.automation.plugins.base import Plugin

class WeatherPlugin(Plugin):
    def __init__(self):
        super().__init__("weather")
    
    def can_handle(self, intent):
        return intent == "weather"
    
    def execute(self, entities):
        # Your implementation
        return "Weather result"
```

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages or logs

## Code Review Process

1. All PRs require at least one review
2. CI/CD pipeline must pass
3. Code coverage should not decrease
4. Follow the project's coding standards

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue or contact the maintainers!
