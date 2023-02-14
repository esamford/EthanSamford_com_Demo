#
# Before you run this script, you should create a deploy key and link it to
# the GitHub repository.
#
#   1. Use these commands to generate the keys. Press Enter to skip password prompts:
#         cd
#         ssh-keygen -t ed25519 -f ".ssh/project" -C "[YOUR_GITHUB_EMAIL]"
#         ssh-keygen -t ed25519 -f ".ssh/django_db_backup" -C "[YOUR_GITHUB_EMAIL]"
#
#   2. Two keys were generated. One is for cloning/pulling the Django project and
#      the other for cloning/pulling/pushing Django's SQLite database file.
#      Create the ".ssh/config" file using the first set of commands, then write
#      the following:
#         cd
#         touch ".ssh/config"
#         nano ".ssh/config"
#
#           Host project github.com
#           Hostname github.com
#           IdentityFile ~/.ssh/project
#
#           Host django_db_backup github.com
#           Hostname github.com
#           IdentityFile ~/.ssh/django_db_backup
#
#      WARNING: If you look in the /home/[user]/.ssh/ folder, you'll see a file called
#      "authorized_keys." NEVER DELETE OR MOVE THIS FILE. It's what recognizes your ssh
#      key, and without it you will no longer be able to log into the server. If you want
#      to allow access to the server from somewhere else, you may generate a new key and
#      paste its contents into this file on a new line to add it to the whitelist.
#
#   4. Use a web browser to navigate to the Django's repository > Settings > Deploy
#      Keys page. Click "Add Deploy Key" and submit the text printed from the
#      ".ssh/project.pub" file. Write access is not necessary.
#
#   5. Use a web browser to navigate to the database backup repository > Settings >
#      Deploy Keys page. Click "Add Deploy Key" and submit the text printed from the
#      ".ssh/django_db_backup.pub" file. Write access is required for "git push"
#      commands used to back up the database to GitHub.
#
# Once the keys have been generated and shared with GitHub, you may clone each
# repository without making them public. Use the following commands to do so:
#   sudo apt-get install git -y
#   cd
#   git clone git@[SSH_KEY_FILE_NAME_WITHOUT_PUB_EXTENSION]:[GITHUB_ACCOUNT_NAME]/[REPOSITORY_NAME].git
# When prompted to clone, type "yes".
#
# This script should be saved in your "[PROJECT_ROOT]/server_files" directory.
# Create a new script in your home directory (the parent of your cloned project)
# and write the following commands:
#   clear
#   cd
#   rm "update_project.sh"
#   cp "[PROJECT_ROOT]/server_files/update_project.sh" "update_project.sh"
#   source "update_project.sh"
#   cd
# If this "update_project.sh" file has been changed, run the script twice to
# get and run the most-recent version. If you cannot run this script with crontab,
# try using "sudo chmod ___ _______" on it.
#
# === === === AFTER SERVER SETUP === === ===
#
# Set up cron jobs for automatic updates.
#
#   1. Open the crontab with this command, and choose "nano" as the editor:
#       crontab -e
#
#   2. Write the following lines at the bottom of the file:
#       SHELL=/bin/sh
#       PATH=/bin:/sbin:/usr/bin:/usr/sbin
#       [DESIRED_TASK_EXECUTION_TIME] [PATH_TO_DATABASE_PUSH_SCRIPT]
#       [DESIRED_TASK_EXECUTION_TIME] [PATH_TO_PROJECT_PULL_SCRIPT]
#       .
#      NOTE: You can use "~/" at the start of the path to specify your home
#      directory.
#
# If you have not done so, don't forget to create the initial Django superuser
# so you can access the Django admin console. Activate your project's virtual
# environment and type the following command to start:
#	  python manage.py createsuperuser
#

# Enter project variable settings here:

github_account=esamford
project_repo_name=portfolio
website_url=www.ethansamford.com

# ====================================

clear

# Initial server setup.
sudo apt-get update
# -> Server packages:
sudo apt-get install cron
sudo apt-get install python3-pip nginx gunicorn git -y
sudo apt-get install gcc libpq-dev -y
sudo apt-get install python-dev  python-pip -y
sudo apt-get install python3-dev python3-pip python3-venv python3-wheel -y
# -> Update packages after downloading.
sudo apt-get update
sudo apt update && sudo apt upgrade -y

# Update the repository.
cd
cd "$project_repo_name/"
git pull git@project:$github_account/$project_repo_name.git

# Set ownership settings on the repository.
cd
sudo chown -R ubuntu $project_repo_name
sudo chmod 777 $project_repo_name

# Set up the virtual environment and install required libraries.
cd "$project_repo_name/"
python3 -m venv venv
source venv/bin/activate
pip3 install wheel
pip3 install -r requirements.txt
pip3 install gunicorn==20.0.2
deactivate

# Make migrations to the Django database.
cd
cd "$project_repo_name/"
source venv/bin/activate
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput
deactivate

# Configure and run Gunicorn from the project's provided "gunicorn.service" file.
cd
sudo rm /etc/systemd/system/gunicorn.service
sudo cp -fr "$project_repo_name/server_files/gunicorn.service" "/etc/systemd/system/gunicorn.service"

# Configure and run Nginx from the project's provided "django_app" file.
cd
sudo rm "/etc/nginx/sites-enabled/django_app"
sudo rm "/etc/nginx/sites-available/django_app"
sudo cp -fr "$project_repo_name/server_files/django_app" "/etc/nginx/sites-available/django_app"
sudo ln -s "/etc/nginx/sites-available/django_app" "/etc/nginx/sites-enabled"
sudo rm "/etc/nginx/sites-enabled/default"
sudo rm "/etc/nginx/sites-available/default"
sudo systemctl daemon-reload

# Install/update the server's SSL certificate for HTTPS traffic.
cd
sudo snap install core; sudo snap refresh core
sudo apt-get remove certbot
sudo snap install --classic certbot
sudo snap refresh certbot
sudo rm /usr/bin/certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

# Update the "/etc/nginx/sites-enabled/django_app" config file for Nginx.
# NOTES:
#   1. It is necessary that the server is allowed to receive HTTPS requests from anywhere after certification.
#      If you can't connect, check the server's network security group to see if it allows HTTPS from anywhere.
#   2. The certification script requires HTTP access to check for a file on the server. If HTTP is blocked,
#      the certification will fail and HTTPS will not be enabled.
sudo certbot --nginx -n -d $website_url --redirect --agree-tos

sudo ufw allow https
sudo ufw allow 'Nginx Full'
sudo systemctl restart nginx

# Display service status for debugging (if needed).
#   Shut down existing Gunicorn versions and restart it.
#   Doing this also re-creates the .sock file in the repository folder.
#   If the .sock file doesn't exist, something may be wrong with the "gunicorn.server" file.
#   If, Nginx is showing a 502 (bad gateway) error on the web, check that Gunicorn is running properly.
#   These used to be just "gunicorn" instead of "gunicorn.service."
cd
sudo systemctl stop gunicorn.service
sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.service
sudo systemctl status gunicorn.service

# Restart Nginx so that the web page is accessible.
sudo service nginx restart
sudo nginx -t
