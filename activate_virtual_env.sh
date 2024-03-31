DIR=$(realpath $(dirname "${BASH_SOURCE[0]}"))
MLROOT=$DIR
export MLROOT

if [ ! -e "$DIR/virtual_env/bin/activate" ]; then
  python3 -m venv "$DIR/virtual_env" || return # exit on error
  source "$DIR/virtual_env/bin/activate"
  echo "Activated virtual env"
  pip3 install --upgrade pip wheel
  pip3 install -e .
  pip3 install pre-commit
  pre-commit install
else
  source "$DIR/virtual_env/bin/activate"
  echo "Activated virtual env"
fi
