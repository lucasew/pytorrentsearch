import sys
import traceback
from typing import Optional


def report_error(exception: Exception, context: Optional[dict] = None):
    """
    Centralized error reporting.

    Currently logs to stderr. Should be updated to use Sentry or similar in
    the future.
    """
    if context:
        print(f"Error Context: {context}", file=sys.stderr)
    traceback.print_exception(
        type(exception), exception, exception.__traceback__, file=sys.stderr
    )
