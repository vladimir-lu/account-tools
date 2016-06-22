"""
Provider module that corresponds to an idealized "unified" statement format specific to this application
"""

import csv
import datetime
from decimal import Decimal


_ZERO = Decimal('0')


class StatementEntry(object):
    """
    A statement that represents a unified version of all the statements that are supported
    """

    def __init__(self, date, ref, amount=None, balance=None, currency=None, credit=None, debit=None, method=None):
        """
        Create a new unified statement entry
        :param date: A `datetime.date` which is the date of the transaction
        :param ref: A string reference
        :param balance: The positive/negative balance change (if it is set, credit/debit cannot be specified)
        :param credit: The amount of money credited to the account (money goes in)
        :param currency: The ISO code representing the currency of the transaction
        :param debit: The amount of money debited from the account (money goes out)
        :param method: Description of the method used in the transfer
        """
        if not isinstance(date, datetime.date):
            raise ValueError("The date should be a datetime.date")
        elif not isinstance(ref, str):
            raise ValueError("The reference must be a string")
        elif currency and not isinstance(currency, str):
            raise ValueError("The currency must be a string")
        elif amount and (debit or credit):
            raise ValueError("Amount specified when debit or credit where also specified")
        elif not (amount or credit or debit):
            raise ValueError("Amount should be specified")
        amount = Decimal(amount) if amount else None
        balance = Decimal(balance) if balance else None
        credit = Decimal(credit) if credit else _ZERO
        debit = Decimal(debit) if debit else _ZERO
        method = method if method else None

        self.date = date
        self.ref = ref
        self.amount = amount
        self.balance = balance
        self.credit = credit
        self.currency = currency
        self.debit = debit
        self.method = method

    def amount_as_debit_credit(self):
        """
        Calculate the entry amount as a (debit, credit) pair

        If amount is not present, return the (debit, credit) pair
        :rtype: (Decimal, Decimal)
        """
        if self.amount is not None:
            return (_ZERO, self.amount) if self.amount > _ZERO else (self.amount, _ZERO)
        else:
            return self.debit, self.credit


def read_unified(istream):
    raise NotImplementedError()


def write_unified(unified_recs, ostream):
    header = ('date', 'ref', 'amount', 'balance', 'credit', 'currency', 'debit', 'method')
    writer = csv.DictWriter(ostream, fieldnames=header)
    writer.writeheader()
    for r in unified_recs:
        writer.writerow(vars(r))
