github_account=esamford
database_repo=ethansamford_com_database_backup
project_repo=portfolio
host_name=django_db_backup

# Pull changes.
cd
cd "$database_repo/"
git pull git@$host_name:$github_account/$database_repo.git

# Stop the website.
sudo systemctl stop gunicorn.service

# Copy the database.
cd
sudo rm "$project_repo/db.sqlite3"
sudo cp "$database_repo/db.sqlite3" "$project_repo/db.sqlite3"

# Restart the website.
sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.service
sudo systemctl status gunicorn.service
sudo service nginx restart
sudo nginx -t

cd
