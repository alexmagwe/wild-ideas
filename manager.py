from flask_script import Manager
from flask_migrate import MigrateCommand
from config import configs
from main import app, db
app.config.from_object(configs['production'])
manager = Manager(app)
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
