from typing import Mapping, Optional, Sequence


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


# We have the option to not inherit from the OtelTest base class, in which case we name our class so it contains
# "OtelTest". This has the benefit of not requiring a dependency on oteltest in the script's environment.
class MyOtelTest:

    def environment_variables(self) -> Mapping[str, str]:
        return {}

    def requirements(self) -> Sequence[str]:
        return ("splunk-opentelemetry[all]",)

    def wrapper_command(self) -> str:
        # return "opentelemetry-instrument"
        return "splunk-py-trace"

    def on_start(self) -> Optional[float]:
        print("started")
        return None

    def on_stop(self, tel, stdout: str, stderr: str, returncode: int) -> None:
        print(f"stopped: {stdout}")
        print(f"telemetry: {tel}")


if __name__ == "__main__":
    print_time(10)
