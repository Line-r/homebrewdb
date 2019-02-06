import os
import sys
import transaction
import json

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from .models import (
    DBSession,
    Category,
    Status,
    CIA,
    TDSX,
    Entry,
    User,
    Group,
    Base,
    )

from .security import hash_password

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    with transaction.manager:
        userpass = json.load(open("private/userpass.json"))
        for username in userpass:
            usermodel = User(name=username, password=userpass[username], active=True)
            DBSession.add(usermodel)

            user = DBSession.query(User).filter_by(name=username).one()
            groupmodel = Group(id=user.id, name='super', active=True)
            DBSession.add(groupmodel)

    with transaction.manager:
        categories = json.load(open("categories.json"))
        for category in categories:
            categorymodel = Category(active=True,name=category)
            DBSession.add(categorymodel)

    with transaction.manager:
        statuses = json.load(open("statuses.json"))
        for status in statuses:
            statusmodel = Status(active=True,name=status)
            DBSession.add(statusmodel)

