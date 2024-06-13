import json
import os
import pickle
from typing import Mapping, Optional, Sequence

import pytest

from oteltest import OtelTest, telemetry, Telemetry
from oteltest.private import (
    get_next_json_file,
    is_test_class,
    load_test_class_for_script,
    save_telemetry_json,
)


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


@pytest.fixture
def telemetry_fixture():
    with open(get_path_to_fixture("telemetry.pkl"), "rb") as file:
        return pickle.load(file)


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

        def on_stop(
            self, tel: Telemetry, stdout: str, stderr: str, returncode: int
        ) -> None:
            pass

    class MyOtelTest:
        pass

    assert not is_test_class(K)
    assert is_test_class(MyImpl)
    assert is_test_class(MyOtelTest)


def test_load_test_class_for_script():
    path = os.path.join(fixtures_dir, "script.py")
    klass = load_test_class_for_script("script", path)
    assert klass is not None


def test_telemetry_functions(telemetry_fixture: Telemetry):
    assert len(telemetry_fixture.trace_requests)
    assert len(telemetry_fixture.trace_requests)
    assert telemetry.num_spans(telemetry_fixture) == 10
    assert telemetry.num_metrics(telemetry_fixture) == 21
    assert telemetry.metric_names(telemetry_fixture) == {
        "system.thread_count",
        "process.runtime.cpython.gc_count",
        "system.disk.io",
        "system.network.errors",
        "system.network.dropped_packets",
        "system.disk.operations",
        "system.network.packets",
        "system.cpu.utilization",
        "system.swap.utilization",
        "system.memory.usage",
        "process.runtime.cpython.context_switches",
        "process.runtime.cpython.cpu_time",
        "process.runtime.cpython.cpu.utilization",
        "system.network.io",
        "system.memory.utilization",
        "loop-counter",
        "process.runtime.cpython.thread_count",
        "system.swap.usage",
        "system.disk.time",
        "system.cpu.time",
        "process.runtime.cpython.memory",
    }
    request = telemetry_fixture.trace_requests[0]
    span = request.pbreq.resource_spans[0].scope_spans[0].spans[0]
    assert span.trace_id.hex() == "0adffbc2cb9f3cdb09f6801a788da973"


# utils

fixtures_dir = os.path.join(os.path.dirname(__file__), "fixtures")


def get_path_to_fixture(fname):
    return os.path.join(fixtures_dir, fname)


def telemetry_from_json(json_str: str) -> telemetry.Telemetry:
    return telemetry_from_dict(json.loads(json_str))


def telemetry_from_dict(d) -> telemetry.Telemetry:
    return telemetry.Telemetry(
        log_requests=d["log_requests"],
        metric_requests=d["metric_requests"],
        trace_requests=d["trace_requests"],
    )
