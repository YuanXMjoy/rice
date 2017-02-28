#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from rice import create_app, db
from rice.models import Rice, Order, User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Rice=Rice, Order=Order, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def create_admin(username, password, phone_number):
    u = User(username=username, password=password, phone_number=phone_number)
    db.session.add(u)
    db.session.commit()

if __name__ == "__main__":
    manager.run()
