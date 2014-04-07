import sys, os

# Use the virtualenv, not the system python
activate_this = '/opt/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# Insert our app directory to $PYTHONPATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Read the SetEnv variables defined in the apache config 
def application(req_environ, start_response):
    _env = {k.replace('FF_',''): v for k,v in req_environ.items() if k.startswith('FF')}
    os.environ.update(_env)
    from runserver import app as _application
    return _application(req_environ, start_response)
