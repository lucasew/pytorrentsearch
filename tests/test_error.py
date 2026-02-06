from pytorrentsearch.error import report_error


def test_report_error(capsys):
    try:
        raise ValueError("test error")
    except ValueError as e:
        report_error(e)

    captured = capsys.readouterr()
    assert "ValueError: test error" in captured.err


def test_report_error_with_context(capsys):
    try:
        raise ValueError("test error")
    except ValueError as e:
        report_error(e, context={"foo": "bar"})

    captured = capsys.readouterr()
    assert "ValueError: test error" in captured.err
    assert "Error Context: {'foo': 'bar'}" in captured.err
