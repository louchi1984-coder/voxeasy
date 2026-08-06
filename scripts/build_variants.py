#!/usr/bin/env python3
"""Build installable VoxEasy variants from one public core and JSON profiles."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
COPY_FILES = ("SKILL.md",)
COPY_DIRS = ("agents", "archive", "evals", "references", "scripts")
REQUIRED_KEYS = {
    "id",
    "skill_name",
    "display_name",
    "version",
    "description",
    "short_description",
    "default_prompt",
    "allow_implicit_invocation",
    "positioning",
    "default_model",
    "default_ratio",
    "default_style",
    "allowed_styles",
    "narrative_preference",
    "visual_priorities",
    "constraints",
}


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def load_profile(path: Path) -> dict:
    profile = json.loads(path.read_text(encoding="utf-8"))
    missing = sorted(REQUIRED_KEYS - profile.keys())
    if missing:
        raise ValueError(f"{path}: missing keys: {', '.join(missing)}")
    if not re.fullmatch(r"[a-z0-9-]{1,63}", profile["skill_name"]):
        raise ValueError(f"{path}: invalid skill_name {profile['skill_name']!r}")
    if profile["default_style"] not in profile["allowed_styles"]:
        raise ValueError(f"{path}: default_style must be present in allowed_styles")
    if not isinstance(profile["allow_implicit_invocation"], bool):
        raise ValueError(f"{path}: allow_implicit_invocation must be boolean")
    return profile


def render_variant_profile(profile: dict) -> str:
    styles = "、".join(f"`{item}`" for item in profile["allowed_styles"])
    priorities = "\n".join(f"- {item}" for item in profile["visual_priorities"])
    constraints = "\n".join(f"- {item}" for item in profile["constraints"])
    invocation = "允许自动触发" if profile["allow_implicit_invocation"] else f"仅手动调用 `${profile['skill_name']}`"
    return f"""# {profile['display_name']} Profile

- 版本：`{profile['version']}`
- 调用：{invocation}
- 定位：{profile['positioning']}
- 推荐模型：`{profile['default_model']}`
- 推荐比例：`{profile['default_ratio']}`
- 推荐风格：`{profile['default_style']}`
- 可选风格：{styles}
- 叙事偏好：{profile['narrative_preference']}

## 视觉优先级

{priorities}

## 定制约束

{constraints}

Profile 只设置版本边界和推荐值，不得跳过两次确认、时间轴验证、文字白名单或用户明确选择。用户要求不在可选风格内的风格时，建议改用 `$voxeasy` 或 `$voxeasy-lab`，不得静默越界。
"""


def render_openai_yaml(profile: dict) -> str:
    implicit = "true" if profile["allow_implicit_invocation"] else "false"
    return f"""interface:
  display_name: {yaml_string(profile['display_name'])}
  short_description: {yaml_string(profile['short_description'])}
  default_prompt: {yaml_string(profile['default_prompt'])}

policy:
  allow_implicit_invocation: {implicit}
"""


def render_interface_yaml(profile: dict) -> str:
    activation = "implicit-or-manual" if profile["allow_implicit_invocation"] else "manual"
    degradation = "native-skill" if profile["allow_implicit_invocation"] else "manual-skill"
    return f"""interface:
  display_name: {yaml_string(profile['display_name'])}
  short_description: {yaml_string(profile['short_description'])}
  default_prompt: {yaml_string(profile['default_prompt'])}
compatibility:
  canonical_format: "agent-skills"
  adapter_targets:
    - "openai"
    - "claude"
    - "generic"
  activation:
    mode: "{activation}"
    paths: []
  execution:
    context: "inline"
    shell: "bash"
  trust:
    source_tier: "local"
    remote_inline_execution: "forbid"
    remote_metadata_policy: "allow-metadata-only"
  degradation:
    openai: "{degradation}"
    claude: "agent-skills-source"
    generic: "neutral-source"
"""


def rewrite_skill(path: Path, profile: dict) -> None:
    text = path.read_text(encoding="utf-8")
    text, name_count = re.subn(r"(?m)^name: .+$", f"name: {profile['skill_name']}", text, count=1)
    text, description_count = re.subn(
        r"(?m)^description: .+$",
        f"description: {profile['description']}",
        text,
        count=1,
    )
    text, heading_count = re.subn(
        r"(?m)^# VoxEasy.*$",
        f"# {profile['display_name']} {profile['version']}",
        text,
        count=1,
    )
    if (name_count, description_count, heading_count) != (1, 1, 1):
        raise ValueError("SKILL.md does not match the expected VoxEasy template")
    path.write_text(text, encoding="utf-8")


def build(profile_path: Path, output_root: Path, replace: bool) -> Path:
    profile = load_profile(profile_path)
    output_root = output_root.resolve()
    target = output_root / profile["skill_name"]
    output_root.mkdir(parents=True, exist_ok=True)

    if target.exists():
        if not replace:
            raise FileExistsError(f"{target} already exists; pass --replace to rebuild it")
        if target.parent != output_root or target.name != profile["skill_name"]:
            raise ValueError(f"refusing unsafe replacement target: {target}")
        shutil.rmtree(target)

    target.mkdir()
    for filename in COPY_FILES:
        shutil.copy2(ROOT / filename, target / filename)
    for dirname in COPY_DIRS:
        source = ROOT / dirname
        if source.exists():
            shutil.copytree(source, target / dirname)

    factory_script = target / "scripts" / "build_variants.py"
    if factory_script.exists():
        factory_script.unlink()

    rewrite_skill(target / "SKILL.md", profile)
    (target / "references" / "variant-profile.md").write_text(
        render_variant_profile(profile), encoding="utf-8"
    )
    (target / "agents" / "openai.yaml").write_text(render_openai_yaml(profile), encoding="utf-8")
    (target / "agents" / "interface.yaml").write_text(render_interface_yaml(profile), encoding="utf-8")
    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--profile", action="append", type=Path, help="Profile JSON; may be repeated")
    group.add_argument("--all", action="store_true", help="Build every committed profile")
    parser.add_argument("--output-root", type=Path, default=ROOT / "dist")
    parser.add_argument("--replace", action="store_true", help="Replace matching outputs inside output-root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    profile_paths = sorted((ROOT / "profiles").glob("*.json")) if args.all else args.profile
    try:
        outputs = [build(path.resolve(), args.output_root, args.replace) for path in profile_paths]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
