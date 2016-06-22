"""
stmt2 - Conversion tool between statement formats.

Usage:
    stmt2 convert <from_fmt> [<file_from>] to <to_fmt> [<file_to>]
    stmt2 list providers
    stmt2 (-h | --help)

Commands:
    convert             Convert one statement format to another
    list providers      List the providers that are implemented

Arguments:
    <file_from>         (Optional) file that the statement is being read from
    <file_to>           (Optional) file that the statement is being written to
    <from_fmt>          Format that is being converted from
    <to_fmt>            Format that is being converted to

Options:
    -h --help           Show this screen
"""

import sys

from docopt import docopt

from account_tools import provider
from account_tools.provider import PROVIDERS
from account_tools.util import input_stderr

_WRITE_PARAMS = {
    'prompt_fun': input_stderr
}


def convert_statement(istream, from_fmt, to_fmt, ostream):
    if from_fmt not in provider.PROVIDERS:
        raise ValueError("No such format '{}'".format(from_fmt))
    elif to_fmt not in provider.PROVIDERS:
        raise ValueError("No such format '{}'".format(to_fmt))

    from_provider = provider.PROVIDERS[from_fmt]
    to_provider = provider.PROVIDERS[to_fmt]

    if not from_provider.read or not from_provider.to_unified:
        raise NotImplementedError("Reading from provider format '{}' not implemented".format(from_fmt))
    elif not to_provider.write or not to_provider.from_unified:
        raise NotImplementedError("Writing to provider format '{}' not implemented".format(to_fmt))

    entries_from = from_provider.read(istream)
    unified_entries = list(map(from_provider.to_unified, entries_from))
    entries_to = list(map(to_provider.from_unified, unified_entries))
    to_provider.write(entries_to, ostream, **_WRITE_PARAMS)

    return len(entries_to)


def list_providers(opts):
    # TODO be more fancy
    for name in sorted(PROVIDERS.keys()):
        print(name)


def convert_files(opts):
    from_fmt = opts['<from_fmt>']
    to_fmt = opts['<to_fmt>']

    from_filename = opts['<file_from>'] or '-'
    to_filename = opts['<file_to>'] or '-'

    from_stream, to_stream = None, None
    try:
        from_stream = sys.stdin if from_filename == '-' else open(from_filename, 'r', encoding='utf-8')
        to_stream = sys.stdout if to_filename == '-' else open(to_filename, 'w', encoding='utf-8')

        convert_statement(from_stream, from_fmt, to_fmt, to_stream)
    finally:
        if from_stream and not from_filename == '-':
            from_stream.close()
        if to_stream and not to_filename == '-':
            to_stream.close()


def main():
    opts = docopt(__doc__)

    if opts["list"] and opts["providers"]:
        return list_providers(opts)
    elif opts["convert"]:
        return convert_files(opts)
    else:
        raise NotImplementedError("Other options are not implemented - this is a bug")


if __name__ == '__main__':
    sys.exit(main())
