"""
Main application routes - Dashboard and landing pages
"""
from flask import render_template
from sociallinkapp import app
from sociallinkapp.models import Post
from datetime import datetime, timedelta
from sqlalchemy import func

# route for the landing page
@app.route('/')
@app.route('/landing')
def landing():
    return render_template('landing.html')

# route for dashboard
@app.route('/home')
def home():
    # Get dashboard statistics
    
    # Total posts
    total_posts = Post.query.count()
    
    # Posts this week
    week_ago = datetime.utcnow() - timedelta(days=7)
    posts_this_week = Post.query.filter(Post.date_posted >= week_ago).count()
    
    # Posts by type
    media_posts = Post.query.filter_by(post_type='media').count()
    text_posts = Post.query.filter_by(post_type='text').count()
    
    # Recent posts (last 5)
    recent_posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
    
    # Platform usage statistics
    platform_stats = {}
    all_posts = Post.query.all()
    total_platform_uses = 0
    
    for post in all_posts:
        platforms = post.get_platforms_list()
        for platform in platforms:
            platform_stats[platform] = platform_stats.get(platform, 0) + 1
            total_platform_uses += 1
    
    # Sort platforms by usage
    platform_stats = dict(sorted(platform_stats.items(), key=lambda x: x[1], reverse=True))
    
    dashboard_data = {
        'total_posts': total_posts,
        'posts_this_week': posts_this_week,
        'media_posts': media_posts,
        'text_posts': text_posts,
        'recent_posts': recent_posts,
        'platform_stats': platform_stats,
        'total_platform_uses': total_platform_uses
    }
    
    return render_template('home.html', heading="Dashboard", title="Dashboard", **dashboard_data)

# help page route
@app.route('/help')
def help():
    faq_data = [
        {
            'id': 1,
            'question': 'What is SocialLink?',
            'answer': [
                'SocialLink is a powerful social media management platform that allows you to create, schedule, and manage posts across multiple social media platforms from one centralized dashboard.',
                'With SocialLink, you can streamline your social media workflow, save time, and maintain a consistent online presence across all your social media accounts.'
            ]
        },
        {
            'id': 2,
            'question': 'What is SocialLink?',
            'answer': [
                'SocialLink is a powerful social media management platform that allows you to create, schedule, and manage posts across multiple social media platforms from one centralized dashboard.',
                'With SocialLink, you can streamline your social media workflow, save time, and maintain a consistent online presence across all your social media accounts.'
            ]
        }
    ]
    return render_template('help.html', heading="Help", title="Help", faq_data=faq_data)
