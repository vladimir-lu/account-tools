from datetime import date
from io import StringIO

from account_tools.provider.unified import *


def test_write_unified_format():
    """
    Test that writing a single unified record produces the output expected
    """
    ostream = StringIO()
    unified_record = StatementEntry(date(1970, 1, 1), '1 JAN 70 FOOBAR LTD', debit=Decimal('23.6'),
                                    method='Card Purchase')

    write_unified([unified_record], ostream)
    ostream.seek(0)
    lines = ostream.readlines()

    assert lines[0] == "date,ref,amount,balance,credit,currency,debit,method\r\n"
    assert lines[1] == "1970-01-01,1 JAN 70 FOOBAR LTD,,,0,,23.6,Card Purchase\r\n"
