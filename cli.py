import click
import time
from source.scrapper import Scrapper
from datetime import timedelta
from source.client import Client


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("Type 'python cli.py run -p <phrase>' to run scrapper.")
    else:
        click.echo(click.style("Running", blink=True))


@cli.command()
@click.option("-p", "--phrase", required=True, type=str)
def run(phrase: str) -> None:
    scrapper = Scrapper(phrase)
    scrapper.get_similar_words()
    start_time = time.monotonic()
    scrapper.scrap_raw_data()
    end_time = time.monotonic()
    print(timedelta(seconds=end_time - start_time))

    mongo_client = Client()
    mongo_client.set_db()
    mongo_client.insert({"XXX": "YYY"}, "TEST")


if __name__ == '__main__':
    cli()
