"""Infisical Dagger module

Fetch and work with secrets for your dagger application using Infisical.
"""

import dataclasses
from typing import Annotated, Self

from dagger import Doc, dag, function, object_type, Secret
from infisical_sdk import InfisicalSDKClient


@object_type
class Infisical:
    infisical_client: InfisicalSDKClient = dataclasses.field(init=False)
    api_url: Annotated[
        dataclasses.InitVar[str],
        Doc("Your self-hosted Infisical site URL. Default: https://app.infisical.com."),
    ] = "https://app.infisical.com"

    def __post_init__(self, api_url: str):
        self.infisical_client = InfisicalSDKClient(host=api_url)

    @function
    async def with_universal_auth(
        self,
        client_id: Annotated[Secret, Doc("Your Machine Identity Client ID")],
        client_secret: Annotated[Secret, Doc("Your Machine Identity Client Secret.")],
    ) -> Self:
        """Authenticate with Universal Auth"""
        client_id_dagger_secret = await client_id.plaintext()
        client_secret_dagger_secret = await client_secret.plaintext()
        self.infisical_client.auth.universal_auth.login(
            client_id_dagger_secret, client_secret_dagger_secret
        )
        return self

    @function
    def get_secret_by_name(
        self,
        secret_name: Annotated[str, Doc("The name of the secret to get.")],
        project_id: Annotated[
            str, Doc("The ID of the project to get the secret from.")
        ],
        environment_slug: Annotated[
            str, Doc("The slug of the environment to get the secret from.")
        ],
        secret_path: Annotated[str, Doc("The path of the secret to get.")],
        expand_secret_references: Annotated[
            bool, Doc("Whether or not to expand secret references")
        ] = True,
        include_imports: Annotated[
            bool, Doc("Weather to include imported secrets or not.")
        ] = True,
    ) -> Secret:
        """Get a secret by name"""
        secret = self.infisical_client.secrets.get_secret_by_name(
            secret_name=secret_name,
            project_id=project_id,
            environment_slug=environment_slug,
            secret_path=secret_path,
            expand_secret_references=expand_secret_references,
            include_imports=include_imports,
        )
        return dag.set_secret(secret_name, secret.secret.secret_value)

    @function
    def get_secrets(
        self,
        project_id: Annotated[
            str, Doc("The ID of the project to get the secret from.")
        ],
        environment_slug: Annotated[
            str, Doc("The slug of the environment to get the secret from.")
        ],
        secret_path: Annotated[str, Doc("The path of the secret to get.")],
        expand_secret_references: Annotated[
            bool, Doc("Whether or not to expand secret references")
        ] = True,
        recursive: Annotated[
            bool,
            Doc(
                "Whether or not to fetch all secrets from the specified base path, and all of its subdirectories. Note, the max depth is 20 deep."
            ),
        ] = False,
        include_imports: Annotated[
            bool, Doc("Weather to include imported secrets or not.")
        ] = True,
        tag_filters: list[str] = [],
    ) -> list[Secret]:
        """List secrets"""
        secrets = self.infisical_client.secrets.list_secrets(
            project_id=project_id,
            environment_slug=environment_slug,
            secret_path=secret_path,
            expand_secret_references=expand_secret_references,
            include_imports=include_imports,
            recursive=recursive,
            tag_filters=tag_filters,
        )
        computed_secrets: dict[str, str] = {}
        for secret in secrets.secrets:
            computed_secrets[secret.secret_key] = secret.secret_value
        for imported_secrets in reversed(secrets.imports):
            for secret in imported_secrets:
                if computed_secrets[secret.secret_key] is None:
                    computed_secrets[secret.secret_key] = secret.secret_value

        final_secrets: list[Secret] = []
        for secret_key, secret_value in computed_secrets.items():
            final_secrets.append(dag.set_secret(secret_key, secret_value))

        return final_secrets
