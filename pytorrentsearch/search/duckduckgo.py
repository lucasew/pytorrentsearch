import re

LINK_REGEXP = re.compile("<a [^>]*href=\"([^\"]*)\"")

def query_results(query: str, page=1):
    from pytorrentsearch.utils import request, get_url_content, quote, status, min_wait
    page_links = []
    min_waiter = min_wait(5)
    while True:
        for link in page_links:
            yield link
        next(min_waiter)
        status("Fetching DuckDuckGo result page...")
        content = get_url_content(f"https://html.duckduckgo.com/html/?q={quote(query)}&s={(page-1)*20}")
        with open("/tmp/preview.html", 'w') as f:
            f.write(content)
        page_links = set()
        for link in LINK_REGEXP.findall(content):
            if link.startswith("http"):
                page_links.add(link)
        if len(page_links) == 0:
            break
