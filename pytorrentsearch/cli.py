"""CLI interface for pytorrentsearch project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""


def main():  # pragma: no cover
    from argparse import ArgumentParser
    from pytorrentsearch.search import yandex, google, duckduckgo
    from pytorrentsearch.utils import multi_iterator_pooler

    parser = ArgumentParser("pytorrentsearch")
    parser.add_argument("query", type=str)
    args = parser.parse_args()
    print(args)

    iterators = []
    for search_backend in [ yandex, google, duckduckgo ]:
        iterators.append(search_backend.query_results(args.query))

    main_iterator = multi_iterator_pooler(*iterators)
    for item in main_iterator:
        print(item)
