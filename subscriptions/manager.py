from flask.ext.script import Manager

from api import app
from app.models import init

manager = Manager(app)


@manager.command
def initializedb():
    init()


@manager.command
def runserver():
    app.run(debug=True)

if __name__ == "__main__":
    manager.run()
