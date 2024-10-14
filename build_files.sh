echo "BUILD START"

# Install the required packages from requirements.txt
python3.9 -m pip install -r requirements.txt

# Collect static files without input and clear the existing ones
python3.9 manage.py collectstatic --noinput --clear

echo "BUILD END"
