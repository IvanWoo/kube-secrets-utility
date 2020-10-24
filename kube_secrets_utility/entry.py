import click

from kube_secrets_utility.config import LOG_LEVEL
from kube_secrets_utility.log import get_logger
from kube_secrets_utility.utils import dump_many_by_type, dump_one, is_exist

logger = get_logger(__name__, LOG_LEVEL)


@click.command()
@click.option("-n", "--name", help="The secret name to manipulate.")
@click.option(
    "-t",
    "--type",
    help="The type of secrets you want to manipulate. When name is provided, type will be ignored",
)
@click.option("-ns", "--namespace", default="default", help="Kubernetes namespace.")
@click.option("-p", "--path", help="Local path where to store dumped yaml.")
@click.version_option()
def main(
    name,
    type,
    namespace,
    path,
):
    """
    kube-secrets-utility: ksu

    Examples:

      - ksu -n azure -ns demo -p secrets/demo

      - ksu -t Opaque -ns demo -p secrets/demo
    """
    if not is_exist(path):
        logger.error(f"{path} not existed")
        return
    if name:
        dump_one(name, namespace, path)
    elif namespace:
        dump_many_by_type(type, namespace, path)
    return
