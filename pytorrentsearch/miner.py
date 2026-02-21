import re

MAGNET_REGEXP = re.compile("magnet:\\?xt=[^\"']*")

nontorrent_blockwords = [
    "lumendatabase.org",
    "disney.com.br",
    "reddit.com",
    "facebook.com",
    "google.com",
    "youtube.com",
    "youtu.be",
    "wikipedia.org",
    "instagram.com",
    "ifunny.co",
    "9gag.com",
]


def is_common_nontorrent_site(url: str):
    """
    Checks if a URL belongs to a site known to not host torrents.

    This filter prevents the crawler from wasting resources on sites like
    Google, Facebook, or Reddit, which are unlikely to contain magnet links.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL contains a blocked domain, False otherwise.
    """
    for nontorrent_blockword in nontorrent_blockwords:
        if url.find(nontorrent_blockword) > 0:
            return True
    return False


def mine_magnet_links(url: str):
    """
    Extracts magnet links from a given URL's content.

    Fetches the page content and scans for strings matching the magnet link
    pattern. It automatically skips known non-torrent sites.

    Args:
        url (str): The web page URL to scrape.

    Returns:
        list[str]: A list of found magnet links, decoded and sanitized.
                   Returns an empty list if the site is blocked.

    Side Effects:
        - Logs status messages to stderr via `utils.status`.
        - Performs an HTTP request to fetch the URL content.
    """
    from urllib.parse import unquote

    from pytorrentsearch.utils import get_url_content, status

    if is_common_nontorrent_site(url):
        status(f"[crawler/ENONTORRNET] {url}")
        return []
    status(f"[crawler/fetch] {url}")
    content = get_url_content(url)
    ret = []
    for occurence in MAGNET_REGEXP.findall(content):
        link = unquote(occurence)
        link = link.replace("&#038;", "&")
        link = link.replace("&amp;", "&")
        ret.append(link)
    return ret


def parse_magnet_link(url: str):
    """
    Parses a magnet URI into its constituent components.

    Extracts the display name (dn), info hash (xt), and trackers (tr)
    from the magnet link query parameters.

    Args:
        url (str): The magnet URI string.

    Returns:
        dict: A dictionary containing:
            - info_hash (str): The BTIH hash.
            - name (str): The display name of the torrent, or "< NO NAME >"
              if missing.
            - trackers (list[str]): A list of tracker URLs.
    """
    from urllib.parse import parse_qs, urlparse

    query = urlparse(url).query
    query_params = parse_qs(query)
    info_hash = query_params["xt"][0].replace("urn:", "").replace("btih:", "")
    name = "< NO NAME >"
    if query_params.get("dn") is not None:
        name = query_params["dn"][0]
    trackers = []
    if query_params.get("tr") is not None:
        trackers = query_params["tr"]
    return dict(info_hash=info_hash, name=name, trackers=trackers)


def prettyprint_magnet(magnet: str):
    """
    Prints a formatted summary of a magnet link to stdout.

    Displays the torrent name, tracker count, info hash, and the raw magnet
    link.

    Args:
        magnet (str): The magnet URI string to print.

    Side Effects:
        - Writes formatted text to stdout.
    """
    parsed = parse_magnet_link(magnet)
    len_trackers = len(parsed["trackers"])
    print(
        f"{parsed['name']}\nTrackers: {str(len_trackers).rjust(3)} InfoHash: {parsed['info_hash']}\n{magnet}\n"  # noqa: E501
    )
