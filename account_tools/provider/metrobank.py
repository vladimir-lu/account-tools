"""
Provider module that corresponds to Metro Bank UK (www.metrobankonline.co.uk)
"""
import datetime

from collections import namedtuple

from account_tools.provider.unified import StatementEntry as UnifiedEntry


class StatementEntry(namedtuple('_StatementEntry', ['Date', 'Reference', 'Transaction_Type', 'Money_In', 'Money_Out'])):
    pass


def to_unified(entry):
    """
    Convert to a unified entry
    """
    assert isinstance(entry, StatementEntry)
    date = datetime.datetime.strptime(entry.Date, '%d/%m/%Y').date()

    return UnifiedEntry(date, entry.Reference, method=entry.Transaction_Type, credit=entry.Money_In,
                        debit=entry.Money_Out)
