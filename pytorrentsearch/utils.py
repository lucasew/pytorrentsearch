def status(message: str):
    """
    Prints a status message to stderr.

    Used for logging progress updates without interfering with stdout output.

    Args:
        message (str): The message to display.
    """
    from sys import stderr

    print(f"[*] {message}", file=stderr)


def request(url: str, timeout=10):
    """
    Performs an HTTP request with a standard User-Agent.

    Args:
        url (str): The URL to request.
        timeout (int, optional): Request timeout in seconds. Defaults to 10.

    Returns:
        http.client.HTTPResponse: The response object.
    """
    from urllib.request import Request, urlopen

    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"  # noqa: E501
        },
    )
    res = urlopen(req, timeout=timeout)
    return res


def get_url_content(url: str, timeout=10):
    """
    Fetches and decodes the content of a URL.

    Args:
        url (str): The URL to fetch.
        timeout (int, optional): Request timeout in seconds. Defaults to 10.

    Returns:
        str: The UTF-8 decoded content of the response.
    """
    return request(url, timeout=timeout).read().decode("utf8")


def multi_iterator_pooler(*iterators):
    """
    Combines multiple iterators into a single stream using a thread pool.

    Each iterator runs in its own thread and feeds into a shared queue.
    This allows parallel consumption of multiple sources (e.g., different
    search engines). Exceptions in worker threads are reported via
    `pytorrentsearch.error.report_error`.

    Args:
        *iterators: Variable number of iterator objects.

    Yields:
        Any: Items produced by the input iterators, in the order they arrive
             in the queue.
    """
    import queue
    from threading import Thread
    from time import sleep

    q = queue.Queue(maxsize=len(iterators))
    threads = []

    def worker(iterator):
        from pytorrentsearch.error import report_error

        while True:
            try:
                item = next(iterator)
            except StopIteration:
                break
            except Exception as e:
                report_error(e)
                break
            try:
                q.put(item)
            except Exception as e:
                report_error(e)
                break

    for iterator in iterators:
        threads.append(Thread(target=worker, args=[iterator]))
    for thread in threads:
        thread.start()
    while True:
        if not q.empty():
            obj = q.get()
            q.task_done()
            yield obj
        keep_going = False
        for thread in threads:
            if thread.is_alive():
                keep_going = True
        if keep_going:
            sleep(0.1)


def min_wait(seconds):
    """
    A generator that enforces a minimum wait time between iterations.

    Useful for rate-limiting loop executions. It yields `None` immediately,
    then sleeps if necessary to ensure the specified interval has passed since
    the last yield.

    Args:
        seconds (float): The minimum number of seconds to wait between yields.

    Yields:
        None: At each iteration.
    """
    from time import sleep, time

    last_time = time()
    yield None
    while True:
        timediff = time() - last_time
        if timediff < seconds:
            sleep(seconds - timediff)
        yield None
