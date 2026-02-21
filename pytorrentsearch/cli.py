"""CLI interface for pytorrentsearch project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""

from argparse import ArgumentParser

from pytorrentsearch.error import report_error
from pytorrentsearch.miner import mine_magnet_links, prettyprint_magnet
from pytorrentsearch.search import duckduckgo, google, yandex
from pytorrentsearch.utils import multi_iterator_pooler


def main():  # pragma: no cover
    parser = ArgumentParser("pytorrentsearch")
    parser.add_argument("query", type=str)
    args = parser.parse_args()

    if args.query.startswith("http"):
        try:
            for magnet in mine_magnet_links(args.query):
                prettyprint_magnet(magnet)
        except Exception as e:
            report_error(e)
            exit(1)
        exit(0)

    iterators = []
    for search_backend in [yandex, google, duckduckgo]:
        iterators.append(search_backend.query_results(args.query))

    visited_urls = {}

    url_iterator = multi_iterator_pooler(*iterators)
    for url in url_iterator:
        if visited_urls.get(url) is not None:
            continue
        try:
            magnets = mine_magnet_links(url)
            for magnet in magnets:
                prettyprint_magnet(magnet)
        except Exception as e:
            report_error(e)
            continue
        finally:
            visited_urls[url] = True
