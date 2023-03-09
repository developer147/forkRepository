import os

class Config(object):
    DEBUG = False
    TESTING = False

class ProdConfig(Config):
    #GITHUB_APP_ID = os.environ.get('github_prod_app_id')
    GITHUB_APP_CLIENT_ID = os.environ.get('github_prod_app_client_id')
    GITHUB_APP_CLIENT_SECRET = os.environ.get('github_prod_app_client_secret')
    REDIRECT_URI_ON_AUTHORIZATION = os.environ.get('prod_redirect_uri_on_authorization')
    REDIRECT_STATE = os.environ.get('prod_redirect_state')
    REDIRECT_URI_FOR_ACCESS_TOKEN = os.environ.get('prod_redirect_uri_for_access_token')
    GITHUB_FORK_REPO_APP_URI = os.environ.get('github_prod_fork_repo_app_uri')
    AUTHORIZATION_URI = os.environ.get('prod_authorization_uri')

class DevConfig(Config):
    ENV = "development"
    #GITHUB_APP_ID = os.environ.get('github_dev_app_id')
    GITHUB_APP_CLIENT_ID = os.environ.get('github_dev_app_client_id')
    GITHUB_APP_CLIENT_SECRET = os.environ.get('github_dev_app_client_secret')
    REDIRECT_URI_ON_AUTHORIZATION = os.environ.get('dev_redirect_uri_on_authorization')
    REDIRECT_STATE = os.environ.get('dev_redirect_state')
    REDIRECT_URI_FOR_ACCESS_TOKEN = os.environ.get('dev_redirect_uri_for_access_token')
    GITHUB_FORK_REPO_APP_URI = os.environ.get('github_dev_fork_repo_app_uri')
    AUTHORIZATION_URI = os.environ.get('dev_authorization_uri')
    DEBUG = True
