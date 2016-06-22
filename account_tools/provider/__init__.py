from collections import namedtuple

from account_tools.provider.crunch import StatementEntry as CrunchEntry, from_unified as crunch_from_unified, write_crunch
from account_tools.provider.metrobank import StatementEntry as MetrobankEntry, to_unified as metrobank_to_unified
from account_tools.provider.unified import read_unified, write_unified
from account_tools.util import read_csv_into_namedtuples


class Provider(namedtuple('_Provider', ['name', 'read', 'write', 'to_unified', 'from_unified'])):
    """A provider of statement entries that has a particular format and conversion functions"""
    pass


PROVIDERS = {f.name: f for f in [
    Provider(name='crunch',
             read=None,
             write=write_crunch,
             to_unified=None,
             from_unified=crunch_from_unified),
    Provider(name='metrobank',
             read=lambda s: read_csv_into_namedtuples(s, MetrobankEntry),
             write=None,
             to_unified=metrobank_to_unified,
             from_unified=None),
    Provider(name='unified',
             read=read_unified,
             write=write_unified,
             to_unified=lambda _: _,
             from_unified=lambda _: _),
]}
