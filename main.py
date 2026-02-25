import asyncio
import logging
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from core.config import settings, setup_logging
from core.client import WPClient
from skills.posts_skill import PostsSkill
from skills.acf_skill import ACFSkill
from skills.analytics_skill import AnalyticsSkill
from skills.report_skill import ReportSkill

# Setup UI
console = Console()

async def run_agent():
    setup_logging()
    
    console.print(Panel.fit(
        "[bold blue]WordPress Integration Agent[/bold blue]
"
        "[dim]Automating your WordPress workflow[/dim]",
        border_style="green"
    ))

    # Initialize Client & Skills
    try:
        client = WPClient()
        posts_skill = PostsSkill(client)
        acf_skill = ACFSkill(client)
        report_skill = ReportSkill()
        
        # Analytics is optional if not configured
        analytics_skill = None
        if settings.GA4_PROPERTY_ID and settings.GA4_CREDENTIALS_PATH:
            analytics_skill = AnalyticsSkill()
    except Exception as e:
        console.print(f"[bold red]Error initializing skills:[/bold red] {e}")
        return

    while True:
        command = Prompt.ask("
[bold cyan]Agent Command[/bold cyan] (list, create, analytics, exit)")
        
        if command == "exit":
            console.print("[yellow]Goodbye![/yellow]")
            break
            
        elif command == "list":
            count = Prompt.ask("How many posts?", default="5")
            posts = await posts_skill.list_posts(count=int(count))
            
            table = Table(title="Recent Posts")
            table.add_column("ID", style="dim")
            table.add_column("Title")
            table.add_column("Status")
            
            for p in posts:
                table.add_row(str(p['id']), p['title']['rendered'], p['status'])
            console.print(table)

        elif command == "create":
            title = Prompt.ask("Post Title")
            content = Prompt.ask("Post Content")
            post = await posts_skill.create_post(title, content, status="draft")
            console.print(f"[green]Draft created successfully! ID: {post['id']}[/green]")

        elif command == "analytics":
            if not analytics_skill:
                console.print("[red]Analytics not configured. Please set GA4_PROPERTY_ID and credentials path in .env.[/red]")
                continue
            
            days = Prompt.ask("Days to analyze?", default="30")
            console.print("[yellow]Fetching GA4 data...[/yellow]")
            data = await analytics_skill.get_basic_report(days=int(days))
            
            if data:
                table = Table(title=f"Traffic Report (Last {days} Days)")
                table.add_column("Date")
                table.add_column("Users")
                table.add_column("Sessions")
                table.add_column("Page Views")
                
                for row in data[:10]: # Show first 10
                    table.add_row(row['date'], row['active_users'], row['sessions'], row['page_views'])
                console.print(table)
                
                if Prompt.confirm("Export to CSV?"):
                    path = report_skill.export_to_csv(data, "analytics_report")
                    console.print(f"[green]Report saved: {path}[/green]")
            else:
                console.print("[red]No data retrieved.[/red]")

        else:
            console.print(f"[dim]Unknown command: {command}[/dim]")

if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        console.print("
[yellow]Interrupted by user. Exiting...[/yellow]")
        sys.exit(0)
