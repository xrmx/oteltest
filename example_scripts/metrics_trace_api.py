from typing import Mapping, Optional, Sequence

from oteltest import OtelTest, Telemetry


def print_time(iterations):
    import time
    from opentelemetry import metrics, trace

    meter = metrics.get_meter("time-printer", "1.0")
    counter = meter.create_counter("loop-counter", unit="1", description="my desc")
    tracer = trace.get_tracer("my.tracer.name")
    for i in range(iterations):
        time.sleep(1)
        counter.add(1)
        with tracer.start_as_current_span("my-span"):
            print(f"{i + 1}/{iterations} current time: {round(time.time())}")


class MyTest(OtelTest):

    def environment_variables(self) -> Mapping[str, str]:
        return {}

    def requirements(self) -> Sequence[str]:
        return ("splunk-opentelemetry[all]",)

    def wrapper_command(self) -> str:
        return "opentelemetry-instrument"

    def on_start(self) -> Optional[float]:
        print("started")
        return None

    def on_stop(
        self, tel: Telemetry, stdout: str, stderr: str, returncode: int
    ) -> None:
        print(f"stopped: {stdout}")
        print(f"telemetry: {tel}")


if __name__ == "__main__":
    print_time(10)
