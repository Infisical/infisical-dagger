# Basic Example

Ideally, set up a Virtual Env with the Dagger Python SDK to run in:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip dagger-io
```

Then to run the example:

```
dagger call test --client-id=env:CLIENT_ID --client-secret=env:CLIENT_SECRET --project-id="<project-id>" --secret-name="TEST" --environment-slug="dev"
```
