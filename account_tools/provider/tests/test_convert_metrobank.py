import datetime
from decimal import Decimal
from pkgutil import get_data

from io import StringIO

from account_tools.provider.metrobank import StatementEntry, to_unified
from account_tools.util import read_csv_into_namedtuples


def test_read_metrobank():
    """
    Simple test for reading a Metro Bank statement
    """
    ts = StringIO(get_data(__name__, 'metrobank/Transaction_01.01.1970.csv').decode('utf-8'))
    statements = read_csv_into_namedtuples(ts, StatementEntry)

    assert len(statements) == 3
    assert statements[0] == StatementEntry('01/01/1970', '1 JAN 70 FOOBAR LTD', 'Card Purchase', '0.00', '23.60')
    assert statements[1] == StatementEntry('13/01/1970', 'EE N T-MOBILE', 'Direct Debit', '0.00', '10.00')
    assert statements[2] == StatementEntry('15/01/1970', '', 'Credit Adjustment', '0.00', '0.40')


def test_convert_unified_metrobank():
    """
    Test for converting an entry from Metro Bank -> Unified format
    """
    unified = to_unified(StatementEntry('01/01/1970', '1 JAN 70 FOOBAR LTD', 'Card Purchase', '0.00', '23.60'))

    assert unified.amount is None
    assert unified.balance is None
    assert unified.credit.is_zero()
    assert unified.debit == Decimal('23.60')
    assert unified.currency is None
    assert unified.date == datetime.date(1970, 1, 1)
    assert unified.ref == '1 JAN 70 FOOBAR LTD'
    assert unified.method == 'Card Purchase'
