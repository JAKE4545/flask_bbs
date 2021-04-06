from flask import session
from flask import g
from .views import cms
from .models import CMSUser
import config

@cms.before_request
def before_request():
    if config.CMS_USER_ID in session:
        id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.filter_by(id=id).first()
        if user:
            g.cms_user = user