import os
import typer
import streamlit.web.bootstrap as st_bootstrap
from streamlit import config
from streamlit import runtime
from streamlit.web import cli as stcli
import sys

# Typer
app = typer.Typer()


@app.command()
def run(
    filepath: str = typer.Option(
        "instarag.config.yml", "-f", "--filepath", help="Path to the file"
    )
):
    script = os.path.join(os.getcwd(), "instarag", "app.py")
    # sys.argv = ["streamlit", "run", script]
    # config.set_option("server.headless", True)  # Ensures headless mode for servers
    # st_bootstrap.run(script, "", args=[], flag_options=[])

    # from streamlit.web import cli
    # cli.main_run(script, args= [])

    if runtime.exists():
        stcli.main()
    else:
        # sys.argv = ["streamlit", "run", script]
        # config.set_option("server.headless", True)  # Ensures headless mode for servers
        # st_bootstrap.run(script, "", args=[], flag_options=[])
        sys.argv = ["streamlit", "run", script, "--", "--filepath", filepath]
        sys.exit(stcli.main())


if __name__ == "__main__":
    run()
