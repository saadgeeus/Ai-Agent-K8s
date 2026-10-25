# aiops/cli.py
# Command Line Interface entry point using Click.
import click
from .agent import initialize_agent_executor, run_diagnosis
from .sop import generate_sop_document

# Module-level placeholder — agent is initialized lazily when first needed.
# This means --help and other commands work even if Ollama is not running.
_agent_executor = None

def get_agent():
    """Returns the agent executor, initializing it on first use (lazy init)."""
    global _agent_executor
    if _agent_executor is None:
        try:
            click.echo("🔌 Connecting to Ollama and loading model...")
            _agent_executor = initialize_agent_executor()
        except Exception as e:
            click.echo(f"🚨 ERROR: Could not start AIOps Agent. Is Ollama running with gemma4 loaded?")
            click.echo(f"   Details: {e}")
    return _agent_executor


@click.group()
def cli():
    """
    AIOps CLI: Autonomous Diagnostic Tool for Kubernetes Clusters.
    Use 'python -m AIOps [COMMAND] --help' for details.
    """
    pass


@cli.command(name="scan")
@click.option('--query', '-q', default="Run a general health scan on the cluster and detect anomalies.", help="Specific query for the agent to focus on.")
def doctor_scan(query: str):
    """
    Performs an initial health scan of the Kubernetes cluster to detect anomalies.
    This is the entry point for diagnosis.
    """
    agent = get_agent()
    if not agent:
        return

    click.echo("=========================================")
    click.echo("✅ Starting initial AIOps Cluster Scan...")
    click.echo("=========================================")

    rca_report = run_diagnosis(agent, query)

    click.echo("\n\n" + "="*20 + " DIAGNOSIS COMPLETE " + "="*20)
    click.echo(rca_report)
    click.echo("="*58 + "\n")
    click.echo("💡 Next Step: Run 'python -m AIOps document \"<paste RCA above>\"' to generate an SOP.")


@cli.command(name="analyze")
@click.argument('report_content', type=str)
def doctor_analyze(report_content: str):
    """
    Analyzes a specific report or raw output to generate a focused RCA (Root Cause Analysis).
    """
    agent = get_agent()
    if not agent:
        return

    click.echo("=========================================")
    click.echo("🔬 Starting Targeted RCA Analysis...")
    click.echo("=========================================")

    full_query = f"Initial Diagnostics:\n{report_content}\n\nTASK: Based on the above diagnostics, provide a formal RCA following the AIOps Doctor format."
    rca_report = run_diagnosis(agent, full_query)

    click.echo("\n\n" + "="*20 + " RCA GENERATED " + "="*20)
    click.echo(rca_report)
    click.echo("="*58 + "\n")


@cli.command(name="document")
@click.argument('rca_output', type=str)
def doctor_document(rca_output: str):
    """
    Generates and saves a Standard Operating Procedure (SOP) document from the completed RCA.
    """
    click.echo("=========================================")
    click.echo("📜 Starting SOP Generation...")
    click.echo("=========================================")

    sop_status = generate_sop_document(rca_output)

    click.echo("\n" + "="*20 + " DOCUMENTATION COMPLETE " + "="*20)
    click.echo(sop_status)
    click.echo("Check your docs/ folder for the generated SOP file.")


@cli.command(name="fix")
def doctor_fix():
    """
    (Planned) Generate and suggest specific kubectl remediation commands based on RCA.
    """
    click.echo("⚠️  Feature Not Yet Implemented.")
    click.echo("The 'fix' command will use the Agent to generate kubectl fixes based on the RCA.")


# Allow running as: python AIOps/cli.py directly
if __name__ == "__main__":
    cli()
