"""
Provider module that corresponds to the Crunch Accounting site (www.crunch.co.uk)
"""
from csv import writer
from decimal import Decimal

from collections import namedtuple


class StatementEntry(namedtuple('_StatementEntry', ['Date', 'Reference', 'Paid_In', 'Paid_Out', 'Balance'])):
    pass


_HEADER_FIELDS = tuple(map(lambda f: f.replace('_', ' '), StatementEntry._fields))


def from_unified(entry):
    """
    Converter from a unified entry to a `StatementEntry`
    """
    date = entry.date.strftime('%d/%m/%Y')
    ref = entry.ref
    (paid_out, paid_in) = entry.amount_as_debit_credit()
    paid_in = paid_in or ''
    paid_out = paid_out or ''
    balance = entry.balance or ''

    return StatementEntry(date, ref, str(paid_in), str(paid_out), str(balance))


def _fixup_balance(entries, prompt_fun):
    """
    Validate Crunch-specific logic in the entries, namely that one of the entries *must* contain a balance column
    """
    if not len(entries):
        return entries
    elif any(_.Balance for _ in entries):
        return entries

    assert prompt_fun

    # FIXME there should be no assumption that the statement entries are sorted or if they are then make it really clear how
    start_or_close = prompt_fun("No balance was found. Would you like to provide a (s)tarting or (c)losing balance?")
    if start_or_close not in ('s', 'c'):
        raise ValueError("Response '{}' was not understood".format(start_or_close))

    idx = 0 if start_or_close == 's' else -1
    balance = Decimal(prompt_fun("Balance for entry {}:".format(entries[idx])))
    entries[idx] = entries[idx]._replace(Balance=str(balance))

    return entries


def write_crunch(entries, ostream, prompt_fun=None, **kwargs):
    """
    Write a Crunch-format statement

    :type entries: list of StatementEntry
    """
    entries = _fixup_balance(entries, prompt_fun)
    w = writer(ostream)
    w.writerow(_HEADER_FIELDS)
    for e in entries:
        w.writerow(tuple(e))
