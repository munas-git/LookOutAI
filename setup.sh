default_env_name = "LookOutAIenv"

# Installing virtualenv
echo "STAGE: Installing virtualenv library..."
pip install virtualenv==20.11.2 -q

# Creating virtual environment
echo "STAGE: Creating virtual environment..."
virtualenv -p python3.9 "$default_env_name"
echo "STAGE: Virtual environment '$default_env_name' has been created with Python3.9."

# Moving working wheel into virtual environment... change cp to mv later..
cp "dlib-19.22.99-cp39-cp39-win_amd64.whl" "$default_env_name/Lib/site-packages"
echo "STAGE: Moved Dlib wheel into virtual environment packages..."

# Activating virtual environment.
source $default_env_name/Scripts/activate
echo "STAGE: Activated virtual environment..."

# Installing cmake and dlib wheel.
pip install $default_env_name/Lib/site-packages/dlib-19.22.99-cp39-cp39-win_amd64.whl -q
echo "STAGE: Installed Dlib wheel..."

Installing system requirements.
echo "STAGE: Installing requirements..."
pip install -r requirements.txt -q
echo "STAGE: Requirements installed... THE FOLLOWING REQUIREMENTS HAVE NOW BEEN INSTLLED"
pip freeze
echo ""
echo "Starting System Now."

# Run Main File
python ./app/app.py