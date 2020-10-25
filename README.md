<div align="left">
  <h1>kube-secrets-utility</h1>
</div>

- [About](#about)
  - [Status](#status)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Examples](#examples)
  - [Dump then update secrets](#dump-then-update-secrets)
- [Authors](#authors)

## About

Utility for dumping, updating and backing up Kubernetes secrets

### Status

**ALPHA** - bleeding edge / work-in-progress

## Requirements

- pyenv
- pipenv
- kubectl

## Setup

```sh
$ pipenv install --dev
$ pipenv shell
```

## Usage

```sh
$ ksu --help
Usage: ksu [OPTIONS] COMMAND [ARGS]...

  kube-secrets-utility: ksu
  Utility for dumping, updating and backing up Kubernetes secrets.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  dump    Dump decoded secrets into a yaml file.
  update  Update secrets from a yaml file.
```

```sh
$ ksu dump --help
Usage: ksu dump [OPTIONS]

  Dump decoded secrets into a yaml file.
  Examples:
    - ksu dump -n azure -ns demo -p secrets/demo
    - ksu dump -t Opaque -ns demo -p secrets/demo

Options:
  -n, --name TEXT        The secret name to manipulate.
  -t, --type TEXT        The type of secrets you want to manipulate. When name
                         is provided, type will be ignored

  -ns, --namespace TEXT  Kubernetes namespace.  [default: default]
  -p, --path TEXT        Local path where to store dumped yaml.
  --help                 Show this message and exit.
```

```sh
$ ksu update --help
Usage: ksu update [OPTIONS]

  Update secrets from a yaml file.
  Examples:
    - ksu update -ns demo -p secrets/demo/azure.yaml
    - ksu update -ns demo -p secrets/demo/Opaque-demo.yaml

Options:
  -ns, --namespace TEXT  Kubernetes namespace.  [default: default]
  -p, --path TEXT        Local path where to store dumped yaml.
  --help                 Show this message and exit.
```

## Examples

### Dump then update secrets

```sh
$ mkdir -p secrets/demo
$ ksu dump -n azure -ns demo -p secrets/demo
```

Update the secrets after modifying the `stringData` field of `secrets/demo/azure.yaml`

```sh
$ ksu update -ns demo -p secrets/demo/azure.yaml
```

## Authors

- Yifan Wu

&copy; 2020