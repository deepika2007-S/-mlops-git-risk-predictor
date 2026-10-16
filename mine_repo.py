import os
import pandas as pd
from git import Repo
from radon.complexity import cc_visit

def get_file_complexity(file_content):
    try:
        blocks = cc_visit(file_content)
        if not blocks:
            return 0
        return sum([b.complexity for b in blocks]) / len(blocks)
    except Exception:
        return 0

print("Starting to scan repository history...")
repo = Repo("./")
data_log = []

# Loop through all historical commits
for commit in repo.iter_commits():
    commit_msg = commit.message.lower()
    
    # 1 if bug-related commit message, 0 if regular change
    is_bug_fix = 1 if any(word in commit_msg for word in ['fix', 'bug', 'patch', 'issue', 'hotfix']) else 0
    
    for file_path, diff in commit.stats.files.items():
        if not file_path.endswith('.py'):
            continue
            
        lines_added = diff.get('insertions', 0)
        lines_deleted = diff.get('deletions', 0)
        
        try:
            file_content = repo.git.show(f"{commit.hexsha}:{file_path}")
            complexity = get_file_complexity(file_content)
        except Exception:
            complexity = 0
            
        data_log.append({
            'lines_added': lines_added,
            'lines_deleted': lines_deleted,
            'code_complexity': complexity,
            'is_bug_prone': is_bug_fix
        })

# Export data to spreadsheet
df = pd.DataFrame(data_log)
df.to_csv('dataset.csv', index=False)
print(f"Success! Exported {len(df)} rows to dataset.csv")
