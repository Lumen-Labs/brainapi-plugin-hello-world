# hello-world

Minimal BrainAPI plugin that shows the three extension points a plugin can use at once: a REST route, an MCP tool, and a prompt injection.

Use this package as a template when you are writing your first plugin.

| | |
|---|---|
| Registry name | `hello-world` |
| Version | `1.0.0` |
| BrainAPI | `>=2.9.0` |
| Priority | `100` |
| Extra pip deps | `humanize` |

## What it does

On load, `register(context)`:

1. Mounts `GET /hello/` and `GET /hello/adapters` (API runtime only).
2. Registers an MCP tool named `hello_plugin`.
3. Appends an extra instruction onto `SCOUT_AGENT_SYSTEM_PROMPT`.

The HTTP routes are mounted with `skip_pat=True` and `skip_brain=True`, so they do **not** require a BrainPAT or brain id. That is intentional for a smoke-test plugin. Real plugins should keep the default auth.

## Install

From a BrainAPI checkout (`>=2.9.0`):

```bash
git clone https://github.com/Lumen-Labs/brainapi-plugin-hello-world.git plugins/hello-world
```

Or from the [plugin registry](https://registry.brain-api.dev/app):

```bash
./bin/brainapi install hello-world
# poetry run brainapi plugins install hello-world
```

Restart the API (and the MCP server if you want the tool). BrainAPI installs `humanize` from `plugin.yaml` before importing the entry point.

## Quick start

```bash
curl -s http://localhost:8000/hello/
# {"message":"Hello from the plugin!","example_uptime":"3 hours, 25 minutes"}

curl -s http://localhost:8000/hello/adapters
# {"status":"adapters are accessible"}
```

`example_uptime` is `humanize.naturaldelta(timedelta(seconds=12345))` — a fixed demo value, not process uptime.

## MCP tool

When the MCP runtime loads this plugin it registers:

| Tool name | Callable | Returns |
|---|---|---|
| `hello_plugin` | `hello_mcp_tool()` | `{ "message", "example_uptime" }` |

Point an MCP client at BrainAPI’s MCP server and list tools to confirm `hello_plugin` is present.

## Prompt injection

The plugin calls:

```python
context.prompts.extend(
    "SCOUT_AGENT_SYSTEM_PROMPT",
    "\n\nAdditional instruction injected by hello-world plugin.",
)
```

After restart, Scout’s system prompt includes that extra paragraph. This is the same hook production plugins use to constrain extraction ontologies.

## Layout

```text
hello-world/
  plugin.yaml    # name, version, entry_point, pip_dependencies
  main.py        # register(context)
  LICENSE
```

`entry_point: main` means BrainAPI imports `main.py` and calls `register`.

## Publishing

Pushes to `main` pack this directory into a `.tar.gz` and upload it to `https://registry.brain-api.dev` (GitHub Action **Publish to BrainAPI registry**). Manual republish: Actions → Run workflow, optionally with **force**.

## License

Business Source License 1.1. See [LICENSE](LICENSE).

## Related

- [BrainAPI](https://github.com/Lumen-Labs/brainapi2)
- [Plugin docs](https://brainapi.lumen-labs.ai/docs/plugins)
- [chatbot](https://github.com/Lumen-Labs/brainapi-plugin-chatbot)
