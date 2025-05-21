# README notes
- **MAKE SURE YOU'RE IN THE CORRECT DIRECTORY**
---

## Requirements 
- Flask
- SQLalchemy
- fullcalendar
- pytest
- SQLite Viewer

## Running application
To run the application
1. `python app.py` to run website, then click the link in terminal 
2. `python manage.py` to drop and create tables

## Installing Flask
1. `pip install Flask`

## Installing SQLalchemy
1. `pip install sqlalchemy`

## Installing Pytest
1. `pip install pytest`
---

# Git Commands
## Switching and Creating Branches
1. Creating a branch `git branch <development>`. (Not needed if you already have another branch)
2. Switching between branches `git checkout <branch name here>`
- to check which branch you are in `git branch`

**If you are switching between branches, make sure you are in the correct branch before pushings changes**
## Pushing Changes to git
1. `git add .` 
2. `git commit -m "message here"`
3. `git push` 

## Fetching Branches
1. `git fetch origin <branch>` downloads up to date data of branch
2. `git pull origin branch` downloads and auto merges 

## Merging Branches
**Used for when you are finished working on the development branch or whatever and it works. Now you want to push that code over to the main branch**
**ONLY MERGE WORKING CODE ONTO MAIN**
**To merge branches, first push changes on the branch you are working on**
- You can also merge on github if this is too confusing lol
1. Switch over to the main branch ` git checkout main`
2. Choose which branch to merge into the main branch ` git merge <development>
3. If you want to delete the branch after merging ` git branch -d <development>
4. You will see a message in the terminal saying to have a comment for reason to merge, to type a message press `i` , after, press `esc` then `:q!` to save
5. you will now need to `git push origin <branch>` on the main branch afterwards so that the merged code gets pushed onto github.

## Cloning the Git repo
1. `git clone <link>`

