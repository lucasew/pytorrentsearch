import sys
import traceback
from typing import Any, Optional


def report_error(error: Any, context: Optional[dict[str, Any]] = None) -> None:
    """
    Centralized error reporting function.

    Args:
        error: The exception or error object.
        context: Optional dictionary with additional context.
    """
    if context is None:
        context = {}

    # Print to stderr with a consistent format
    print(f"[ERROR] Unexpected error: {error}", file=sys.stderr)
    if context:
        print(f"[ERROR] Context: {context}", file=sys.stderr)

    traceback.print_exc(file=sys.stderr)

    # Future: Integrate with Sentry or other error reporting services here.
