# -*- coding: utf-8 -*-

import pytest

from gridsync.tahoe import Tahoe, decode_introducer_furl


@pytest.fixture(autouse=True)
def mock_appdata(monkeypatch):
    monkeypatch.setenv('APPDATA', 'C:\\Users\\test\\AppData\\Roaming')


@pytest.fixture(scope='module')
def tahoe(tmpdir_factory):
    return Tahoe(str(tmpdir_factory.mktemp('tahoe')))


def test_decode_introducer_furl():
    furl = 'pb://abc234@example.org:12345/introducer'
    assert decode_introducer_furl(furl) == ('abc234', 'example.org:12345')


def test_decode_introducer_furl_no_host_separator():
    furl = 'pb://abc234example.org:12345/introducer'
    with pytest.raises(AttributeError):
        assert decode_introducer_furl(furl)


def test_decode_introducer_furl_no_port_separator():
    furl = 'pb://abc234@example.org12345/introducer'
    with pytest.raises(AttributeError):
        assert decode_introducer_furl(furl)


def test_decode_introducer_furl_invalid_char_in_connection_hint():
    furl = 'pb://abc234@exam/ple.org:12345/introducer'
    with pytest.raises(AttributeError):
        assert decode_introducer_furl(furl)


def test_decode_introducer_furl_tub_id_not_base32():
    furl = 'pb://abc123@example.org:12345/introducer'
    with pytest.raises(AttributeError):
        assert decode_introducer_furl(furl)


def test_tahoe(tahoe):
    assert tahoe


def test_tahoe_name(tahoe):
    assert tahoe.name
