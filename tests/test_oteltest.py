import json
import os
import pathlib
from typing import Optional, Sequence, Mapping

import pytest
from oteltest import telemetry, OtelTest, Telemetry
from oteltest.private import get_next_json_file, save_telemetry_json, is_test_class, setup_script_environment, \
    load_test_class_for_script


@pytest.fixture
def metric_telemetry():
    return load_json("metric")


@pytest.fixture
def trace_telemetry():
    return load_json("trace")


def load_json(fname):
    fixtures_dir = pathlib.Path(__file__).parent / "fixtures"
    file_path = fixtures_dir / f"{fname}.json"
    with file_path.open("r") as file:
        return json.load(file)


def test_get_next_json_file(tmp_path):
    module_name = "my_module_name"
    path_to_dir = str(tmp_path)

    next_file = get_next_json_file(path_to_dir, module_name)
    assert "my_module_name.0.json" == next_file

    save_telemetry_json(path_to_dir, next_file, "")

    next_file = get_next_json_file(path_to_dir, module_name)
    assert "my_module_name.1.json" == next_file

    save_telemetry_json(path_to_dir, next_file, "[1]")

    next_file = get_next_json_file(path_to_dir, module_name)
    assert "my_module_name.2.json" == next_file


def test_telemetry_metric_operations(metric_telemetry):
    tel = telemetry.Telemetry()

    tel.add_metric(metric_telemetry, {}, 1)
    assert {"my-metric-name"} == telemetry.metric_names(tel)
    assert 1 == telemetry.num_metrics(tel)

    tel.add_metric(metric_telemetry, {}, 1)
    assert 2 == telemetry.num_metrics(tel)
    assert {"my-metric-name"} == telemetry.metric_names(tel)


def test_telemetry_trace_operations(trace_telemetry):
    tel = telemetry.Telemetry()
    tel.add_trace(trace_telemetry, {}, 1)
    assert 1 == telemetry.num_spans(tel)
    header_key = "my-trace-header"
    header_val = "my-trace-header-value"
    tel.add_trace(trace_telemetry, {header_key: header_val}, 1)
    assert 2 == telemetry.num_spans(tel)
    assert telemetry.has_trace_header(tel, header_key, header_val)
    assert {"/"} == telemetry.span_names(tel)


def test_is_test_class():
    class K:
        pass

    class MyImpl(OtelTest):
        def environment_variables(self) -> Mapping[str, str]:
            pass

        def requirements(self) -> Sequence[str]:
            pass

        def wrapper_command(self) -> str:
            pass

        def on_start(self) -> Optional[float]:
            pass

        def on_stop(self, tel: Telemetry, stdout: str, stderr: str, returncode: int) -> None:
            pass

    class MyOtelTest:
        pass

    assert not is_test_class(K)
    assert is_test_class(MyImpl)
    assert is_test_class(MyOtelTest)


def test_load_test_class_for_script():
    current_dir = os.path.dirname(__file__)
    path = os.path.join(current_dir, "fixtures", "script.py")
    klass = load_test_class_for_script("script", path)
    assert klass is not None


################################################################################################

def telemetry_from_json(json_str: str) -> telemetry.Telemetry:
    return telemetry_from_dict(json.loads(json_str))


def telemetry_from_dict(d) -> telemetry.Telemetry:
    return telemetry.Telemetry(
        log_requests=d["log_requests"],
        metric_requests=d["metric_requests"],
        trace_requests=d["trace_requests"],
    )
