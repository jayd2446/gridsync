# -*- coding: utf-8 -*-

import difflib
import os
import sys
if sys.version_info >= (3, 4):
    from importlib import reload

import gridsync


def test_the_approval_of_RMS():  # :)
    assert gridsync.__license__.startswith('GPL')


def test_pkgdir(monkeypatch):
    monkeypatch.setattr("sys.frozen", False, raising=False)
    assert gridsync.pkgdir == os.path.dirname(
        os.path.realpath(gridsync.__file__))


def test_frozen_pkgdir(monkeypatch):
    monkeypatch.setattr("sys.frozen", True, raising=False)
    reload(gridsync)
    assert gridsync.pkgdir == os.path.dirname(os.path.realpath(sys.executable))


def test_append_tahoe_bundle_to_PATH(monkeypatch):
    monkeypatch.setattr("sys.frozen", True, raising=False)
    old_path = os.environ['PATH']
    reload(gridsync)
    delta = ''
    for _, s in enumerate(difflib.ndiff(old_path, os.environ['PATH'])):
        if s[0] == '+':
            delta += s[-1]
    assert delta == os.pathsep + os.path.join(os.path.dirname(sys.executable),
                                              'Tahoe-LAFS')


def test_frozen_del_reactor(monkeypatch):
    monkeypatch.setattr("sys.frozen", True, raising=False)
    sys.modules['twisted.internet.reactor'] = 'test'
    reload(gridsync)
    assert 'twisted.internet.reactor' not in sys.modules


def test_frozen_del_reactor_pass_without_twisted(monkeypatch):
    monkeypatch.setattr("sys.frozen", True, raising=False)
    reload(gridsync)
    assert 'twisted.internet.reactor' not in sys.modules


def test_config_dir_win32(monkeypatch):
    monkeypatch.setattr("sys.platform", "win32")
    monkeypatch.setenv('APPDATA', 'C:\\Users\\test\\AppData\\Roaming')
    reload(gridsync)
    assert gridsync.config_dir == os.path.join(
        os.getenv('APPDATA'), gridsync.APP_NAME)


def test_config_dir_darwin(monkeypatch):
    monkeypatch.setattr("sys.platform", "darwin")
    reload(gridsync)
    assert gridsync.config_dir == os.path.join(
        os.path.expanduser('~'), 'Library', 'Application Support',
        gridsync.APP_NAME)


def test_config_dir_other(monkeypatch):
    monkeypatch.setattr("sys.platform", "linux")
    reload(gridsync)
    assert gridsync.config_dir == os.path.join(
        os.path.expanduser('~'), '.config', gridsync.APP_NAME.lower())


def test_config_dir_xdg_config_home(monkeypatch):
    monkeypatch.setattr("sys.platform", "linux")
    monkeypatch.setenv('XDG_CONFIG_HOME', '/test')
    reload(gridsync)
    assert gridsync.config_dir == os.path.join(
        '/test', gridsync.APP_NAME.lower())


def test_resource():
    assert gridsync.resource('test') == os.path.join(
        gridsync.pkgdir, 'resources', 'test')
