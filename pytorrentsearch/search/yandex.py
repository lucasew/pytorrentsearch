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
        status("Fetching Yandex result page...")
        content = get_url_content(f"https://yandex.com/search?text={quote(query)}&p={page}")
        with open("/tmp/preview.html", 'w') as f:
            f.write(content)
        page_links = set()
        for link in LINK_REGEXP.findall(content):
            # if link.startswith("http"):
            page_links.add(link)
        if len(page_links) == 0:
            break
        if "smartcaptcha" in " ".join(page_links):
            status("Yandex asked captcha, giving up")
            break
