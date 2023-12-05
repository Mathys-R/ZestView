# Bash script useful to update database tables when you modify their structure

#Define the name of your Database file
dbName="zestviewdata.db"

#Removing Database if it already exists
if [ -e "instance/$dbName" ]; then
  echo "Removing existing database file..."
  rm instance/$dbName
  echo "Database file $dbName removed successfully."
fi

#Generate the new Database according to your flask app
echo "Creating a new database file..."
python3 << EOF
from app import app, db
app.app_context().push()
db.create_all()
EOF

#Check if the Database has been created or something wrent wrong
if [ -e "instance/$dbName" ]; then
  echo "Database file $dbName created successfully."
else
  echo "Failed to create database file $dbName."
fi
