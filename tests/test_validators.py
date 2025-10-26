import random
import pydantic
import pytest
import tum_esm_utils.files
from tum_esm_utils.validators import StrictFilePath, StrictDirectoryPath, Version, StrictIPv4Adress


@pytest.mark.order(3)
@pytest.mark.quick
def test_strict_path_validators() -> None:
    class Config(pydantic.BaseModel):
        f: StrictFilePath
        d: StrictDirectoryPath

    test_file = tum_esm_utils.files.rel_to_abs_path("../pyproject.toml")
    test_dir = tum_esm_utils.files.rel_to_abs_path("..")

    c = Config(f=test_file, d=test_dir) # pyright: ignore[reportArgumentType]
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


@pytest.mark.order(3)
@pytest.mark.quick
def test_version_validator() -> None:
    for valid_string in [
        "0.0.0",
        "1.2.3",
        "1.2.3-alpha.1",
        "1.2.3-alpha.30",
        "1.2.3-beta.2",
        "1.2.3-rc.70",
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


@pytest.mark.order(3)
@pytest.mark.quick
def test_ipv4_validator() -> None:
    # validate bunch of valid IPv4 addresses
    for _ in range(10):
        random_port = random.randint(0, 65535)
        for valid_string in [
            "192.168.1.1",
            "10.0.0.1",
            "172.16.0.1",
            "8.8.8.8",
            "1.1.1.1",
            "123.45.67.89",
            "255.255.255.255",
            "0.0.0.0",
            "192.0.2.1",
            "198.51.100.1",
            "203.0.113.1",
            "192.168.0.100",
            "10.10.10.10",
            "172.31.255.249",
            "169.254.0.1",
        ]:
            StrictIPv4Adress(f"{valid_string}")
            StrictIPv4Adress(f"{valid_string}:{random_port}")

    # validate bunch of invalid IPv4 addresses
    for invalid_string in [
        "192.168.1.256",  # Octet out of range
        "10.0.0.999",  # Octet out of range
        "172.16.0.256",  # Octet out of range
        "8.8.8.8.8",  # Too many octets
        "1.1.1",  # Too few octets
        "123.45.67.89.0",  # Too many octets
        "255.255.255.256",  # Octet out of range
        "0.0.0.0.0",  # Too many octets
        "192.0.2",  # Too few octets
        "198.51.100.256",  # Octet out of range
        "203.0.113.999",  # Octet out of range
        "192.168.0.1000",  # Octet out of range
        "10.10.10.10.10",  # Too many octets
        "172.31.255.256",  # Octet out of range
        "169.254.0.256",  # Octet out of range
        "abc.def.ghi.jkl",  # Non-numeric octets
        "123.456.78.90",  # Octet out of range
        "192.168.1.-1",  # Negative octet
        "192.168.1.1.",  # Trailing dot
        ".192.168.1.1",  # Leading dot
        "192.168..1.1",  # Double dot
        "192.168.1.1:999999",  # Port out of range
    ]:
        try:
            StrictIPv4Adress(invalid_string)
        except pydantic.ValidationError:
            pass
        else:
            raise AssertionError(
                f"ValidationError not raised for invalid IPv4 address '{invalid_string}'"
            )
