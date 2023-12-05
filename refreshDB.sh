# Bash script useful to update database tables when you modify their structure

fileName="zestviewdata.db"

if [ -e "instance/$fileName" ]; then
  echo "Removing existing database file..."
  rm instance/$fileName
  echo "Database file $fileName removed successfully."
fi

echo "Creating a new database file..."
python3 << EOF
from app import app, db
app.app_context().push()
db.create_all()
EOF

if [ -e "instance/$fileName" ]; then
  echo "Database file $fileName created successfully."
else
  echo "Failed to create database file $fileName."
fi
