#!/bin/sh
cd `dirname $0`
echo "Enter dir $(pwd)"
export FLASK_APP=movienest
export FLASK_ENV=development
flask run
