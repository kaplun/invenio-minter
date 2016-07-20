# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Module tests."""

from __future__ import absolute_import, print_function

from flask import Flask

from invenio_minter import get_last_sequence, get_next_sequence, \
    record_sequence, reset_sequence


def test_version():
    """Test version import."""
    from invenio_minter import __version__
    assert __version__


def test_get_next_sequence(app):
    """Test get_next_sequence function"""
    with app.app_context():
        assert get_next_sequence("test-{id}") == "test-1"
        assert get_next_sequence("test-{id}") == "test-2"
        assert get_next_sequence("test2-{id}") == "test2-1"
        assert get_next_sequence("test-{id}") == "test-3"


def test_get_next_sequence(app):
    """Test get_last_sequence function"""
    with app.app_context():
        assert get_next_sequence("test-last-{id}") == "test-last-1"
        assert get_last_sequence("test-last-{id}") == "test-last-1"
        assert get_next_sequence("test-last-{id}") == "test-last-2"
        assert get_last_sequence("test-last2-{id}") == "test-last2-0"
        assert get_last_sequence("test-last-{id}") == "test-last-2"


def test_get_reset_sequence(app):
    """Test reset_sequence function"""
    with app.app_context():
        assert get_next_sequence("test-reset-{id}") == "test-reset-1"
        assert get_next_sequence("test-reset-{id}") == "test-reset-2"
        reset_sequence("test-reset-{id}", 10)
        assert get_next_sequence("test-reset-{id}") == "test-reset-11"
        reset_sequence("test-reset-{id}", 5)
        assert get_next_sequence("test-reset-{id}") == "test-reset-6"
        reset_sequence("test-reset2-{id}", 5)
        assert get_next_sequence("test-reset2-{id}") == "test-reset2-6"


def test_get_record_sequence(app):
    """Test record_sequence function"""
    with app.app_context():
        assert get_next_sequence("test-record-{id}") == "test-record-1"
        assert get_next_sequence("test-record-{id}") == "test-record-2"
        record_sequence("test-record-{id}", 10)
        assert get_next_sequence("test-record-{id}") == "test-record-11"
        record_sequence("test-record-{id}", 5)
        assert get_next_sequence("test-record-{id}") == "test-record-12"
        record_sequence("test-record2-{id}", 5)
        assert get_next_sequence("test-record2-{id}") == "test-record2-6"
