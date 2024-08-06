from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shorts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_id = db.Column(db.String(36), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    actual_content_link = db.Column(db.String(255), default="")
    image = db.Column(db.String(255), default="")
    upvote = db.Column(db.Integer, default=0)
    downvote = db.Column(db.Integer, default=0)

    def as_dict(self):
        return {
            "short_id": self.short_id,
            "category": self.category,
            "title": self.title,
            "author": self.author,
            "publish_date": self.publish_date.isoformat(),
            "content": self.content,
            "actual_content_link": self.actual_content_link,
            "image": self.image,
            "votes": {
                "upvote": self.upvote,
                "downvote": self.downvote
            }
        }

if __name__ == '__main__':
    app.run(port=9000,debug=True)
