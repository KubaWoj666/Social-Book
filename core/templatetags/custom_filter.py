from django import template

register = template.Library()

def get_comments(comments, post_id):
    return comments.get(post_id)
register.filter("get_comments", get_comments)