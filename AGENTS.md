# Project Conventions

## Error Handling
- **Never ignore errors:** You must NEVER leave an empty catch block.
- **Centralized Error Reporting:** The project MUST have a single, centralized error-reporting function (e.g. `reportError`, `captureException`, or equivalent). All code paths that handle unexpected errors MUST funnel through this function — never call `console.error` or `Sentry.captureException` directly at the call site.
- **Sentry-aware:** If the project already uses Sentry, the centralized function MUST report to Sentry. If Sentry is not set up, it MUST log the error with enough context (message, stack, relevant metadata). The call site should not know or care which backend is active.
- **No silent failures:** Every `catch` block, every `.catch()`, every error callback that is not an expected/recoverable condition MUST call the centralized error-reporting function. "Out of scope" is not an excuse to swallow — at minimum, report and move on.

## Testing
- **Tests Must Earn Their Place:** If you write a test, it must test something you actually implemented or changed — your own logic, your own edge cases. Do not write tests that just exercise external libraries or restate what the library's own tests already cover. A test that doesn't catch a real bug in your code is noise.
- **Test Beyond Automation:** Passing lint and unit tests is the baseline, not the finish line. After automated checks pass, do a manual sanity check: build the project, trace the code path you changed, think about what a user would actually hit.
