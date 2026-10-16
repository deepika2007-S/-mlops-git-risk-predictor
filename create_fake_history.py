import os
import random
from git import Repo

def create_fake_history():
    print("Initializing dummy repository and generating fake history...")
    
    if not os.path.exists('.git'):
        repo = Repo.init('.')
    else:
        repo = Repo('.')
        
    filename = 'sample_app.py'
    
    for i in range(1, 31):
        lines_count = random.randint(10, 100)
        complexity_loops = "    for x in range(10):\n        print(x)\n" * random.randint(1, 5)
        
        code_content = f"""# Mock Python File - Commit Version {i}
def core_function():
    print("Running system update version {i}")
{complexity_loops}
    return True
"""
        with open(filename, 'w') as f:
            f.write(code_content)
            
        repo.index.add([filename])
        
        if i % 4 == 0:
            commit_message = f"Fixed critical index bug in system component patch #{i}"
        elif i % 7 == 0:
            commit_message = f"Hotfix for memory leak issue #{i}"
        else:
            commit_message = f"Refactored code structure and updated features variation {i}"
            
        repo.index.commit(commit_message)
        
    print(f"Success! Generated 30 synthetic commits on {filename}.")

if __name__ == "__main__":
    create_fake_history()
