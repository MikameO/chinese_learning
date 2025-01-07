import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from flask import Flask, render_template, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from config import config
import random

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)

    # Configure logging
    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/chinese_learning.log',
                                             maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Chinese Learning Platform startup')

    from models import Character, UserCharacterProgress, CharacterComponent, RelationType
    from datetime import datetime

    # Register routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/study')
    def study():
        limit = request.args.get('limit', 15, type=int)
        all_chars = Character.query.all()
        chosen_chars = random.sample(all_chars, k=min(limit, len(all_chars)))
        return render_template('study.html', characters=[char.to_dict() for char in chosen_chars])

    @app.route('/characters')
    def characters():
        chars = Character.query.all()
        return render_template('characters.html', characters=chars)

    @app.route('/api/characters')
    def get_characters():
        chars = Character.query.all()
        return jsonify([char.to_dict() for char in chars])

    @app.route('/api/characters/<int:char_id>/related')
    def get_related_characters(char_id):
        char = Character.query.get_or_404(char_id)
        return jsonify({
            'components': [c.to_dict() for c in char.components],
            'similar': [c.to_dict() for c in char.similar_to]
        })

    @app.route('/character/<int:char_id>')
    def character_detail(char_id):
        character = Character.query.get_or_404(char_id)
        return render_template('character_detail.html', character=character)

    @app.route('/api/review', methods=['POST'])
    def review_character():
        data = request.json
        char_id = data.get('char_id')
        user_id = data.get('user_id')  # or from session/current_user
        
        progress = UserCharacterProgress.query.filter_by(
            user_id=user_id, character_id=char_id
        ).first()

        if not progress:
            # Create new progress record if it doesn’t exist
            progress = UserCharacterProgress(
                user_id=user_id,
                character_id=char_id
            )
            db.session.add(progress)

        # Update fields
        progress.learned = True
        progress.last_reviewed_at = datetime.now()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Character reviewed!'})

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables created successfully")
        except Exception as e:
            app.logger.error(f"Error creating database tables: {e}")
            raise

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)