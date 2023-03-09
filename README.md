# forkRepository
A web service to fork it's own Github repo to a user's account

# Deployment
To fork this repository to your Github account, go to https://fork-repo-app.herokuapp.com/

# To run locally
- Prerequisites
    - Python 3 must be installed on your local workstation
- Set up the following environment variables. For example, on mac terminal execute the following
    - export CONFIGURATION_SETUP="config.DevConfig"
    - export github_dev_app_client_id={Your Github App Client ID}
    - export dev_redirect_uri_on_authorization='http://127.0.0.1:9001/forkRepo'
    - export dev_redirect_state={any random string}
    - export dev_redirect_uri_for_access_token='http://127.0.0.1:9001/accessToken'
    - export github_dev_fork_repo_app_uri='https://github.com/apps/fork-repo-github-app'
    - export dev_authorization_uri='http://127.0.0.1:9001/authorize'
- Run the following at the project's root level
  - source venv/bin/activate
  - flask --app app run --port=9001
  - On a browser, go to http://127.0.0.1:9001

# Things to be aware of
1. User authentication & authorization are done by a Github App
2. When prompted a Github User (you) must install the proposed Github App 
3. Github App authentication & authorization workflow should be self-explanatory but occasionally may trip up on some workflows 

# Known Limitation
1. No tests at this time
2. fork name is static
2. May not work as intended up on token expiration as refresh token is not taken into account within the implementation
3. "Unhappy" paths are not vetted