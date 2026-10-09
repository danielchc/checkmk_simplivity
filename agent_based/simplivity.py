#!/usr/bin/env python3
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    Result,
    State,
    Metric,
    check_levels,
)
from cmk.agent_based.v2 import render

import itertools
import json


def parse_json(string_table):
    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", '"'))
    return parsed


def discover(section):
    yield Service()


def discover_cluster(section):
    for cluster in section["clusters"].keys():
        yield Service(item=section["clusters"][cluster]["name"])


def discover_hosts(section):
    for cluster in section["hosts"].keys():
        yield Service(item=section["hosts"][cluster]["name"])


### CLUSTER ###


def get_status(section):
    if section:
        yield Result(state=State.OK, summary="OK")
    else:
        yield Result(state=State.CRIT, summary=f"Unable to get data")


def get_cluster_id(item, section):
    try:
        yield Result(state=State.OK, summary=section["clusters"][item]["cluster_id"])
    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_cluster_version(item, section):
    try:
        yield Result(state=State.OK, summary=section["clusters"][item]["version"])
    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_cluster_iops(item, section):
    try:
        value = section["clusters"][item]["metrics"]["iops"]

        yield from check_levels(value["reads"], label="Reads", metric_name="iops_reads")
        yield from check_levels(
            value["writes"],
            label="Writes",
            metric_name="iops_writes",
        )

    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_cluster_latency(item, params, section):
    try:
        threshold_latency_reads = params["latency_reads"]
        threshold_latency_writes = params["latency_writes"]
        value = section["clusters"][item]["metrics"]["latency"]
        yield from check_levels(
            value["reads"] / 1e6,
            label="Reads",
            metric_name="latency_reads",
            levels_upper=(
                "fixed",
                tuple(level / 1e6 for level in threshold_latency_reads[1]),
            ),
            render_func=render.timespan,
        )

        yield from check_levels(
            value["writes"] / 1e6,
            label="Writes",
            metric_name="latency_writes",
            levels_upper=(
                "fixed",
                tuple(level / 1e6 for level in threshold_latency_writes[1]),
            ),
            render_func=render.timespan,
        )
    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_cluster_throughput(item, section):
    try:
        value = section["clusters"][item]["metrics"]["throughput"]
        yield from check_levels(
            value["reads"],
            label="Reads",
            metric_name="throughput_reads",
            render_func=lambda v: render.iobandwidth(v),
        )
        yield from check_levels(
            value["writes"],
            label="Writes",
            metric_name="throughput_writes",
            render_func=lambda v: render.iobandwidth(v),
        )
    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_cluster_capacity(item, params, section):
    try:
        value = section["clusters"][item]["capacity"]
        used_capacity = value["used_capacity"]
        free_space = value["free_space"]

        total = free_space + used_capacity
        used_percentage = used_capacity / total * 100

        yield from check_levels(
            used_percentage,
            label="Used",
            metric_name="used_percentage",
            levels_upper=params["cluster_used_percentage"],
            render_func=render.percent,
            boundaries=(0.0, 100.0),
        )

        state_string = ""
        for val in value.keys():
            yield Metric(val, value[val])
            state_string += f"{val}={value[val]} , "

        yield Result(
            state=State.OK,
            summary=(
                f"{render.bytes(used_capacity)} of {render.bytes(total)}; Free {render.bytes(free_space)}"
            ),
            details=state_string,
        )

    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_cluster_vms_status(item, params, section):
    try:
        value = section["clusters"][item]["vm_status"]

        safe_percentage = (
            value["safe"] / value["total"] * 100 if value["total"] > 0 else 0
        )
        yield from check_levels(
            safe_percentage,
            label="Safe VMs",
            metric_name="safe_percentage",
            levels_lower=params["safe_vms_percentage"],
            render_func=render.percent,
            boundaries=(0.0, 100.0),
        )

        for key, val in value.items():
            yield Metric(f"{key}_vms", val)

        yield Result(
            state=State.OK,
            summary=(
                f"Safe: {value['safe']}, Syncing: {value['syncing']}, Degraded: {value['degraded']}, Unknown: {value['unknown']}, Total: {value['total']}"
            ),
        )
    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


### HOST ###


