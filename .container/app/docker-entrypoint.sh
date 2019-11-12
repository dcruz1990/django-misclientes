#!/usr/bin/env bash
set -e
shopt -s extglob globstar

# Activate venv
source $VENV_HOME/bin/activate
cd $SRC_HOME
echo "Execute migrations"
python manage.py migrate
echo "Compile .po to .mo"
python manage.py compilemessages
echo "Update assets: All modules to static dir"
python manage.py collectstatic --noinput
# Real entrypoint
uwsgi --emperor $SRC_HOME/uwsgi --master --enable-threads
