from app import db
from datetime import datetime
from enum import Enum

class RelationType(Enum):
    PHONETIC = 'phonetic'
    VISUAL = 'visual'
    SEMANTIC = 'semantic'

class CharacterComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    component = db.Column(db.String(8), nullable=False)
    meaning = db.Column(db.String(100))
    stroke_count = db.Column(db.Integer)
    usage_notes = db.Column(db.Text)

# Association table for character components with additional metadata
character_components = db.Table('character_components',
    db.Column('character_id', db.Integer, db.ForeignKey('character.id')),
    db.Column('component_id', db.Integer, db.ForeignKey('character_component.id')),
    db.Column('position', db.String(20)),  # top, bottom, left, right, etc.
    db.Column('notes', db.Text)
)

# Enhanced association table for similar characters with relationship type
similar_characters = db.Table('similar_characters',
    db.Column('character_id', db.Integer, db.ForeignKey('character.id')),
    db.Column('similar_id', db.Integer, db.ForeignKey('character.id')),
    db.Column('relationship_type', db.Enum(RelationType)),
    db.Column('similarity_score', db.Float),  # 0.0 to 1.0
    db.Column('notes', db.Text)
)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hanzi = db.Column(db.String(7), nullable=False)
    pinyin = db.Column(db.String(50), nullable=False)
    meaning = db.Column(db.String(100), nullable=False)
    stroke_count = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    radical = db.Column(db.String(1))  # Main radical of the character
    etymology = db.Column(db.Text)     # Brief explanation of character origin
    mnemonic = db.Column(db.Text)      # Memory aid for learning
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Enhanced relationships
    components = db.relationship('CharacterComponent', 
                              secondary=character_components,
                              backref=db.backref('characters', lazy='dynamic'))

    similar_to = db.relationship('Character',
                              secondary=similar_characters,
                              primaryjoin=(similar_characters.c.character_id == id),
                              secondaryjoin=(similar_characters.c.similar_id == id),
                              backref=db.backref('similar_from', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'hanzi': self.hanzi,
            'pinyin': self.pinyin,
            'meaning': self.meaning,
            'stroke_count': self.stroke_count,
            'difficulty': self.difficulty,
            'radical': self.radical,
            'etymology': self.etymology,
            'mnemonic': self.mnemonic,
            'components': [{
                'component': c.component,
                'meaning': c.meaning,
                'position': self.get_component_position(c),
                'usage_notes': c.usage_notes
            } for c in self.components],
            'similar_characters': [{
                'hanzi': c.hanzi,
                'pinyin': c.pinyin,
                'relationship_type': self.get_relationship_type(c),
                'similarity_score': self.get_similarity_score(c)
            } for c in self.similar_to]
        }

    def get_component_position(self, component):
        """Get the position of a component within this character"""
        result = db.session.query(character_components.c.position)\
            .filter(character_components.c.character_id == self.id)\
            .filter(character_components.c.component_id == component.id)\
            .first()
        return result[0] if result else None

    def get_relationship_type(self, similar_char):
        """Get the type of relationship with another character"""
        result = db.session.query(similar_characters.c.relationship_type)\
            .filter(similar_characters.c.character_id == self.id)\
            .filter(similar_characters.c.similar_id == similar_char.id)\
            .first()
        return result[0].value if result else None

    def get_similarity_score(self, similar_char):
        """Get the similarity score with another character"""
        result = db.session.query(similar_characters.c.similarity_score)\
            .filter(similar_characters.c.character_id == self.id)\
            .filter(similar_characters.c.similar_id == similar_char.id)\
            .first()
        return result[0] if result else None
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    # add other fields like email, password, etc.

class UserCharacterProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    learned = db.Column(db.Boolean, default=False)
    last_reviewed_at = db.Column(db.DateTime)
    # ... any other fields that make sense for progress tracking (e.g., review_score)
