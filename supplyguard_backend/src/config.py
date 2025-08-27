"""
Configuration management for SupplyGuard backend
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database Configuration
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_PATH = os.path.join(BASE_DIR, 'src', 'database', 'app.db')
    DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DATABASE_PATH}')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenRouter API Configuration
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', 'sk-or-v1-demo-key-placeholder')
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    
    # AI Service Configuration
    AI_MODEL = os.getenv('AI_MODEL', 'openai/gpt-3.5-turbo')
    AI_TEMPERATURE = float(os.getenv('AI_TEMPERATURE', '0.7'))
    AI_MAX_TOKENS = int(os.getenv('AI_MAX_TOKENS', '1000'))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate_config(cls):
        """Validate configuration and warn about missing values"""
        warnings = []
        
        if cls.OPENROUTER_API_KEY == 'sk-or-v1-demo-key-placeholder':
            warnings.append("OPENROUTER_API_KEY is using placeholder value. Set your actual API key in .env file.")
        
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            warnings.append("SECRET_KEY is using default value. Change it for production.")
        
        return warnings
    
    @classmethod
    def is_development(cls):
        """Check if running in development mode"""
        return cls.FLASK_ENV == 'development'
    
    @classmethod
    def is_production(cls):
        """Check if running in production mode"""
        return cls.FLASK_ENV == 'production'
