# forkRepository
A web service to fork it's own Github repo to a user's account

# Deployment
To fork this repository to your Github account, go to https://fork-repo-app.herokuapp.com/

# To run locally
- Prerequisites
    - Python 3 must be installed on your local workstation
    - Flask
- Set up the following environment variables. For example, on mac terminal execute the following
    - export CONFIGURATION_SETUP="config.DevConfig"
    - export github_dev_app_client_id={Your Github App Client ID}
    - export dev_redirect_uri_on_authorization='http://127.0.0.1:9001/forkRepo'
    - export dev_redirect_state={any random string}
    - export dev_redirect_uri_for_access_token='http://127.0.0.1:9001/accessToken'
    - export github_dev_fork_repo_app_uri='https://github.com/apps/fork-repo-github-app'
    - export dev_authorization_uri='http://127.0.0.1:9001/authorize'
- Run the following repository's root directory level
  - source venv/bin/activate
  - flask --app app run --port=9001
  - On a browser, open http://127.0.0.1:9001

# Things to be aware of
- User authentication & authorization are done by a Github App 
- When prompted a Github User (you) must install the proposed Github App 
- Github App authentication & authorization workflow should be self-explanatory but occasionally may trip up on some workflows 

# Known Limitation
- No tests at this time 
- fork name is static 
- May not work as intended up on token expiration as refresh token is not taken into account within the implementation
- "Unhappy" paths are not vetted

# Resources
- https://devcenter.heroku.com/articles/config-vars
- https://medium.com/thedevproject/how-and-why-have-a-properly-configuration-handling-file-using-flask-1fd925c88f4c
- https://realpython.com/flask-by-example-part-1-project-setup/
- https://docs.github.com/en/apps/creating-github-apps/creating-github-apps/about-apps
