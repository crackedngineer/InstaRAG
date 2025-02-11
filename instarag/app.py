from rich.console import Console
from ui_builder import UIBuilder
from config_parser import ConfigParser
from config_parser.error import ConfigReaderError
from llmgateway.ingest import get_source_processor
from llmgateway import Embedding

# Rich
console = Console()


class InstaRAGManager:
    """
    Facade class to manage the entire application workflow, including:
    - Config parsing
    - Chat model setup
    - Embedding model setup
    - Image generation model setup
    - UI building
    """

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = None

    def initialize(self) -> None:
        """
        Initialize the application workflow.
        """
        try:
            # Config Parser
            self._parse_config()

            # Load Source Data
            chunks = self.__load_source()

            # # Setup Embeddings
            embedding = self._setup_embedding_model()

            # Setup Vector Store

            # Load Enbedding in Vector Store

            # self._setup_chat_model()
            # self._setup_image_generation_model()
            self._build_ui()
        except ConfigReaderError as e:
            print(f"Configuration Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
            import traceback

            print(traceback.format_exc())

    def __load_source(self) -> list:
        chunk = list()
        for details in self.config.source:
            processor = get_source_processor(details.type, details.data)
            chunk.extend(processor.process())
        return chunk

    def _parse_config(self) -> None:
        """
        Parses the configuration file.
        """
        console.print("Parsing configuration...", style="bold green")
        config_parser = ConfigParser(self.config_path)
        config_parser.read_config()
        self.config = config_parser.get_config()
        console.print("Configuration parsed successfully.", style="bold green")

    def _setup_chat_model(self) -> None:
        """
        Sets up the chat model using the configuration.
        """
        print("Setting up chat model...")
        chat_model_config = self.config.get("models", {}).get("chat_model")
        if not chat_model_config:
            print("No chat model configuration found.")
            return
        # Example: Initialize the chat model
        print(f"Chat model setup with: {chat_model_config}")

    def _setup_embedding_model(self) -> None:
        """
        Sets up the embedding model using the configuration.
        """
        print("Setting up embedding model...")
        embedding_model_config = self.config.models.embeddings
        if not embedding_model_config:
            print("No embedding model configuration found.")
            return
        print(f"Embedding model setup with: {embedding_model_config}")

        embedding = Embedding(embedding_model_config.type)
        return embedding.load(
            embedding_model_config.model_name,
            embedding_model_config.credentials.api_key,
        )

    def _setup_image_generation_model(self) -> None:
        """
        Sets up the image generation model using the configuration.
        """
        print("Setting up image generation model...")
        image_gen_model_config = self.config.get("models", {}).get(
            "image_generation_model"
        )
        if not image_gen_model_config:
            print("No image generation model configuration found.")
            return
        # Example: Initialize the image generation model
        print(f"Image generation model setup with: {image_gen_model_config}")

    def _build_ui(self) -> None:
        """
        Builds the user interface.
        """
        print("Building the UI...")
        ui_config = self.config.get("settings", {})
        if not ui_config:
            print("No UI configuration found.")
            return
        # Example: Initialize the UI
        print(f"UI built with: {ui_config}")
        ui_builder = UIBuilder(ui_config)
        ui_builder.execute()

def main() -> None:
    import sys 
    if "--filepath" in sys.argv:
        filepath_index = sys.argv.index("--filepath") + 1
        if filepath_index < len(sys.argv):
            filepath = sys.argv[filepath_index]

    app = InstaRAGManager(config_path=filepath)
    app.initialize()


# Main Execution
if __name__ == "__main__":
    main()
