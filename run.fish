#!/usr/local/bin/fish
if ls | grep venv
    source venv/bin/activate.fish
end
if mysql -u root -e "exit"
    echo "Database is working"
else
    mysql.server start
end
python3 run.py
 