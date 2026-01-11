# Gemini Agent Rules for RAE Project

This document contains key operational rules for AI agents working on the RAE (Robotic Agent Emulation) project. These rules are designed to ensure efficient, non-interactive, and token-conscious operation within the project's ecosystem.

## 🚨 Critical Rules - MUST FOLLOW

### 1. **No Interactive Commands**
- **NEVER** use interactive commands or editors that require user input and block automation.
- **FORBIDDEN**: `nano`, `vim`, `vi`, `emacs`, `less`, `more`, `git add -i`, `git commit` (without `-m`), `git rebase -i`.
- **ALLOWED**: Use non-interactive tools like `cat`, `head`, `tail`, `grep`, `sed`, `git add .`, `git commit -m "message"`.

### 2. **Hybrid Testing Strategy (Token-Efficient)**
The project uses a smart hybrid CI workflow to save tokens and time.

- **Quick Tests**: Run automatically on commits to `feature/*` branches. Use this for iterative development.
- **Full Tests**: Run automatically on PRs, pushes to `main`/`develop`, or when a commit message includes the `[full-test]` tag. Use this before creating a pull request or when refactoring core code to catch regressions.

### 3. **Commit Message Format**
Adhere to the following format for all commits:
```
type(scope): short description

[optional detailed body]

[optional tags like [full-test]]
```
- **Types**: `feat`, `fix`, `test`, `refactor`, `docs`, `ci`, `perf`, `chore`.

### 4. **RAE & Communication**
- The project follows a "RAF-First" (RAE-First) ideology where communication should pass through the RAE system to conserve tokens and maintain context.
- Avoid asking the same questions repeatedly.
- If direct RAE/MCP communication is not available, use `curl` for reading and writing data as a temporary measure.
- The ultimate goal is to communicate with RAE via MCP (Master Control Protocol).

### 5. **General Principles**
- Prioritize token and time efficiency in all operations.
- For simple tasks, use "cheap" methods (like quick tests) to conserve resources.
