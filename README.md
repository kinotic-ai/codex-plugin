# Kinotic for Codex

A Codex plugin that packages the Kinotic OS MCP connection and workflows for creating applications,
entities and repositories, services, frontends, and verifying push-to-deploy releases.

## Install

Register the GitHub marketplace:

```sh
codex plugin marketplace add kinotic-ai/codex-plugin
```

In the desktop app's Plugins directory, select **Kinotic for Codex** and install
**Kinotic**. Refresh or restart the app if the local source is not yet visible, then
start a new chat and run the plugin's setup skill. Installation is a user action;
publishing this repository does not install it into your account.

For local development, clone the repository and register its absolute directory path
with `codex plugin marketplace add /absolute/path/to/codex-plugin` instead.

The marketplace points to `./plugins/kinotic`. Keep that directory structure intact.
The plugin uses the supported `.codex-plugin/plugin.json` compatibility format and
`.mcp.json` HTTP transport configuration. See the
[official packaging guide](https://developers.openai.com/plugins/build/plugins).

## Connect

The default endpoint is **the development environment**:
`https://dev-api.kinotic.ai/mcp`, portal `https://dev-portal.kinotic.ai`.
The setup skill guides sign-in, GitHub linking, and tool discovery.

**Operator prerequisite:** Kinotic must allow the Codex OAuth client ID. Existing
Claude support alone does not establish this. The setup skill explains CIMD metadata
IDs, callbacks, and issuer settings. Live OAuth compatibility has not been verified
with a signed-in Kinotic account. No credentials are bundled.

For a different environment, edit `plugins/kinotic/.mcp.json` before installing, or
configure a separate standalone connection. Preserve the chosen endpoint throughout
the workflow. A CLI-only alternative (which configures MCP, not the bundled skills):

```sh
codex mcp add kinotic-os --url https://dev-api.kinotic.ai/mcp
codex mcp login kinotic-os --oauth-client-registration cimd
```

Avoid duplicate connections when the plugin connection already works.
See [official MCP documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

## Use

After connecting, ask:

- “Build a Kinotic inventory app with private per-user stock records.”
- “Add an Order entity and its repository to this Kinotic project.”
- “Build a frontend for my Kinotic app.”
- “Check whether my latest Kinotic deployment is running.”

The `new-app` skill replaces the Claude `/kinotic:new-app` command. You can select
the plugin's skill explicitly or ask naturally; no Claude command syntax is required.

The plugin has seven skills: setup, new-app, create-app, entities-and-persistence,
services, frontend, and deploying. Detailed SDK and MCP contracts are retained from
the pinned upstream snapshot. Actual connected tool schemas and installed SDK types
take precedence if the platform has changed.

Kinotic creates the project repository. Default-branch pushes deploy it. The workflows
preserve generated repositories and `.config/c3`, check the exact deployed commit,
and avoid deleting projects or rotating runtime secrets as troubleshooting steps.

## Verification

Run `python3 scripts/validate.py` to check package structure, manifest paths, server
wiring, skill metadata, and bundled reference links without a live account.

Before calling this production-tested, install it and verify:

1. OAuth completes and Application/Project tools are callable.
2. A test app provisions its private GitHub repository, including the GitHub-linking
   recovery path if required.
3. The clone installs, generates a first entity, and passes its type checks.
4. An authorized push reaches `RUNNING` on the exact pushed commit, and entity writes
   round-trip. A failed build preserves the prior running commit.

This package has been checked locally; the live checklist requires a Kinotic account
and GitHub access. See `plugins/kinotic/NOTICE` for provenance and `LICENSE` for terms.
