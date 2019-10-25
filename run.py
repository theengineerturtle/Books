from app import create_app, db
from app.models import User, Book

if __name__ == '__main__':
    app = create_app('production')
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0')
    
