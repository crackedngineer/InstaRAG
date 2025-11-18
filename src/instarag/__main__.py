import sys
import argparse
import uvicorn
from typing import List
from rich.text import Text

from instarag.settings import console
from instarag.api import app
from instarag.core.helpers import find_available_port
from instarag.core.config_parser import ConfigParser, SourceConfig
from instarag.core.ingest import get_source_processor

class InstaRAGManager:
    def __init__(self, config_path: str, port: int = 0):
        self.port = int(port) if port else 8112
        self.config_path = config_path
        self.status_spinner = None

    @staticmethod
    def run_task(task_name: str):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                self.status_spinner.update(Text(f"{task_name}...", style="bold green"))
                try:
                    result = func(self, *args, **kwargs)
                    return result
                except Exception as e:
                    console.print(
                        f":x: [bold red]{task_name} Failed:[/bold red]\n[magenta]{e}[/magenta]"
                    )
                    return None
            return wrapper
        return decorator

    @run_task("Parsing Configuration")
    def parse_config(self, config_path: str) -> ConfigParser:
        """Parse the configuration file using ConfigParser."""
        config_parser = ConfigParser(config_path)
        config_parser.read_config()
        return config_parser.get_config()

    @run_task("Setting Up Vector Store")
    def setup_vector_store(self):
        """
        Multiple PDF store and retrival technique
        Reference :- https://colab.research.google.com/drive/1gyGZn_LZNrYXYXa-pltFExbptIe7DAPe?usp=sharing
        """
        pass

    @run_task("Setting Up Embeddings")
    def setup_embedding(self):
        pass

    @run_task("Load Source Data")
    def load_source(self, details: List[SourceConfig]):
        chunk = list()
        for detail in details:
            for file_location in detail.params:
                processor = get_source_processor(detail.type, data=file_location)
                chunk.extend(processor.process())
        return chunk

    def initialize(self) -> None:
        """
        Initialize the application workflow with Docker-like logging.
        """
        try:
            with console.status("[bold green]Starting InstaRAG Manager...[/bold green]", spinner="line") as status:
                self.status_spinner = status

                config = self.parse_config(self.config_path)
                if config is None:
                    return
                
                chunks = self.load_source(config.sources)
                if not chunks:
                    return

                embedding = self.setup_embedding()
                vector_store = self.setup_vector_store()

                # embedded_obj = self.store_embedding(embedding, vector_store, chunks)
                # ai_model = self.setup_model(config.models.chat, embedded_obj)
                
            try:
                port = find_available_port(self.port, 1)
                app.state.configuration = config
                app.state.port = port
                uvicorn.run(app, host="0.0.0.0", port=port)
            except Exception as e:
                console.print(f"[bold red][✖] Failed to Start Server:[/bold red] {e}")
            sys.stdout.flush()
        except Exception as e:
            console.print(f"[bold red][✖] Unexpected Error:[/bold red] {e}")
            return None


def main():
    parser = argparse.ArgumentParser(description="InstaRAG Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run InstaRAG Manager")
    run_parser.add_argument(
        "-f",
        "--filepath",
        required=False,
        help="Path to the config file",
    )
    run_parser.add_argument(
        "-p", "--port", type=int, default=8112, help="Port to run server on"
    )

    args = parser.parse_args()

    if args.command == "run":
        instarag_app = InstaRAGManager(config_path=args.filepath, port=args.port)
        instarag_app.initialize()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
