import base64
import shlex
import subprocess
from pathlib import Path

import yaml

from kube_secrets_utility.log import get_logger

logger = get_logger(__name__)


def run(cmd):
    return subprocess.run(shlex.split(cmd), capture_output=True)


def decode(secret):
    string_data = {
        k: base64.b64decode(v).decode("utf8")
        for k, v in secret["data"].items()
        if not k.startswith(".")
    }
    return string_data


def clean(secret):
    """
    remove `data` filed and all `metadata` of the secret except `name`
    """
    for k in [k for k in secret["metadata"].keys() if k not in ["name"]]:
        secret["metadata"].pop(k, None)
    secret.pop("data", None)
    return secret


def translate(secret):
    """
    decode base64 `data` and save it to `stringData` field
    """
    string_data = decode(secret)
    secret["stringData"] = string_data
    secret = clean(secret)
    return secret


def is_exist(path):
    p = Path(path)
    return p.exists()


def is_file(path):
    p = Path(path)
    return p.is_file()


def is_dir(path):
    p = Path(path)
    return p.is_dir()


def save(content, file):
    file_path = Path(file)
    file_path.touch(exist_ok=True)
    with open(file, "w+") as f:
        yaml.dump(content, f)
    logger.info(f"dumped yaml is saved at {file}")
    return


def dump_one(secret_name, namespace, path):
    res = run(f"kubectl get secret {secret_name} -n {namespace} -o yaml")
    if not res.stdout:
        logger.error(
            f"empty response: make sure the secret({secret_name}) exists at {namespace}"
        )
    if res.stderr:
        logger.warning(res.stderr)
        return

    secret = yaml.safe_load(res.stdout)
    secret = translate(secret)
    logger.debug(secret)

    file = f"{path}/{secret['metadata']['name']}.yaml"
    save(secret, file)
    return


def dump_many_by_type(type, namespace, path):
    res = run(f"kubectl get secret --field-selector type={type} -n {namespace} -o yaml")
    if not res.stdout:
        logger.error(f"empty response: no secret of {type} exists at {namespace}")
        return
    if res.stderr:
        logger.warning(res.stderr)
        return

    secrets = yaml.safe_load(res.stdout)

    for secret in secrets["items"]:
        secret = translate(secret)
        logger.debug(secret)

    file = f"{path}/{type.replace('/', '-')}-{namespace}.yaml"
    save(secrets, file)
    return


def delete(namespace, path):
    res = run(f"kubectl delete -n {namespace} -f {path}")
    if res.stderr:
        logger.warning(res.stderr)
        return
    logger.info(res.stdout)
    return


def apply(namespace, path):
    res = run(f"kubectl apply -n {namespace} -f {path}")
    if res.stderr:
        logger.warning(res.stderr)
        return
    logger.info(res.stdout)
    return


def update_one(namespace, path):
    delete(namespace, path)
    apply(namespace, path)
    return


update_many = update_one
