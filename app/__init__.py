from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev_cinemax_pro_super_secret'
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import movies
    app.register_blueprint(movies.bp)
    
    from . import shows
    app.register_blueprint(shows.bp)
    
    from . import seats
    app.register_blueprint(seats.bp)
    
    from . import bookings
    app.register_blueprint(bookings.bp)
    
    return app
