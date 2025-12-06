# Contributing to The Wizard's Keep

Thank you for your interest in contributing! This project is designed to be educational, and contributions that help others learn are especially welcome.

## How Can I Contribute?

### 🐛 Reporting Bugs
Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### 💡 Suggesting Features
Have an idea? Open an issue with:
- Clear description of the feature
- Why it would be useful
- How it fits the educational goals

### 📝 Improving Documentation
Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add more examples
- Improve code comments
- Create tutorials or guides

### 🔨 Code Contributions
Ready to code? Great!

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```powershell
   git clone https://github.com/yourusername/the-wizards-keep.git
   cd the-wizards-keep
   ```

3. Run setup script:
   ```powershell
   .\scripts\setup.ps1
   ```

4. Create a branch:
   ```powershell
   git checkout -b feature/your-feature-name
   ```

## Coding Standards

### Python Code
- Follow PEP 8 style guide
- Use type hints
- Add docstrings to functions/classes
- Keep functions focused and small
- Write tests for new features

Run formatters before committing:
```powershell
cd backend
black app/ tests/
isort app/ tests/
flake8 app/ tests/
mypy app/
```

### JavaScript Code
- Use ES6+ features
- Add comments for complex logic
- Keep functions pure when possible
- Handle errors gracefully

### Documentation
- Use Markdown for docs
- Include code examples
- Explain the "why", not just the "how"
- Consider beginners - avoid assuming knowledge

## Testing

All code changes should include tests:

```powershell
# Run tests
cd backend
pytest tests/ -v

# Run with coverage
pytest --cov=app --cov-report=html
```

Aim for >80% test coverage for new code.

## Commit Messages

Write clear commit messages:

```
feat: add inventory sorting feature

- Add sort_inventory function in game_engine.py
- Update API endpoint to accept sort parameter
- Add tests for sorting functionality
- Update documentation
```

Format: `type: short description`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test changes
- `refactor`: Code refactoring
- `style`: Formatting changes
- `chore`: Build/tool changes

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Run all tests and linters
4. Update README.md if needed
5. Create pull request with:
   - Clear description
   - Link to related issues
   - Screenshots (if UI changes)

### PR Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts

## Educational Contributions

This project is meant to teach! Great educational contributions:

### Add Learning Resources
- Tutorial documents
- Video walkthrough links
- Architecture diagrams
- Code explanation comments

### Improve Examples
- More comprehensive test examples
- Additional API endpoint examples
- Docker/Kubernetes examples

### Game Content
- New levels or locations
- Additional items or enemies
- Quest storylines
- Boss encounters

## Code Review

All submissions require review. Reviewers will check:
- Code quality and style
- Test coverage
- Documentation
- Educational value

Be patient - reviews may take a few days!

## Community Guidelines

- Be respectful and constructive
- Help others learn
- Share knowledge freely
- Give credit where due
- Focus on the educational mission

## Questions?

Open an issue or start a discussion! We're here to help.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make this project better for learners everywhere! 🎓
