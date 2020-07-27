# How to run
```
pipenv install
pipenv install pandas random-word requests 
python spotiparser.py
```

## To do
1. Exception handling for errors
   1. Words are not found for Spotify
   2. Random generator breaks
   3. Empty arrays (maybe not a breaking bug however) 
2. Tame the random word generator so that it behaves itself.
3. Decide how to store this. 
   1. Write a function that appends results to a master file.
4. Decide what part of runmemore() should become a Class / method
