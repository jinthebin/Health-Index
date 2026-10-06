import os
import contextlib

# Show the current working directory before the context
print("Before:", os.getcwd())

# Temporarily change directory to the parent folder
with contextlib.chdir("dat/"):
    print("Inside:", os.getcwd())  # This will be the parent directory

# After the block, the working directory is restored
print("After:", os.getcwd())
