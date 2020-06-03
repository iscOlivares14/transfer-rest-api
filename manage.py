#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server

from app import create_app, db
from app.models import (
    User,
    Account
)

env = os.environ["KAKA_ENV"]
app = create_app(env)
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("runserver", Server(port=5000))


@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Account=Account
    )


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def seed():
    db.session.commit()

@manager.command
def urlmap():
    """Print url map."""
    print(app.url_map)

# manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

app.port = 5000
app.host = "0.0.0.0"
app.debug = True

if __name__ == "__main__":
    def my_handler(type, value, tb):
        app.logger.error("Uncaught exception: {0}".format(str(value)))


    # Install exception handler
    sys.excepthook = my_handler
    manager.run()
