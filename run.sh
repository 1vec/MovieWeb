#!/bin/sh
cd `dirname $0`
echo "Enter dir $(pwd)"
export FLASK_APP=flaskr
export FLASK_ENV=development
flask init-db
flask run

