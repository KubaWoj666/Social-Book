from django import template
# from models import Comment

register = template.Library()

def get_comments(post_comments, post_id):
    return post_comments.get(post_id)
register.filter("get_comments", get_comments)