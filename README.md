# kube-secrets-utility

Utility for dumping, updating and backing up Kubernetes secrets

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
Usage: ksu [OPTIONS]

  kube-secrets-utility: ksu
  Examples:
    - ksu -n azure -ns demo -p secrets/demo
    - ksu -t Opaque -ns demo -p secrets/demo

Options:
  -n, --name TEXT        The secret name to manipulate.
  -t, --type TEXT        The type of secrets you want to manipulate. When name
                         is provided, type will be ignored

  -ns, --namespace TEXT  Kubernetes namespace.  [default: default]
  -p, --path TEXT        Local path where to store dumped yaml.
  --version              Show the version and exit.
  --help                 Show this message and exit.
```

## Examples

### Update secrets

```sh
$ mkdir -p secrets/demo
$ ksu -n azure-secret -ns default -p secrets/demo
```

Apply the updated secrets after modifying the `stringData` field of `secrets/demo/azure-secret.yaml`

```sh
$ kubectl apply -f secrets/demo/azure-secret.yaml
```
