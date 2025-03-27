DIR=$(realpath $(dirname "${BASH_SOURCE[0]}"))
MLROOT=$DIR
export MLROOT

if [ ! -e "$DIR/.venv/bin/activate" ]; then
  python3 -m venv "$DIR/.venv" || return # exit on error
  source "$DIR/.venv/bin/activate"
  echo "Activated .venv"
  pip3 install --upgrade pip wheel
  pip3 install -e .
  pip3 install pre-commit
  pre-commit install
else
  source "$DIR/.venv/bin/activate"
  echo "Activated .venv"
fi
