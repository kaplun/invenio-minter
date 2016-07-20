# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2016 CERN.
#
# INSPIRE is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""INSPIRE sequence ID generator."""

from invenio_db import db


class SequenceIdentifier(db.Model):
    """Generic sequence generator."""

    __tablename__ = 'minter_sequence'

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"))
    sequence = db.Column(db.String(255), nullable=False, primary_key=True)

    @classmethod
    def next(cls, sequence):
        """Return next element in the sequence."""
        with db.session.begin_nested() as session:
            obj = db.session.query(cls).filter_by(sequence=sequence).first()
            if obj is None:
                obj = cls(id=0, sequence=sequence)
                db.session.add(obj)
            obj.id += 1
            return sequence.format(id=obj.id)

    @classmethod
    def last(cls, sequence):
        """Return last element in the sequence."""
        with db.session.begin_nested() as session:
            obj = db.session.query(cls).filter_by(sequence=sequence).first()
            if obj is None:
                return sequence.format(id=0)
            return sequence.format(id=obj.id)

    @classmethod
    def reset(cls, sequence, id=0):
        """Reset the sequence."""
        with db.session.begin_nested() as session:
            obj = db.session.query(cls).filter_by(sequence=sequence).first()
            if obj is None:
                obj = cls(id=id, sequence=sequence)
                db.session.add(obj)
            else:
                obj.id = id

    @classmethod
    def record(cls, sequence, id=0):
        """Reset the sequence."""
        with db.session.begin_nested() as session:
            obj = db.session.query(cls).filter_by(sequence=sequence).first()
            if obj is None:
                obj = cls(id=id, sequence=sequence)
                db.session.add(obj)
            elif id > obj.id:
                obj.id = id


def get_next_sequence(sequence):
    """Return the next element for the given sequence."""
    return SequenceIdentifier.next(sequence)


def get_last_sequence(sequence):
    """Return the last element already returned for the given sequence."""
    return SequenceIdentifier.last(sequence)


def reset_sequence(sequence, id=0):
    """Reset the ID for the given sequence."""
    SequenceIdentifier.reset(sequence, id)


def record_sequence(sequence, id=0):
    """Record the ID for the current sequence.

    Note: this implies that if the provided id is smaller than the last used
    one, nothing changes. If id is bigger that the last one, then this is
    equivalent to calling reset_sequence().
    """
    SequenceIdentifier.record(sequence, id)
