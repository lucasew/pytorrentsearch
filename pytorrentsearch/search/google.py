import re

LINK_REGEXP = re.compile("<a [^>]*href=\"([^\"]*)\"")

def query_results(query: str, page=1):
    from pytorrentsearch.utils import request, get_url_content, quote, status, min_wait
    from time import time, sleep
    page_links = []
    min_waiter = min_wait(5)
    while True:
        for link in page_links:
            yield link
        next(min_waiter)
        status("Fetching Google result page...")
        content = get_url_content(f"https://www.google.com/search?q={quote(query)}&start={(page-1)*20}")
        with open("/tmp/preview.html", 'w') as f:
            f.write(content)
        page_links = []
        for link in LINK_REGEXP.findall(content):
            if link.startswith("/url"):
                if link.find("http") != -1:
                    link = link[link.find("http"):]
                else:
                    continue
                if link.find("&amp"):
                    link = link[0:link.find("&amp")]
            if link.startswith("http") and link.find("google.com") == -1:
                page_links.append(link)
        if len(page_links) == 0:
            break
