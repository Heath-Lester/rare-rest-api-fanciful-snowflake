# rare-rest-api-fanciful-snowflake
rare-rest-api-fanciful-snowflake created by GitHub

# Rare: The Publishing Platform for the Discerning Writer

## **Description**
Rare is a publishing platform and social application that allows authenticated users to interact in a social forum by creating posts, associated tags and categories to their posts for relevance and filtering, and create comments on each other’s posts in order to interact directly with each other.
 
 
## **Features**
* Users can create Posts to share their thoughts in a public forum.
* Users can create, edit, and delete Tags and Categories to a Post in order to better classify their Posts. Both Tags and Categories can be managed on individual posts or as list views that include the same capabilities.
* Users can create, edit, and delete Comments on their Posts and other user’s Posts in order to take part in a discussion regarding the post.
* Users have the capability to view all of their Posts as a list, or view Posts by all users as a list.
* Admins can approve or delete Author posts before posts are displayed
* Users can search posts by title 
* Users can sort posts by category

## **Setup Server-Side**
 
### Pull down the Server-Side Repo.
 
>Note: This project is meant to run simultaneously with the Client Side Repo found here: https://github.com/nss-day-cohort-44/rare-client-fanciful-snowflake*  
>Depending on which repo you start with, you may already have the following directories set up. 
>This project requires Python
 
### To Begin installing the Server-Side Repo, complete the following steps: 
 
1. Create a directory from which to deploy the application. 	
```mkdir RARE```
 
2.   Enter the following commands: 

```git clone git@github.com:nss-day-cohort-44/rare-rest-api-fanciful-snowflake.git server .```        _note the single dot preceded by a single space_

```pip install django```
or if that doesn't work
```pip3 install django```
 
```pipenv install django autopep8 pylint djangorestframework django-cors-headers pylint-django``` 
 
3. Create a seed.sh file and run it

```
Create a seed.sh file in your project directory
Place the code below in the file.

#!/bin/bash

rm -rf rareapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations rareapi
python3 manage.py migrate rareapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata tags
python3 manage.py loaddata categories
python3 manage.py loaddata posts
python3 manage.py loaddata comments
python3 manage.py loaddata postTags
 
Run chmod +x seed.sh in the terminal.
Then run ./seed.sh in the terminal to run the commands.
```
 
## **Technologies Used**
This application was built using the React JavaScript library. The only package used in the production site outside of those provided by create-react-app was react-router-dom.
The API server is powered by SQLite, python3 and Python.
All styling was accomplished with vanilla CSS3 written by us.

## Planning Links
1. [ERD](https://dbdiagram.io/d/60119b2780d742080a381992)
1. Wireframe: provided by UI/UX https://miro.com/app/board/o9J_kiGCSK4=/

# Authors
[Devin Kent](https://github.com/dalamcd) |
[Mario Campopiano](https://github.com/mcampopiano) |
[Travis Milner](https://github.com/TravisMilner) |
[Patrick Stewart](https://github.com/NotThatPatrickStewart) |
[Ted Marov](https://github.com/tedmarov)

