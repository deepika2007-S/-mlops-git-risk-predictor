import sys
import os
import joblib
from git import Repo
from radon.complexity import cc_visit
from rich.console import Console
from rich.panel import Panel

console = Console()

def get_file_complexity(file_content):
    try:
        blocks = cc_visit(file_content)
        if not blocks:
            return 0
        return sum([b.complexity for b in blocks]) / len(blocks)
    except Exception:
        return 0

def assess_staged_risk():
    # 1. Load the pre-trained ML model asset
    model_path = 'bug_predictor.pkl'
    if not os.path.exists(model_path):
        console.print("[bold red]Error: Pre-trained model binary 'bug_predictor.pkl' not found![/bold red]")
        sys.exit(0)
        
    model = joblib.load(model_path)
    repo = Repo("./")
    
    # 2. Grab only the differences staged for the upcoming commit
    staged_diffs = repo.index.diff("HEAD")
    
    if not staged_diffs:
        console.print("[yellow]No staged file modifications detected to analyze.[/yellow]")
        sys.exit(0)
        
    high_risk_detected = False
    
    for diff in staged_diffs:
        file_path = diff.a_path
        if not file_path.endswith('.py'):
            continue
            
        # Parse insertion and deletion counts from the diff patch string
        diff_text = repo.git.diff("--cached", file_path)
        lines_added = len([l for l in diff_text.splitlines() if l.startswith('+') and not l.startswith('+++')])
        lines_deleted = len([l for l in diff_text.splitlines() if l.startswith('-') and not l.startswith('---')])
        
        # Read the modified local file content to evaluate structural complexity
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            complexity = get_file_complexity(content)
        except Exception:
            complexity = 0
            
        # 3. Request predictions from our Machine Learning model
        features = [[lines_added, lines_deleted, complexity]]
        risk_probability = model.predict_proba(features)[0][1] * 100
        
        # 4. Enforce our risk threshold limit rule (e.g., 60%)
        if risk_probability >= 60.0:
            high_risk_detected = True
            console.print(Panel(
                f"[bold red]❌ RISK WARNING DETECTED IN CODE CHANGES![/bold red]\n\n"
                f"[bold]File Targeted:[/bold] {file_path}\n"
                f"[bold]Lines Added:[/bold] {lines_added} | [bold]Lines Deleted:[/bold] {lines_deleted}\n"
                f"[bold]Structure Complexity Index:[/bold] {complexity:.2f}\n"
                f"[bold yellow]Defect Introduction Propensity Score: {risk_probability:.1f}%[/bold yellow]\n\n"
                f"[red]Action Required: Please refactor or simplify this file before committing.[/red]",
                title="MLOps Git Repository Risk Assessment Pipeline",
                border_style="red"
            ))
            
    if high_risk_detected:
        # Exit with a non-zero exit status to block the Git commit execution flow
        sys.exit(1)
    else:
        console.print("[bold green]✓ Code changes evaluated successfully. Risk scores optimal![/bold green]")
        sys.exit(0)

if __name__ == "__main__":
    assess_staged_risk()
