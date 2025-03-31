from __future__ import annotations
import os
import tempfile

import tum_esm_utils

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INDEX_SRC = os.path.join(PROJECT_DIR, "README.md")
INDEX_DST = os.path.join(PROJECT_DIR, "docs", "pages", "index.md")
API_DST = os.path.join(PROJECT_DIR, "docs", "pages", "api-reference.md")

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
    "datastructures",
    "decorators",
    "em27",
    "files",
    "mathematics",
    "opus",
    "opus.file_interface",
    "opus.http_interface",
    "plotting",
    "processes",
    "shell",
    "system",
    "text",
    "timing",
    "validators",
]
print("Module names:", module_names)

parsed_modules = ["--module=tum_esm_utils"]
for m in module_names:
    parsed_modules.append(f"--module=tum_esm_utils.{m}")

with tempfile.NamedTemporaryFile() as f:
    command = f"pydoc-markdown " + (" ").join(parsed_modules)
    os.system(f"cd {PROJECT_DIR} && {command} > {f.name}")
    raw_api_reference_content = tum_esm_utils.files.load_file(f.name)

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

    parsed_api_reference_content = "\n".join(parsed_api_reference_content_lines[2:])

with open(API_DST, "w") as f:
    f.write("# API Reference \n\n" + parsed_api_reference_content)
