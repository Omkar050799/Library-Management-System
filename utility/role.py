from django.conf import settings

""" check superadmin role """
def user_role_super_admin(user):
    return user.group.id == settings.GRP_SUPER_ADMIN
