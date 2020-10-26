from functools import partial

import click

from kube_secrets_utility.log import get_logger
from kube_secrets_utility.utils import (
    dump_many_by_type,
    dump_one,
    is_dir,
    is_exist,
    is_file,
    update_many,
    update_one,
)

logger = get_logger(__name__)
# https://github.com/pallets/click/issues/646#issuecomment-435317967
click.option = partial(click.option, show_default=True)


@click.group()
@click.version_option()
def cli():
    """
    \b
    kube-secrets-utility: ksu
    Utility for dumping, updating and backing up Kubernetes secrets.
    """
    pass


@cli.command()
@click.option("-n", "--name", help="The secret name to manipulate.")
@click.option(
    "-t",
    "--type",
    help="The type of secrets you want to manipulate. When name is provided, type will be ignored",
)
@click.option("-ns", "--namespace", default="default", help="Kubernetes namespace.")
@click.option("-p", "--path", help="Local path where to store dumped yaml.")
def dump(
    name,
    type,
    namespace,
    path,
):
    """
    \b
    Dump decoded secrets into a yaml file.
    Examples:
      - ksu dump -n azure -ns demo -p secrets/demo
      - ksu dump -t Opaque -ns demo -p secrets/demo
    """
    if not is_exist(path):
        logger.error(f"{path} does not exist")
        return
    if name:
        dump_one(name, namespace, path)
    elif namespace:
        dump_many_by_type(type, namespace, path)
    return


@cli.command()
@click.option("-ns", "--namespace", default="default", help="Kubernetes namespace.")
@click.option("-p", "--path", help="Local path where to store dumped yaml.")
def update(namespace, path):
    """
    \b
    Update secrets from a yaml file.
    Examples:
      - ksu update -ns demo -p secrets/demo/azure.yaml
      - ksu update -ns demo -p secrets/demo/Opaque-demo.yaml
    """
    if not is_exist(path):
        logger.error(f"{path} does not exist")
        return
    if is_file(path):
        update_one(namespace, path)
    elif is_dir(path):
        update_many(namespace, path)
    else:
        logger.error(f"{path} is neither file nor path")
    return


main = cli


if __name__ == "__main__":
    main()
