from src.models import app, db, User, bcrypt

def create_app(): 

    app.app_context().push()
    db.drop_all()
    db.create_all()
    # hashed_password = bcrypt.generate_password_hash("qa74ze7r").decode("utf-8")
    user = User(username = "Admin", email = "info@hkmakeupshop.com", phone = "60482103", password = "$2b$12$CdP7uMlCdKcmEx03r.yrXuzlydc0zH5PfWEcTbN7rgcTm9R8UHru6")
    db.session.add(user)
    db.session.commit()

    return app