"""
Vercel serverless entrypoint for The Decision Completeness Engine.
"""

from app import app

# Vercel looks for 'app' or handler
handler = app
