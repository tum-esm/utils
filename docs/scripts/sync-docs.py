from __future__ import annotations
import ast
import os
import shutil
import subprocess
import tempfile

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INDEX_SRC = os.path.join(PROJECT_DIR, "README.md")
INDEX_DST = os.path.join(PROJECT_DIR, "docs", "pages", "index.md")
EXAMPLE_USAGE_SRC = os.path.join(PROJECT_DIR, "docs", "pages", "example-usage.md")
API_DST = os.path.join(PROJECT_DIR, "docs", "pages", "api-reference.md")
AGENTIC_DOCS_DIR = os.path.join(PROJECT_DIR, "docs", "agentic")
AGENTIC_MODULES_DIR = os.path.join(AGENTIC_DOCS_DIR, "modules")
AGENTIC_EXAMPLE_USAGE_DST = os.path.join(AGENTIC_DOCS_DIR, "example-usage.md")
AGENTS_DST = os.path.join(AGENTIC_DOCS_DIR, "AGENTS.md")

# copy index file to docs folder

with open(INDEX_SRC, "r") as f:
    index_file_content = f.read()

with open(INDEX_DST, "w") as f:
    f.write(index_file_content)

# generate automatic API reference and prettify output

module_names = [
    "code",
    "column",
    "column.astronomy",
    "column.averaging_kernel",
    "column.ncep_profiles",
    "dataframes",
    "datastructures",
    "decorators",
    "em27",
    "files",
    "mathematics",
    "netcdf",
    "opus",
    "opus.file_interface",
    "opus.http_interface",
    "plotting",
    "processes",
    "rebinning",
    "shell",
    "sqlitelock",
    "system",
    "text",
    "timing",
    "validators",
]
print("Module names:", module_names)


def get_pydoc_markdown_command() -> str:
    pydoc_markdown_command = shutil.which("pydoc-markdown")
    if pydoc_markdown_command is not None:
        return pydoc_markdown_command

    local_pydoc_markdown_commands = [
        os.path.join(PROJECT_DIR, ".venv", "bin", "pydoc-markdown"),
        os.path.join(PROJECT_DIR, ".venv", "Scripts", "pydoc-markdown.exe"),
    ]
    for local_pydoc_markdown_command in local_pydoc_markdown_commands:
        if os.path.exists(local_pydoc_markdown_command):
            return local_pydoc_markdown_command

    raise FileNotFoundError("Could not find pydoc-markdown on PATH or in the local .venv")


def load_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def get_module_source_path(module_name: str) -> str:
    module_path = module_name.replace(".", os.sep)
    package_init_path = os.path.join(PROJECT_DIR, "tum_esm_utils", module_path, "__init__.py")
    if os.path.exists(package_init_path):
        return package_init_path
    return os.path.join(PROJECT_DIR, "tum_esm_utils", module_path + ".py")


def get_module_docstring(module_name: str) -> str:
    module_source_path = get_module_source_path(module_name)
    with open(module_source_path, "r") as f:
        module = ast.parse(f.read(), filename=module_source_path)
    return ast.get_docstring(module) or "No module docstring available."


def parse_api_reference_content(raw_api_reference_content: str) -> str:
    parsed_api_reference_content_lines: list[str] = []
    for line in raw_api_reference_content.split("\n"):
        if line.startswith('<a id="'):
            continue
        if line.startswith("#"):
            line_segments = line.split(" ")
            assert line_segments[0] == "#" * len(line_segments[0])
            if len(line_segments) == 2:
                parsed_api_reference_content_lines.append(
                    line_segments[0] + "# `" + line_segments[1].replace("\\_", "_") + "`"
                )
            elif len(line_segments) == 3:
                assert line_segments[2] == "Objects"
                parsed_api_reference_content_lines.append(
                    line_segments[0] + "# `" + line_segments[1].replace("\\_", "_") + "` Objects"
                )
            else:
                raise ValueError("Unexpected line format: " + line)
        else:
            parsed_api_reference_content_lines.append(line)

    return "\n".join(parsed_api_reference_content_lines[2:])


def generate_api_reference_content(module_import_paths: list[str]) -> str:
    parsed_modules = [f"--module={module_import_path}" for module_import_path in module_import_paths]
    with tempfile.NamedTemporaryFile() as f:
        with open(f.name, "w") as stdout:
            subprocess.run(
                [get_pydoc_markdown_command(), *parsed_modules],
                cwd=PROJECT_DIR,
                stdout=stdout,
                check=True,
            )
        raw_api_reference_content = load_file(f.name)
    return parse_api_reference_content(raw_api_reference_content)


def write_agentic_docs() -> None:
    os.makedirs(AGENTIC_MODULES_DIR, exist_ok=True)

    write_file(AGENTIC_EXAMPLE_USAGE_DST, load_file(EXAMPLE_USAGE_SRC))

    for module_name in module_names:
        module_import_path = f"tum_esm_utils.{module_name}"
        module_api_reference_content = generate_api_reference_content([module_import_path])
        module_api_reference_path = os.path.join(AGENTIC_MODULES_DIR, f"{module_name}.md")
        write_file(
            module_api_reference_path,
            f"# `{module_import_path}` API Reference\n\n{module_api_reference_content}",
        )

    module_summary_lines: list[str] = []
    for module_name in module_names:
        module_import_path = f"tum_esm_utils.{module_name}"
        module_api_reference_filename = f"modules/{module_name}.md"
        module_docstring = get_module_docstring(module_name)
        module_summary_lines.append(
            f"## `{module_import_path}`\n\n"
            f"API reference: [{module_api_reference_filename}]({module_api_reference_filename})\n\n"
            f"{module_docstring}\n"
        )

    write_file(
        AGENTS_DST,
        "# TUM ESM Utils Agent Guide\n\n"
        "## Purpose\n\n"
        "This library is a collection of small Python utilities used in research projects "
        "by the Professorship of Environmental Sensing and Modeling at the Technical "
        "University of Munich. It centralizes reusable helpers so downstream projects can "
        "depend on tested, documented primitives instead of carrying local utility copies.\n\n"
        "## Documentation Structure\n\n"
        "- `example-usage.md` contains the same examples as the human-facing documentation page.\n"
        "- `modules/` contains one API reference file per documented submodule. File names "
        "match Python import paths below `tum_esm_utils`, for example "
        "`modules/column.astronomy.md` documents `tum_esm_utils.column.astronomy`.\n"
        "- This `AGENTS.md` file lists the documented modules and their module docstrings so "
        "agents can choose the narrowest API file before reading detailed references.\n\n"
        "## Modules\n\n"
        + "\n".join(module_summary_lines),
    )


with open(API_DST, "w") as f:
    f.write(
        "# API Reference \n\n"
        + generate_api_reference_content(
            ["tum_esm_utils", *[f"tum_esm_utils.{module_name}" for module_name in module_names]]
        )
    )


write_agentic_docs()
