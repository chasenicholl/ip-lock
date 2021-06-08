"""Exceptions"""


class UnsupportedDNSProvider(Exception):
    """Base class for exceptions in this module."""

    pass


class InvalidAuthToken(Exception):
    """Base class for exceptions in this module."""

    pass


class DNSZoneNameNotFound(Exception):
    """Base class for exceptions in this module."""

    pass


class DNSRecordsError(Exception):
    """Base class for exceptions in this module."""

    pass
