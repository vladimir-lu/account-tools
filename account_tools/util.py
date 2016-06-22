from csv import DictReader

import sys


def read_csv_into_namedtuples(istream, namedtuple):
    """
    Read a csv stream into a list of namedtuples
    """
    reader = DictReader(istream)
    adapt_fieldnames_to_tuple(reader, namedtuple)
    return [namedtuple(**r) for r in reader]


def adapt_fieldnames_to_tuple(reader, namedtuple):
    """
    Modify the passed in DictReader with expected field names from a namedtuple, after verifying whether it actually has
    the right field names
    """
    got_fieldnames = reader.fieldnames
    expected_fieldnames = namedtuple._fields

    if are_expected_fieldnames(got_fieldnames, expected_fieldnames):
        reader.fieldnames = expected_fieldnames
    else:
        raise ValueError("Unexpected fieldnames: got={}, expected={}".format(got_fieldnames, expected_fieldnames))


def are_expected_fieldnames(fieldnames, expected_fieldnames):
    """
    Check whether field names correspond to expected field names by stripping their contents and replacing non-python
    friendly characters with underscores
    """
    norm_fieldnames = map(lambda f: f.strip().replace(' ', '_') if f else '', fieldnames)
    return list(norm_fieldnames) == list(expected_fieldnames)


def input_stderr(prompt):
    """
    Read a line of user input (like input) but unlike input, use stderr for prompting
    """
    print(prompt, file=sys.stderr, end=' ', flush=True)
    return sys.stdin.readline().strip('\n')