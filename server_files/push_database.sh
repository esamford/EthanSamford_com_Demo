github_account=esamford
database_repo=ethansamford_com_database_backup
project_repo=portfolio
host_name=django_db_backup

# Copy the database.
cd
sudo rm "$database_repo/db.sqlite3"
sudo cp "$project_repo/db.sqlite3" "$database_repo/db.sqlite3"

# Push changes.
cd
cd "$database_repo/"
git add --all
git commit -m "Automated ethansamford.com database backup."
git push git@$host_name:$github_account/$database_repo.git

cd
