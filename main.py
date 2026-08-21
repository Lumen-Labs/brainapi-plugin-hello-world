import humanize
from datetime import timedelta
from typing import Any

from src.core.plugins.context import PluginContext


def hello_mcp_tool() -> dict[str, Any]:
    """
    A demo tool registered by the hello-world plugin.
    Returns a friendly greeting and a humanized uptime example.
    """
    uptime = humanize.naturaldelta(timedelta(seconds=12345))
    return {"message": "Hello from the hello-world plugin!", "example_uptime": uptime}


def register(context: PluginContext):
    if context._app:
        from fastapi import APIRouter

        router = APIRouter(prefix="/hello", tags=["hello-world-plugin"])

        @router.get("/")
        async def hello():
            uptime = humanize.naturaldelta(timedelta(seconds=12345))
            return {"message": "Hello from the plugin!", "example_uptime": uptime}

        @router.get("/adapters")
        async def check_adapters():
            return {"status": "adapters are accessible"}

        context.include_router(router, skip_pat=True, skip_brain=True)

    context.register_mcp_tool(hello_mcp_tool, name="hello_plugin")

    context.prompts.extend(
        "SCOUT_AGENT_SYSTEM_PROMPT",
        "\n\nAdditional instruction injected by hello-world plugin.",
    )
