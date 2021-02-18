#!/bin/bash

rm -rf levelupapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations levelupapi
python manage.py migrate levelupapi
python manage.py loaddata users
python manage.py loaddata tokens

# Create a seed.sh file in your project directory
# Place the code below in the file.
# Run chmod +x seed.sh in the terminal.
# Then run ./seed.sh in the terminal to run the commands.