import click

from source.client import Client
from source.scrapper import Scrapper


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("Type 'python cli.py run -p <phrase>' to run scrapper or use --help.")
    else:
        click.echo(click.style("Running", blink=True))


@cli.command()
@click.option("-p", "--phrase", required=True, type=str, help="Scrap for specific phrase")
def run(phrase: str) -> None:
    """Run scraper."""

    scrapper = Scrapper(phrase)
    scrapper.get_similar_words()
    scrapper.scrap_raw_data()

    mongo_client = Client()
    mongo_client.set_db()
    mongo_client.insert(data=scrapper.scrapped, collection=phrase)
    click.echo(f"{len(scrapper.scrapped)} records saved in database.")


@cli.command()
@click.option("-o", "--output-dir", type=click.Path(dir_okay=True), help="Export data from database")
def export(output_dir: str) -> None:
    """Export collections to csv."""

    mongo_client = Client()
    mongo_client.set_db()
    all_collections = mongo_client.collections()
    documents = mongo_client.fetch_documents(all_collections)
    df = mongo_client.convert_to_df(documents)
    mongo_client.export_to_csv(df, output_dir)


@cli.command()
@click.option("-c", "--collection-name", type=click.Path(dir_okay=True), help="Export data from database")
def delete(collection_name: str) -> None:
    """Delete collection from DB."""

    mongo_client = Client()
    mongo_client.set_db()
    mongo_client.delete_collection(collection_name)


@cli.command()
def show() -> None:
    """Show all collections."""

    mongo_client = Client()
    mongo_client.set_db()
    mongo_client.collections()


if __name__ == '__main__':
    cli()
