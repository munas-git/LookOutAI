# Installing virtualenv
echo "STAGE: Installing virtualenv library..."
pip install virtualenv==20.11.2 -q

# Creating virtual environment
echo "STAGE: Creating virtual environment..."
virtualenv -p python3.9 "$env_name"
echo "STAGE: Virtual environment '$env_name' has been created with Python3.9."

# Moving working wheel into virtual environment... change cp to mv later..
# cp "dlib-19.22.99-cp39-cp39-win_amd64.whl" "$env_name/Lib/site-packages"
# echo "STAGE: Moved Dlib wheel into virtual environment packages..."

# Activating virtual environment.
source $env_name/Scripts/activate
echo "STAGE: Activated virtual environment..."


# Installing cmake and dlib wheel.
# pip install $env_name/Lib/site-packages/dlib-19.22.99-cp39-cp39-win_amd64.whl -q
# echo "STAGE: Installed Dlib wheel..."

# Installing system requirements.
# echo "STAGE: Installing requirements..."
# pip install -r requirements.txt -q
# echo "STAGE: Requirements installed"






# Default virtual environment name
default_env_name="LookOutAIenv"

# Parse optional argument for environment name
env_name=${1:-$default_env_name}

# Sanitize the environment name (remove spaces and replace them with hyphens)
env_name=$(echo "$env_name" | sed 's/ /-/g')
echo "Your virtual environment will be named '$env_name'"

# Stop on error.
set -o errexit

# Updating pip version on original environment.
pip install -U pip

# Installing virtualenv.
pip install virtualenv==20.11.2

# Creating virtual environment.
virtualenv -p python3.9 "../system-env"

# Move wheel into virtual environment..... CHANGE FROM COPY TO MOVE LATER.
cp "./dlib-19.22.99-cp39-cp39-win_amd64.whl" "../system-env/Lib/site-packages"

# Activating virtual environment.
source ../system-env/Scripts/activate

# Installing dlib wheel.
pip install ../system-env/Lib/site-packages/dlib-19.22.99-cp39-cp39-win_amd64.whl

# Updating pip version in the virtual environment.
# pip install -U pip
# This requires admin priviledge hence commented out for now.

# Installing system requirements.
pip install -r ../requirements.txt

# Displaying installed requirements.
echo "THE FOLLOWING REQUIREMENTS HAVE NOW BEEN INSTLLED"
pip freeze
echo ""
echo "Starting System Now."

# Run Main File
python ../main.py