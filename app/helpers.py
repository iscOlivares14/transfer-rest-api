#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.sql import func

from . import db


class CoreMixin(object):
    # this mixin automatically adds these fields for all models that inherit it
    last_modified = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    created = db.Column(db.DateTime, server_default=func.now(), nullable=False)

