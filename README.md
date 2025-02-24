# Q-CTRL Coding challenge - Kai

## Preamble & Assumptions:
- The database is just a json file here, just to make it easy to share this code and to make it easy for others to run.
- The database will store all ingredients in metric units, amount of ingredients are for 1 serving.
- Number of servings will be integers
- For the sake of simplicity, I am ignoring ingredients that are not typically measured in a unit like "3 eggs".
   - This would also pose a problem when scaling the number of servings. If 4 servings needs 3 eggs, then one serving would need 3/4 of an egg which is wacky.


## How to run

### Set up a virtual environment (recommended)
```sh
python3 -m venv <path_to_venv>

# Bash/zsh
source <venv>/bin/activate

# Windows
<venv>\Scripts\activate.bat
```

### Install required libraries
- Flask
- Pytest
```bash
pip install flask pytest
```

### Running the server
```bash
# Normal
flask --app server.py run

# With debug info
flask --app server.py run --debug
```

### Running the tests
```bash
# -v flag for verbose mode, lists out the names of the tests run.
pytest -v tests.py
```
