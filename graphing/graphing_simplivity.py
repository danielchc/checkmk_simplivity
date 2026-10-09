#!/usr/bin/env python3

from cmk.graphing.v1 import Title
from cmk.graphing.v1.graphs import Graph, MinimalRange
from cmk.graphing.v1.metrics import (
    Color,
    DecimalNotation,
    Metric,
    SINotation,
    TimeNotation,
    Unit,
)
from cmk.graphing.v1.perfometers import Closed, FocusRange, Open, Perfometer

metric_latency_reads = Metric(
    name="latency_reads",
    title=Title("Latency Reads"),
    unit=Unit(TimeNotation()),
    color=Color.GREEN,
)
metric_latency_writes = Metric(
    name="latency_writes",
    title=Title("Latency Writes"),
    unit=Unit(TimeNotation()),
    color=Color.ORANGE,
)

metric_throughput_reads = Metric(
    name="throughput_reads",
    title=Title("Throughput Reads"),
    unit=Unit(DecimalNotation("B/s")),
    color=Color.GREEN,
)
metric_throughput_writes = Metric(
    name="throughput_writes",
    title=Title("Throughput Writes"),
    unit=Unit(DecimalNotation("B/s")),
    color=Color.ORANGE,
)

metric_iops_reads = Metric(
    name="iops_reads",
    title=Title("IOPS Reads"),
    unit=Unit(DecimalNotation("")),
    color=Color.GREEN,
)
metric_iops_writes = Metric(
    name="iops_writes",
    title=Title("IOPS Writes"),
    unit=Unit(DecimalNotation("")),
    color=Color.ORANGE,
)

metric_used_capacity = Metric(
    name="used_capacity",
    title=Title("Used Capacity"),
    unit=Unit(SINotation("B")),
    color=Color.ORANGE,
)
metric_free_space = Metric(
    name="free_space",
    title=Title("Free Space"),
    unit=Unit(SINotation("B")),
    color=Color.GREEN,
)
metric_allocated_capacity = Metric(
    name="allocated_capacity",
    title=Title("Allocated Capacity"),
    unit=Unit(SINotation("B")),
    color=Color.BLUE,
)

metric_capacity_savings = Metric(
    name="capacity_savings",
    title=Title("Capacity Savings"),
    unit=Unit(SINotation("B")),
    color=Color.BLUE,
)

metric_compression_ratio = Metric(
    name="compression_ratio",
    title=Title("Compression Ratio"),
    unit=Unit(DecimalNotation("")),
    color=Color.BLUE,
)

metric_efficiency_ratio = Metric(
    name="efficiency_ratio",
    title=Title("Efficiency Ratio"),
    unit=Unit(DecimalNotation("")),
    color=Color.BLUE,
)

metric_deduplication_ratio = Metric(
    name="deduplication_ratio",
    title=Title("Deduplication Ratio"),
    unit=Unit(DecimalNotation("")),
    color=Color.BLUE,
)

metric_remote_backup_capacity = Metric(
    name="remote_backup_capacity",
    title=Title("Remote Backup Capacity"),
    unit=Unit(SINotation("B")),
    color=Color.BLUE,
)

metric_local_backup_capacity = Metric(
    name="local_backup_capacity",
    title=Title("Local Backup Capacity"),
    unit=Unit(SINotation("B")),
    color=Color.BLUE,
)

metric_stored_compressed_data = Metric(
    name="stored_compressed_data",
    title=Title("Stored Compressed Data"),
    unit=Unit(SINotation("B")),
    color=Color.BLUE,
)

metric_stored_uncompressed_data = Metric(
    name="stored_uncompressed_data",
    title=Title("Stored Uncompressed Data"),
    unit=Unit(SINotation("B")),
    color=Color.BLUE,
)

metric_stored_virtual_machine_data = Metric(
    name="stored_virtual_machine_data",
    title=Title("Stored Virtual Machine Data"),
    unit=Unit(SINotation("B")),
    color=Color.BLUE,
)

metric_used_logical_capacity = Metric(
    name="used_logical_capacity",
    title=Title("Used Logical Capacity"),
    unit=Unit(SINotation("B")),
    color=Color.ORANGE,
)


metric_used_percentage = Metric(
    name="used_percentage",
    title=Title("Used Capacity Percentage"),
    unit=Unit(DecimalNotation("%")),
    color=Color.ORANGE,
)

metric_safe_percentage = Metric(
    name="safe_percentage",
    title=Title("Safe VMs Percentage"),
    unit=Unit(DecimalNotation("%")),
    color=Color.GREEN,
)

metric_degraded_vms = Metric(
    name="degraded_vms",
    title=Title("Degraded VMs"),
    unit=Unit(DecimalNotation("")),
    color=Color.RED,
)

metric_unknown_vms = Metric(
    name="unknown_vms",
    title=Title("Unknown VMs"),
    unit=Unit(DecimalNotation("")),
    color=Color.PURPLE,
)

metric_syncing_vms = Metric(
    name="syncing_vms",
    title=Title("Syncing VMs"),
    unit=Unit(DecimalNotation("")),
    color=Color.YELLOW,
)

metric_safe_vms = Metric(
    name="safe_vms",
    title=Title("Safe VMs"),
    unit=Unit(DecimalNotation("")),
    color=Color.GREEN,
)
metric_total_vms = Metric(
    name="total_vms",
    title=Title("Total VMs"),
    unit=Unit(DecimalNotation("")),
    color=Color.BLUE,
)
