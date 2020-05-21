from flask_migrate import Migrate, MigrateCommand, Manager

from app import create_app, db

app = create_app('dev')

manage = Manager(app=app)
Migrate(app, db)
manage.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manage.run()
