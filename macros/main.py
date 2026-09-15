import yaml
from pathlib import Path
from typing import Any
from collections import defaultdict

FLAG_ADMONITIONS = {
    "experimental": {"type": "example", "title": "Experimental"},
    "dev-only": {"type": "warning", "title": "For development environments only"},
}
INI_SECTION_MD_HEADINGS = {
    "service:graph": "Graph store",
    "service:node-api": "Node API",
    "service:federation-api": "Federation API",
    "service:query": "Query tool",
    "service:experimental": "Experimental settings",
    "compose": "Docker Compose configuration",
}


def define_env(env):
    data_path = (
        Path(env.project_dir) / "docs" / "includes" / "environment_variables.yaml"
    )
    env_vars: list[dict[str, Any]] = yaml.safe_load(
        data_path.read_text(encoding="utf-8")
    )
    vars_by_name = {var["name"]: var for var in env_vars}
    vars_by_ini_section = defaultdict(list)
    for var in env_vars:
        vars_by_ini_section[var["ini_section"]].append(var)

    def get_yaml_list(value: Any) -> list:
        if value is None:
            return []
        return value if isinstance(value, list) else [value]

    def as_section_heading(value: str) -> str:
        return f"## {value}"

    def as_variable_heading(value: str) -> str:
        return f"### {value}"

    def as_inline_code(value: Any) -> str:
        if value == "":
            return '`""`'
        return f"`{value}`"

    def as_admonition(admonition_type: str, title: str) -> str:
        return f'!!! {admonition_type} "{title}"'

    @env.macro
    def create_env_reference_section(name: str) -> str:
        """Generate a reference section for a single environment variable as markdown."""
        var = vars_by_name.get(name)

        var_reference_lines = []
        var_reference_lines.append(as_variable_heading(var["name"]))

        for flag in get_yaml_list(var.get("flags")):
            flag_admonition = FLAG_ADMONITIONS.get(flag)
            if flag_admonition:
                var_reference_lines.append(
                    f"{as_admonition(flag_admonition['type'], flag_admonition['title'])}"
                )
        if "default" in var:
            var_reference_lines.append(f"**Default:** {as_inline_code(var['default'])}")
        var_reference_lines.append(
            f"**Configuration INI section:** {as_inline_code(var['ini_section'])}"
        )
        var_reference_lines.append(
            f"**Deployment profiles:** {', '.join([as_inline_code(profile) for profile in var['deployment_profiles']])}"
        )
        var_reference_lines.append(f"**Description:** {var['description']}")

        return "  \n".join(var_reference_lines)

    @env.macro
    def create_env_var_reference() -> str:
        """Generate the full reference markdown for all available environment variables."""
        reference_lines = []

        for ini_section, section_md_heading in INI_SECTION_MD_HEADINGS.items():
            section_vars = vars_by_ini_section[ini_section]
            reference_lines.append(as_section_heading(section_md_heading))
            for var in section_vars:
                reference_lines.append(create_env_reference_section(var["name"]))

        return "\n".join(reference_lines)
