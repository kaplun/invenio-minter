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

"""Click command-line interface for PIDStore management."""

from __future__ import absolute_import, print_function

import click
from flask_cli import with_appcontext
from invenio_db import db

from . import get_last_sequence, get_next_sequence, reset_sequence


#
# Minter management commands
#

@click.group()
def minter():
    """Minter management commands."""


@minter.command()
@click.argument('sequence')
@with_appcontext
def next(sequence):
    """Return the next element for the given sequence."""
    next_sequence = get_next_sequence(sequence)
    db.session.commit()
    click.echo(next_sequence)


@minter.command()
@click.argument('sequence')
@with_appcontext
def next(sequence):
    """Return the last element already returned for the given sequence."""
    last_sequence = get_last_sequence(sequence)
    db.session.commit()
    click.echo(last_sequence)


@minter.command()
@click.argument('sequence')
@click.option('-i', '--id', 'id', required=False, default=0)
@with_appcontext
def next(sequence, id=0):
    """Reset the ID for the given sequence."""
    reset_sequence(sequence, id=id)
    db.session.commit()
