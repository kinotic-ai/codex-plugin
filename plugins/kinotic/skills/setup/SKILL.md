---
name: setup
description: Connect Codex to Kinotic OS, guide account signup, and diagnose Kinotic MCP OAuth or missing tools. Use when setting up the Kinotic plugin or changing its server.
---

# Connect Kinotic OS

The plugin bundles a remote HTTP MCP server named `kinotic-os` at
`https://dev-api.kinotic.ai/mcp`. Its portal is `https://dev-portal.kinotic.ai`.
This is the upstream development environment. Use a different endpoint when the user
has selected one; do not silently switch environments or send credentials elsewhere.

## Discover before reconnecting

Search available tool names and descriptions for `Application Service` and
`Project Service`. Kinotic tool names are opaque hashes. Select by the full title at
the beginning of each description, including the service name; inspect the actual
tool schema before calling it. Deferred tools may need discovery before they appear.
Never fabricate tool names or interpret a missing tool as proof the user has no account.

If the tools are callable, continue the requested app workflow. Do not create test
applications merely to check authentication.

## Authenticate

For an installed desktop plugin, use its connection/authentication controls. Let the
user complete sign-in and consent in their own browser. Do not request passwords,
tokens, machine secrets, or GitHub verification codes in chat.

For a standalone Codex CLI connection, the supported alternative is:

```sh
codex mcp add kinotic-os --url https://dev-api.kinotic.ai/mcp
codex mcp login kinotic-os --oauth-client-registration cimd
```

Run the add command only when the user wants this connection configured and a server
with that name is not already configured. This alternative is unnecessary when the
installed plugin already supplies a working connection. For custom environments,
replace the URL and use a distinct server name. `codex mcp list` inspects configured
standalone servers; `/mcp` in the Codex terminal UI shows active MCP servers.
Do not assume a plugin-scoped server is addressable as the standalone CLI name.

An existing Kinotic user signs in and approves consent. A new user follows
**Create an organization** on the portal login page, signs up through GitHub, chooses
an organization, then **Continue to GitHub** to install the Kinotic GitHub App.
The chosen GitHub account/organization is where Kinotic creates project repositories.
Invited users use their invitation instead of creating another organization.
Upstream signup ends at the Applications page and does not resume OAuth: start a
fresh connection authorization after signup and approve it. Honor denied consent.

After authorization, rediscover the tools. A fresh server may publish its tool catalog
after a short delay; retry a bounded number of times and report the remaining error.
Connections can be reviewed under **Account → Connected apps** in the Kinotic portal.

## OAuth compatibility for operators

The upstream server uses `kinotic.domain.oauth.allowedClientIds` and does not support
dynamic client registration. Its Claude allowlist does not establish Codex support.
The operator must allow the actual Codex client ID used by the authorization request.
Do not guess it or reuse the Claude client ID.

Codex CLI supports CIMD. When the server advertises issuer-bound authorization
responses, the shared metadata document is
`https://chatgpt.com/oauth/codex/client.json`. Otherwise the document is specific to
the endpoint: `https://chatgpt.com/oauth/codex/<callback_id>/client.json`.
Use the exact ID from the attempted authorization and allow it on the server.
The desktop connection may use a different identity: inspect its request independently.
Loopback redirects must accept variable ports while matching the registered host and
path. If OAuth is served through a different public host, configure
`kinotic.domain.oauth.issuerBaseUrl` to match the externally reachable issuer.

If CIMD is unavailable, an operator-provided pre-registered client may be configured
using the host's documented OAuth settings. Never invent a client ID, bypass consent,
disable authentication, or put a secret in the plugin package.

If authentication fails, report the endpoint, non-secret error, and whether discovery,
client registration, consent, or callback validation failed. Never print authorization
codes, tokens, or complete callback URLs containing codes.

Official reference: https://learn.chatgpt.com/docs/extend/mcp?surface=cli
App creation: [create-app](../create-app/SKILL.md).
