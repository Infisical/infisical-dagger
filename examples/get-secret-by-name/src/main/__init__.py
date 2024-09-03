"""A generated module for Test functions

This module has been generated via dagger init and serves as a reference to
basic module structure as you get started with Dagger.

Two functions have been pre-created. You can modify, delete, or add to them,
as needed. They demonstrate usage of arguments and return types using simple
echo and grep commands. The functions can be called from the dagger CLI or
from one of the SDKs.

The first line in this comment block is a short description line and the
rest is a long description with more detail on the module's purpose or usage,
if appropriate. All modules should have a short description.
"""

from typing import Annotated
from dagger import Doc, Secret, dag, function, object_type

# NOTE: it's recommended to move your code into other files in this package
# and keep __init__.py for imports only, according to Python's convention.
# The only requirement is that Dagger needs to be able to import a package
# called "main", so as long as the files are imported here, they should be
# available to Dagger.


@object_type
class Test:
    @function
    async def test(
        self,
        client_id: Annotated[Secret, Doc("Your Machine Identity Client ID")],
        client_secret: Annotated[Secret, Doc("Your Machine Identity Client Secret.")],
        secret_name: Annotated[str, Doc("The name of the secret to get.")],
        project_id: Annotated[
            str, Doc("The ID of the project to get the secret from.")
        ],
        environment_slug: Annotated[
            str, Doc("The slug of the environment to get the secret from.")
        ],
    ) -> str:
        """Returns a container that echoes whatever string argument is provided"""
        test_secret: Secret = (
            dag.infisical()
            .with_universal_auth(client_id, client_secret)
            .get_secret_by_name(
                project_id=project_id,
                environment_slug=environment_slug,
                secret_path="/",
                secret_name=secret_name,
            )
        )

        return await (
            dag.container()
            .from_("alpine:latest")
            .with_secret_variable("TEST", test_secret)
            .with_exec(["sh", "-c", 'echo "hello $TEST"'])
            .stdout()
        )
