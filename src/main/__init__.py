"""Infisical Dagger module

Fetch and work with secrets for your dagger application using Infisical.
"""

import dataclasses
from typing import Annotated, List, Self

from dagger import Doc, function, object_type
from infisical_sdk import InfisicalSDKClient
from infisical_sdk.client import (
    ApiV3SecretsRawGet200Response,
    ApiV3SecretsRawSecretNameGet200Response,
)


@object_type
class InfisicalDagger:
    infisical_client: InfisicalSDKClient = dataclasses.field(init=False)
    api_url: Annotated[
        dataclasses.InitVar[str],
        Doc("Your self-hosted Infisical site URL. Default: https://app.infisical.com."),
    ] = "https://app.infisical.com"

    def __post_init__(self, api_url: str):
        self.infisical_client = InfisicalSDKClient(host=api_url)

    @function
    def with_universal_auth(
        self,
        client_id: Annotated[str, Doc("Your Machine Identity Client ID")],
        client_secret: Annotated[str, Doc("Your Machine Identity Client Secret.")],
    ) -> Self:
        """Authenticate with Universal Auth"""
        self.infisical_client.auth.universal_auth.login(client_id, client_secret)
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
    ) -> ApiV3SecretsRawSecretNameGet200Response:
        """Get a secret by name"""
        secret = self.infisical_client.secrets.get_secret_by_name(
            secret_name=secret_name,
            project_id=project_id,
            environment_slug=environment_slug,
            secret_path=secret_path,
            expand_secret_references=expand_secret_references,
            include_imports=include_imports,
        )
        return secret

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
        tag_filters: Annotated[
            List[str], Doc("The comma separated tag slugs to filter secrets")
        ] = [],
    ) -> ApiV3SecretsRawGet200Response:
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
        return secrets
