"""
Copyright 2008-2015 Free Software Foundation, Inc.
This file is part of GNU Radio

GNU Radio Companion is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

GNU Radio Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
"""

import uuid

def valid_uuid_or_none(existing_uuid):
    # Is it already a UUID object?
    if type(existing_uuid) is uuid.UUID:
        return str(existing_uuid)
        
    # Is it a string (or string-compatible) that can be converted to a UUID?
    try:
        converted_uuid = uuid.UUID(existing_uuid)
        return str(converted_uuid)
    except (AttributeError, TypeError, ValueError):
        # Not valid!
        # AttributeError happens if input is not string-like
        # TypeError happens if the input is None
        # ValueError happens if the string is not a valid UUID
        return None

def valid_uuid_or_new(existing_uuid):
    this_uuid = valid_uuid_or_none(existing_uuid)
        
    if this_uuid is None:
        # Create a new UUID from scratch, totally randomly
        return new_uuid()
    else:
        # Return the existing UUID
        return this_uuid

def new_uuid():
    return str(uuid.uuid4())
