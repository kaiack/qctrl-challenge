# Q-CTRL Coding challenge - Kai

# Preamble / Assumptions:
- The database is just a json file here, just to make it easy to share this code and to make it easy for others to run.
- The database will store all ingredients in metric units, amount of ingredients are for 1 serving.
- For the sake of simplicity, I am ignoring elements where they are not typically measured in a unit like "3 eggs".
   - This would also pose a problem when scaling the number of servings. If 4 servings needs 3 eggs, then one serving would need 3/4 of an egg which is wacky.


## Required libraries
- Flask
- Pytest# qctrl-challenge
