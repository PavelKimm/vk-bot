from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Project(db.Model):
    __tablename__ = 'projects'

    project_name = db.Column(db.String(50), primary_key=True)
    url = db.Column(db.String(80))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    project_name = db.Column(db.ForeignKey('projects.project_name'))
    login = db.Column(db.String(50))
    password = db.Column(db.String(50))

    db.UniqueConstraint(user_name, project_name)
    db.UniqueConstraint(login)

    def __init__(self, user_name, project_name, login, password):
        self.user_name = user_name
        self.project_name = project_name
        self.login = login
        self.password = password

    def __repr__(self):
        return f'<id {self.id}>'

    def serialize(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'project_name': self.project_name,
            'login': self.login,
            'password': self.password
        }
