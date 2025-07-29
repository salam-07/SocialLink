"""
Routes package - Import all route modules
"""
from . import main_routes
from . import post_routes
from . import auth_routes

__all__ = ['main_routes', 'post_routes', 'auth_routes']
