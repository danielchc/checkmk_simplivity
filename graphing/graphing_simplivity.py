#!/usr/bin/env python3

from cmk.graphing.v1 import Title
from cmk.graphing.v1.graphs import Graph, MinimalRange
from cmk.graphing.v1.metrics import Color, DecimalNotation, Metric, Unit,TimeNotation
from cmk.graphing.v1.perfometers import Closed, FocusRange, Open, Perfometer


metric_latency_reads = Metric(
    name = "latency_reads",
    title = Title("Latency Reads"),
    unit = Unit(DecimalNotation("μs")),
    color = Color.GREEN,
)
metric_latency_writes = Metric(
    name = "latency_writes",
    title = Title("Latency Writes"),
    unit = Unit(DecimalNotation("μs")),
    color = Color.ORANGE,
)

metric_throughput_reads = Metric(
    name = "throughput_reads",
    title = Title("Throughput Reads"),
    unit = Unit(DecimalNotation("B/s")),
    color = Color.GREEN,
)
metric_throughput_writes = Metric(
    name = "throughput_writes",
    title = Title("Throughput Writes"),
    unit = Unit(DecimalNotation("B/s")),
    color = Color.ORANGE,
)

metric_iops_reads = Metric(
    name = "iops_reads",
    title = Title("IOPS Reads"),
    unit = Unit(DecimalNotation("")),
    color = Color.GREEN,
)
metric_iops_writes = Metric(
    name = "iops_writes",
    title = Title("IOPS Writes"),
    unit = Unit(DecimalNotation("")),
    color = Color.ORANGE,
)