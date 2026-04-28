import yaml
from pathlib import Path
from typing import Any


def define_env(env):
    flag_admonitions = {
        "experimental": {"type": "example", "title": "Experimental"},
        "dev-only": {"type": "warning", "title": "For development environments only"},
    }
    data_path = (
        Path(env.project_dir) / "docs" / "includes" / "environment_variables.yaml"
    )

    env_vars: list[dict[str, Any]] = yaml.safe_load(
        data_path.read_text(encoding="utf-8")
    )
    vars_by_name = {var["name"]: var for var in env_vars}

    def get_yaml_list(value: Any) -> list:
        if value is None:
            return []
        return value if isinstance(value, list) else [value]

    def as_heading(value: str) -> str:
        return f"### {value}"

    def as_inline_code(value: Any) -> str:
        if value == "":
            return '`""`'
        return f"`{value}`"

    def as_admonition(admonition_type: str, title: str) -> str:
        return f'!!! {admonition_type} "{title}"'

    @env.macro
    def define_env_var(name: str) -> str:
        """Generate a reference section for a single environment variable as markdown."""
        var = vars_by_name.get(name)

        var_reference_lines = []
        var_reference_lines.append(as_heading(var["name"]))

        for flag in get_yaml_list(var.get("flags")):
            flag_admonition = flag_admonitions.get(flag)
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
    def define_all_env_vars() -> str:
        """Generate a reference section for all available environment variables as markdown."""
        reference_lines = []
        for var in env_vars:
            reference_lines.append(define_env_var(var["name"]))
        return "\n".join(reference_lines)
