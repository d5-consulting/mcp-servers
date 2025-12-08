# Claude Development Guidelines

This document contains guidelines for AI assistants working on this codebase.

## Workflow

### Use Git Worktrees for Changes

Always create a new worktree for each branch to keep work isolated:

```bash
git worktree add ../dirname -b branch-name
```

This keeps your main working directory clean and allows you to work on multiple features simultaneously.

## Code Principles

### Keep the Codebase Minimum, Clean and Consistent

- Only add code that is necessary for the feature or fix
- Remove unused imports, functions, and dependencies
- Follow existing patterns and conventions in the codebase
- Maintain consistency in:
  - Code style and formatting
  - Naming conventions
  - Project structure
  - Documentation style

### Always Test

- Write tests for new features and bug fixes
- Run the test suite before committing changes
- Ensure all tests pass before creating pull requests
- Update existing tests when modifying functionality
