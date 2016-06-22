from io import StringIO
from datetime import date

from account_tools.provider.crunch import *
from account_tools.provider.unified import StatementEntry as UnifiedEntry


def test_convert_unified_to_crunch():
    """
    Test conversion of Unified -> Crunch format
    """
    crunch_entry = from_unified(UnifiedEntry(date(2000, 1, 1), 'ARef', amount=Decimal('83105.31'), method='Blah'))
    assert crunch_entry == StatementEntry(Date='01/01/2000', Reference='ARef', Paid_In='83105.31', Paid_Out='',
                                          Balance='')


def test_prompt_closing_balance_on_write():
    """
    Test that closing balance is prompted on conversion
    """
    entries = [StatementEntry(Date='01/01/2000', Reference='ARef', Paid_In='83105.31', Paid_Out='',
                              Balance='')]
    ostream = StringIO()
    answers = (_ for _ in ['c', '25.6'])
    prompt_answers = lambda _: answers.__next__()
    write_crunch(entries, ostream, prompt_fun=prompt_answers)
    ostream.seek(0)
    lines = ostream.readlines()

    assert lines[0] == "Date,Reference,Paid In,Paid Out,Balance\r\n"
    assert lines[1] == "01/01/2000,ARef,83105.31,,25.6\r\n"
