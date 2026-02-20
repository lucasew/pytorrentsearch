# Project Conventions

This project uses `mise` for task management and `trunk` for linting/formatting.

## Task Management

- ALWAYS use `mise run` to execute tasks.
- `mise.toml` is the source of truth for tasks.
- Standard tasks: `lint`, `fmt`, `test`, `codegen`, `install`, `ci`.

## Tooling

- Tools are pinned in `mise.toml`.
- Do NOT install tools manually; let `mise` manage them.
- `trunk` is used for linting and formatting.

## Error Handling

- All unexpected errors MUST be reported via `pytorrentsearch.error.report_error`.
- Do NOT use `print(e)` or `logging.error(e)` directly for unexpected errors.
- Do NOT swallow errors silently.
- Every `catch` block (or `except` block) MUST call `report_error`.

## Code Style

- Follow `trunk check` and `trunk fmt` guidelines.
- Use explicit types (mypy).
