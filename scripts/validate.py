"""Validate the distributable package without network calls or credentials."""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
catalog = json.loads((root / '.agents/plugins/marketplace.json').read_text())
entry, = catalog['plugins']
assert entry['policy']['authentication'] == 'ON_INSTALL'
assert entry['source']['path'].startswith('./')
plugin = (root / entry['source']['path']).resolve()
assert plugin.is_relative_to(root)
manifest = json.loads((plugin / '.codex-plugin/plugin.json').read_text())
assert manifest['name'] == entry['name']
assert re.fullmatch(r'\d+\.\d+\.\d+', manifest['version'])
assert manifest['author']['name']
for key in ('skills', 'mcpServers'):
    value = manifest[key]
    assert value.startswith('./') and '..' not in Path(value).parts
    assert (plugin / value).exists(), value
onboarding = plugin / manifest['extensions']['com.openai']['onboardingSkill']
assert onboarding.is_file()
servers = json.loads((plugin / manifest['mcpServers']).read_text())['mcpServers']
assert servers['kinotic-os']['type'] == 'http'
assert servers['kinotic-os']['url'] == 'https://dev-api.kinotic.ai/mcp'
names = set()
for skill in sorted((plugin / 'skills').glob('*/SKILL.md')):
    text = skill.read_text()
    assert text.startswith('---\n')
    frontmatter = text.split('---', 2)[1]
    name = re.search(r'^name:\s*(\S+)', frontmatter, re.M).group(1)
    assert name == skill.parent.name and name not in names
    assert re.search(r'^description:\s*\S', frontmatter, re.M)
    assert len(frontmatter.split('description:', 1)[1]) < 1024
    names.add(name)
    assert 'claude mcp' not in text and 'Claude Code' not in text
assert names == {'setup', 'new-app', 'create-app', 'entities-and-persistence',
                 'services', 'frontend', 'deploying'}
for document in (plugin / 'skills').rglob('*.md'):
    text = document.read_text()
    targets = re.findall(r'\]\(([^)]+\.md)\)', text)
    targets += re.findall(r'`(references/[^`]+\.md)`', text)
    for target in targets:
        resolved = (document.parent / target).resolve()
        assert resolved.is_relative_to(plugin) and resolved.is_file(), (document, target)
assert (plugin / 'LICENSE').is_file() and (plugin / 'NOTICE').is_file()
print(f'PASS: marketplace, manifest, HTTP MCP wiring, {len(names)} skills, references, license')
