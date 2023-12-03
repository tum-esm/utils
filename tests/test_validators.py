import pydantic
import tum_esm_utils


def test_strict_path_validators() -> None:
    class Config(pydantic.BaseModel):
        f: tum_esm_utils.validators.StrictFilePath
        d: tum_esm_utils.validators.StrictDirectoryPath

    test_file = tum_esm_utils.files.rel_to_abs_path("../pyproject.toml")
    test_dir = tum_esm_utils.files.rel_to_abs_path("..")

    c = Config(f=test_file, d=test_dir)
    assert isinstance(c.f, tum_esm_utils.validators.StrictFilePath)
    assert isinstance(c.f.root, str)
    assert set(c.model_dump().keys()) == {"f", "d"}

    try:
        c = Config.model_validate({"f": "someinvalidfile", "d": test_dir})
    except pydantic.ValidationError:
        pass
    else:
        raise AssertionError("ValidationError not raised")

    try:
        c = Config.model_validate({"f": test_file, "d": "someinvaliddir"})
    except pydantic.ValidationError:
        pass
    else:
        raise AssertionError("ValidationError not raised")

    # you can turn off the file path validation at construction time if you want
    c = Config.model_validate(
        {"f": "someinvalidfile", "d": "someinvaliddir"},
        context={"ignore-path-existence": True},
    )
