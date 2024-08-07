import pydantic
import tum_esm_utils
from tum_esm_utils.validators import StrictFilePath, StrictDirectoryPath, Version


def test_strict_path_validators() -> None:
    class Config(pydantic.BaseModel):
        f: StrictFilePath
        d: StrictDirectoryPath

    test_file = tum_esm_utils.files.rel_to_abs_path("../pyproject.toml")
    test_dir = tum_esm_utils.files.rel_to_abs_path("..")

    c = Config(f=test_file, d=test_dir)
    assert isinstance(c.f, StrictFilePath)
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


def test_version_validator() -> None:
    for valid_string in [
        "0.0.0", "1.2.3", "1.2.3-alpha.1", "1.2.3-alpha.30", "1.2.3-beta.2",
        "1.2.3-rc.70"
    ]:
        v = Version(valid_string)
        assert v.as_identifier() == valid_string
        assert v.as_tag() == f"v{valid_string}"

    for invalid_string in [
        "0.0",
        "1.2.3-alpha",
        "1.2.3-alpha.1.2",
        "1.2.3-beta.2.3",
        "1.2.3-rc.70.1",
        "1",
        "-1.1.0",
        "1.1.0-",
        "1.1.0-alpha-",
        "1.1.0-beta.",
        "1.1.0-rc",
    ]:
        try:
            v = Version(invalid_string)
        except pydantic.ValidationError:
            pass
        else:
            raise AssertionError(
                f"ValidationError not raised for invalid version string '{invalid_string}'"
            )

    assert Version("1.2.3-alpha.1") > Version("1.2.3-alpha.0")
    assert Version("1.2.3-alpha.1") < Version("1.2.3-alpha.2")
    assert Version("1.2.3-alpha.1") == Version("1.2.3-alpha.1")
    assert Version("1.2.3-alpha.1") != Version("1.2.3-alpha.2")
    assert Version("1.2.3") > Version("1.2.2")
    assert Version("1.2.3") < Version("1.2.4")
    assert Version("10.2.3") > Version("1.2.3")
    assert Version("10.6.9") < Version("10.7.8")
    assert Version("10.6.9-alpha.1") > Version("10.6.8-beta.3")
    assert Version("10.6.9-alpha.4") < Version("10.6.9-beta.3")
    assert Version("10.6.9-alpha.4") < Version("10.6.9-rc.3")
    assert Version("10.6.9-rc.4") > Version("10.6.9-beta.3")
    assert Version("10.6.9-rc.4") < Version("10.6.9-rc.5")
