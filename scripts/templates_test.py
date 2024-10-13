# 1. Verify directory structure
echo "Checking WebProject structure:"
tree WebProject

echo "Checking DataScienceProject structure:"
tree DataScienceProject

echo "Checking CLIProject structure:"
tree CLIProject

# 2. Check file contents
echo "Checking WebProject files:"
cat WebProject/src/app.py
cat WebProject/requirements.txt

echo "Checking DataScienceProject files:"
cat DataScienceProject/requirements.txt
cat DataScienceProject/notebooks/example.ipynb

echo "Checking CLIProject files:"
cat CLIProject/src/cli.py
cat CLIProject/requirements.txt

# 3. Test functionality
echo "Testing WebProject:"
cd WebProject
pip install -r requirements.txt
python src/app.py &
curl http://localhost:5000
kill %1
cd ..

echo "Testing DataScienceProject:"
cd DataScienceProject
pip install -r requirements.txt
python -c "import numpy; import pandas; import matplotlib; import sklearn; print('All libraries imported successfully')"
cd ..

echo "Testing CLIProject:"
cd CLIProject
pip install -r requirements.txt
python src/cli.py
cd ..