# Infisical Dagger

This module is part of the Daggerverse, a collection of reusable Dagger modules.

## Description

The Infisical Dagger Module is an official integration that seamlessly connects your Dagger workflows with **[Infisical](https://infisical.com)**. Infisical is the open source secret management platform that teams use to centralize their secrets like API keys, database credentials, and configurations.

## Features

- Get secret by key
- List secrets

## Installation

```shell
dagger install github.com/Infisical/infisical-dagger@<version-number>
```

## Usage

### CLI

```bash
dagger call with-universal-auth --client-id=env:CLIENT_ID --client-secret=env:CLIENT_SECRET get-secret-by-name --project-id="<project-id>" --secret-name="<SECRET-NAME>" --environment-slug="<slug>" --secret-path="/"
```

### Dagger Function

```python
 dag.infisical()
            .with_universal_auth(client_id, client_secret)
            .get_secrets(
                project_id=project_id,
                environment_slug=environment_slug,
                secret_path="/",
            )
```

## License

Specify the license for your module:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
