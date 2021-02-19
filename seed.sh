#!/bin/bash

python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata tags
python3 manage.py loaddata categories
python3 manage.py loaddata comments
python3 manage.py loaddata posts
python3 manage.py loaddata postTags


# Create a seed.sh file in your project directory
# Place the code below in the file.
# Run chmod +x seed.sh in the terminal.
# Then run ./seed.sh in the terminal to run the commands.