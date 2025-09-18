import os
import sys
import argparse
from rich.console import Console
import uvicorn

from api import app
from utils import (
    parse_config,
    # load_source,
    setup_vector_store,
    setup_embedding,
    store_embedding,
    # setup_model,
)
from helpers import find_available_port

# Rich
console = Console()


class InstaRAGManager:
    def __init__(self, config_path: str, port: int = 0):
        self.port = port
        self.config_path = os.path.join(os.getcwd(), config_path)
        console.print(f"[bold cyan][⏳] Configuring Path...[/bold cyan]", end="\r")
        sys.stdout.flush()

        try:
            console.print(
                f"[bold green][✔] Config Path Set:[/bold green] {self.config_path}"
            )
        except Exception as e:
            console.print(f"[bold red][✖] Failed to Set Config Path:[/bold red] {e}")
        sys.stdout.flush()

    def initialize(self) -> None:
        """
        Initialize the application workflow with Docker-like logging.
        """
        try:
            console.rule("[bold blue]🚀 Initializing InstaRAG[/bold blue]")
            sys.stdout.flush()

            # Step-by-step initialization
            config = self.run_task(
                "Parsing Configuration", parse_config, self.config_path
            )
            if not config:
                return

            # chunks = self.run_task("Loading Source Data", load_source, config.source)
            # if not chunks:
            #     return

            vector_store = self.run_task("Setting Up Vector Store", setup_vector_store)
            # if not vector_store:
            #     return

            embedding = self.run_task("Setting Up Embeddings", setup_embedding)
            # if not embedding:
            #     return

            # embedded_obj = self.run_task(
            #     "Storing Embeddings in Vector Store",
            #     store_embedding,
            #     embedding,
            #     vector_store,
            #     chunks,
            # )
            # if not embedded_obj:
            #     return

            # ai_model = self.run_task(
            #     "Setting Up Chat Model", setup_model, config.models.chat, embedded_obj
            # )
            # if not ai_model:
            #     return

            # Start the server
            console.print(
                "[bold cyan][⏳] Starting InstaRAG Server...[/bold cyan]", end="\r"
            )
            sys.stdout.flush()

            try:
                port = find_available_port(self.port or 8112, 1 if self.port else 100)
                # app.state.model = ai_model  # Set AI model before starting
                app.state.configuration = config
                app.state.port = port
                uvicorn.run(app, host="0.0.0.0", port=port)
            except Exception as e:
                console.print(f"[bold red][✖] Failed to Start Server:[/bold red] {e}")
            sys.stdout.flush()

        except Exception as e:
            console.print(f"[bold red][✖] Unexpected Error:[/bold red] {e}")
            sys.stdout.flush()

    def run_task(self, task_name, func, *args):
        """
        Runs a task with a spinner and updates the state like Docker logs.
        """
        console.print(f"[bold cyan][⏳] {task_name}...[/bold cyan]", end="\r")
        sys.stdout.flush()

        try:
            result = func(*args) if args else func()
            console.print(f"[bold green][✔] {task_name} Completed[/bold green]")
            sys.stdout.flush()
            return result
        except Exception as e:
            console.print(f"[bold red][✖] {task_name} Failed:[/bold red] {e}")
            sys.stdout.flush()
            return None


def main():
    try:
        parser = argparse.ArgumentParser(description="InstaRAG Manager CLI")
        subparsers = parser.add_subparsers(dest="command")

        run_parser = subparsers.add_parser("run", help="Run InstaRAG Manager")
        run_parser.add_argument(
            "-f",
            "--filepath",
            default="instarag.config.yaml",
            help="Path to the config file",
        )
        run_parser.add_argument("-p", "--port", default=0, help="default port")

        args = parser.parse_args()

        if args.command == "run":
            instarag_app = InstaRAGManager(config_path=args.filepath, port=args.port)
            instarag_app.initialize()
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error during execution: {e}")


if __name__ == "__main__":
    main()