def get_host_id(item, section):
    try:
        yield Result(state=State.OK, summary=section["hosts"][item]["host_id"])
    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_host_state(item, section):
    try:
        if section["hosts"][item]["state"] == "ALIVE":
            yield Result(state=State.OK, summary=section["hosts"][item]["state"])
        else:
            yield Result(state=State.WARN, summary=section["hosts"][item]["state"])
    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_host_virtual_controller_name(item, section):
    try:
        yield Result(
            state=State.OK, summary=section["hosts"][item]["virtual_controller_name"]
        )
    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_hosts_iops(item, section):
    try:
        value = section["hosts"][item]["metrics"]["iops"]
        yield from check_levels(value["reads"], label="Reads", metric_name="iops_reads")

        yield from check_levels(
            value["writes"], label="Writes", metric_name="iops_writes"
        )
    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_hosts_latency(item, params, section):
    try:
        threshold_latency_reads = params["latency_reads"]
        threshold_latency_writes = params["latency_writes"]
        value = section["hosts"][item]["metrics"]["latency"]
        yield from check_levels(
            value["reads"] / 1e6,
            label="Reads",
            metric_name="latency_reads",
            levels_upper=(
                "fixed",
                tuple(level / 1e6 for level in threshold_latency_reads[1]),
            ),
            render_func=render.timespan,
        )

        yield from check_levels(
            value["writes"] / 1e6,
            label="Writes",
            metric_name="latency_writes",
            levels_upper=(
                "fixed",
                tuple(level / 1e6 for level in threshold_latency_writes[1]),
            ),
            render_func=render.timespan,
        )
    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_hosts_throughput(item, section):
    try:
        value = section["hosts"][item]["metrics"]["throughput"]
        yield from check_levels(
            value["reads"],
            label="Reads",
            metric_name="throughput_reads",
            render_func=lambda v: render.iobandwidth(v),
        )

        yield from check_levels(
            value["writes"],
            label="Writes",
            metric_name="throughput_writes",
            render_func=lambda v: render.iobandwidth(v),
        )
    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_hosts_capacity(item, params, section):
    try:
        value = section["hosts"][item]["capacity"]
        free_space = value["free_space"]["value"]
        used_capacity = value["used_capacity"]["value"]
        total = free_space + used_capacity
        used_percentage = used_capacity / total * 100

        yield from check_levels(
            used_percentage,
            label="Used",
            metric_name="used_percentage",
            levels_upper=params["host_used_percentage"],
            render_func=render.percent,
            boundaries=(0.0, 100.0),
        )

        state_string = ""
        for val in value.keys():
            yield Metric(val, value[val]["value"])
            state_string += f"{val}={value[val]["value"]} , "

        yield Result(
            state=State.OK,
            summary=(
                f"{render.bytes(used_capacity)} of {render.bytes(total)}; Free {render.bytes(free_space)}"
            ),
            details=state_string,
        )
    except Exception as e:
        yield Result(state=State.CRIT, summary=f"Unable to get data {e}")


def get_hosts_hardware_status(item, section):
    try:
        value = section["hosts"][item]["hardware"]

        healthy = (
            value["host_status"] == "GREEN"
            and value["raid_status"] == "GREEN"
            and value["disk_status"] == "GREEN"
        )

        yield Result(
            state=State.OK if healthy else State.CRIT,
            summary="HEALTHY" if healthy else "NOT HEALTHY",
            details=(
                f"Host Status: {value['host_status']}, RAID Status: {value['raid_status']}, Disk Status: {value['disk_status']}"
            ),
        )

    except Exception:
        yield Result(
            state=State.CRIT,
            summary="Unknown status",
        )


agent_section_ = AgentSection(
    name="simplivity",
    parse_function=parse_json,
)


check_plugin_status = CheckPlugin(
    name="simplivity_status",
    sections=["simplivity"],
    service_name="Plugin Status",
    discovery_function=discover,
    check_function=get_status,
)

### Clusters ###

check_plugin_cluster_id = CheckPlugin(
    name="simplivity_cluster_id",
    sections=["simplivity"],
    service_name="Cluster %s ID",
    discovery_function=discover_cluster,
    check_function=get_cluster_id,
)

