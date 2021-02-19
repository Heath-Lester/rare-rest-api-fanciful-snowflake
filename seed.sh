#!/bin/bash

rm -rf rareapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations rareapi
python manage.py migrate rareapi
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata tags
python manage.py loaddata categories
python manage.py loaddata comments
python manage.py loaddata posts
python manage.py loaddata postTags

# Create a seed.sh file in your project directory
# Place the code below in the file.
# Run chmod +x seed.sh in the terminal.
# Then run ./seed.sh in the terminal to run the commands.