check_plugin_cluster_version = CheckPlugin(
    name="simplivity_cluster_version",
    sections=["simplivity"],
    service_name="Cluster %s Version",
    discovery_function=discover_cluster,
    check_function=get_cluster_version,
)


check_plugin_cluster_iops = CheckPlugin(
    name="simplivity_cluster_iops",
    sections=["simplivity"],
    service_name="Cluster %s IOPS",
    discovery_function=discover_cluster,
    check_function=get_cluster_iops,
)


check_plugin_cluster_latency = CheckPlugin(
    name="simplivity_cluster_latency",
    sections=["simplivity"],
    service_name="Cluster %s Latency",
    discovery_function=discover_cluster,
    check_function=get_cluster_latency,
    check_default_parameters={
        "latency_writes": ("fixed", (25000, 30000)),
        "latency_reads": ("fixed", (20000, 25000)),
    },
    check_ruleset_name="simplivity_thresholds",
)

check_plugin_cluster_throughput = CheckPlugin(
    name="simplivity_cluster_throughput",
    sections=["simplivity"],
    service_name="Cluster %s Throughput",
    discovery_function=discover_cluster,
    check_function=get_cluster_throughput,
)

check_plugin_cluster_capacity = CheckPlugin(
    name="simplivity_cluster_capacity",
    sections=["simplivity"],
    service_name="Cluster %s Capacity",
    discovery_function=discover_cluster,
    check_function=get_cluster_capacity,
    check_default_parameters={"cluster_used_percentage": ("fixed", (80.0, 90.0))},
    check_ruleset_name="simplivity_capacity_thresholds",
)

check_plugin_cluster_vms_status = CheckPlugin(
    name="simplivity_cluster_vms_status",
    sections=["simplivity"],
    service_name="Cluster %s VMs Status",
    discovery_function=discover_cluster,
    check_function=get_cluster_vms_status,
    check_default_parameters={"safe_vms_percentage": ("fixed", (80.0, 70.0))},
    check_ruleset_name="simplivity_capacity_thresholds",
)


### Hosts ###

check_plugin_host_id = CheckPlugin(
    name="simplivity_host_id",
    sections=["simplivity"],
    service_name="Host %s ID",
    discovery_function=discover_hosts,
    check_function=get_host_id,
)

check_plugin_host_state = CheckPlugin(
    name="simplivity_host_state",
    sections=["simplivity"],
    service_name="Host %s State",
    discovery_function=discover_hosts,
    check_function=get_host_state,
)


check_plugin_host_ovc = CheckPlugin(
    name="simplivity_host_ovc",
    sections=["simplivity"],
    service_name="Host %s OVC Controller",
    discovery_function=discover_hosts,
    check_function=get_host_virtual_controller_name,
)


check_plugin_host_iops = CheckPlugin(
    name="simplivity_host_iops",
    sections=["simplivity"],
    service_name="Host %s IOPS",
    discovery_function=discover_hosts,
    check_function=get_hosts_iops,
)


check_plugin_host_latency = CheckPlugin(
    name="simplivity_host_latency",
    sections=["simplivity"],
    service_name="Host %s Latency",
    discovery_function=discover_hosts,
    check_function=get_hosts_latency,
    check_default_parameters={
        "latency_writes": ("fixed", (25000, 30000)),
        "latency_reads": ("fixed", (20000, 25000)),
    },
    check_ruleset_name="simplivity_thresholds",
)

check_plugin_host_throughput = CheckPlugin(
    name="simplivity_host_throughput",
    sections=["simplivity"],
    service_name="Host %s Throughput",
    discovery_function=discover_hosts,
    check_function=get_hosts_throughput,
)


check_plugin_host_capacity = CheckPlugin(
    name="simplivity_host_capacity",
    sections=["simplivity"],
    service_name="Host %s Capacity",
    discovery_function=discover_hosts,
    check_function=get_hosts_capacity,
    check_default_parameters={"host_used_percentage": ("fixed", (80.0, 90.0))},
    check_ruleset_name="simplivity_capacity_thresholds",
)

check_plugin_host_hardware_status = CheckPlugin(
    name="simplivity_host_hardware_status",
    sections=["simplivity"],
    service_name="Host %s Hardware Status",
    discovery_function=discover_hosts,
    check_function=get_hosts_hardware_status,
)
