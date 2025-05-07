#!/usr/bin/env python3
from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service, Result, State, Metric, check_levels

import itertools
import json

def parse_json(string_table):
    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    return parsed


def discover_cluster(section):
    for cluster in section["clusters"].keys():
        yield Service(item=section["clusters"][cluster]["name"])
        
def discover_hosts(section):
    for cluster in section["hosts"].keys():
        yield Service(item=section["hosts"][cluster]["name"])


### CLUSTER ###

def get_cluster_id(item,section):
    yield Result(state=State.OK, summary= section["clusters"][item]["cluster_id"])
    
def get_cluster_version(item,section):
    yield Result(state=State.OK, summary= section["clusters"][item]["version"])

def get_cluster_iops(item,section):
    value = section["clusters"][item]["metrics"]["iops"]
    yield Metric("reads", value["reads"])
    yield Metric("writes", value["writes"])
    yield Result(state=State.OK, summary=f"Read {value["reads"]} / Write {value["writes"]}")

def get_cluster_latency(item,section):
    value =  section["clusters"][item]["metrics"]["latency"]
    yield Metric("reads", value["reads"])
    yield Metric("writes", value["writes"])
    yield Result(state=State.OK, summary=f"Read {value["reads"]} / Write {value["writes"]}")
    
def get_cluster_throughput(item,section):
    value = section["clusters"][item]["metrics"]["throughput"]
    yield Metric("reads", value["reads"])
    yield Metric("writes", value["writes"])
    yield Result(state=State.OK, summary=f"Read {value["reads"]} / Write {value["writes"]}")

### HOST ###

def get_host_id(item,section):
    yield Result(state=State.OK, summary= section["hosts"][item]["host_id"])
    
def get_host_virtual_controller_name(item,section):
    yield Result(state=State.OK, summary= section["hosts"][item]["virtual_controller_name"])
    

def get_hosts_iops(item,section):
    value = section["hosts"][item]["metrics"]["iops"]
    yield Metric("reads", value["reads"])
    yield Metric("writes", value["writes"])
    yield Result(state=State.OK, summary=f"Read {value["reads"]} / Write {value["writes"]}")

def get_hosts_latency(item,section):
    value =  section["hosts"][item]["metrics"]["latency"]
    yield Metric("reads", value["reads"])
    yield Metric("writes", value["writes"])
    yield Result(state=State.OK, summary=f"Read {value["reads"]} / Write {value["writes"]}")
    
def get_hosts_throughput(item,section):
    value = section["hosts"][item]["metrics"]["throughput"]
    yield Metric("reads", value["reads"])
    yield Metric("writes", value["writes"])
    yield Result(state=State.OK, summary=f"Read {value["reads"]} / Write {value["writes"]}")


def get_hosts_capacity(item,section):
    value = section["hosts"][item]["capacity"]

    state_string=""
    for val in value.keys():
        yield Metric(val, value[val]["value"])
        state_string += f"{val}={value[val]["value"]} , " 

    yield Result(state=State.OK, summary=state_string)



agent_section_ = AgentSection(
    name = "simplivity",
    parse_function = parse_json,
)

### Clusters ###

check_plugin_cluster_id = CheckPlugin(
    name = "simplivity_cluster_id",
    sections=["simplivity"],
    service_name = "Cluster %s ID",
    discovery_function = discover_cluster,
    check_function = get_cluster_id,
)

check_plugin_cluster_version = CheckPlugin(
    name = "simplivity_cluster__version",
    sections=["simplivity"],
    service_name = "Cluster %s Version",
    discovery_function = discover_cluster,
    check_function = get_cluster_version,
)


check_plugin_cluster_iops = CheckPlugin(
    name = "simplivity_cluster_iops",
    sections=["simplivity"],
    service_name = "Cluster %s IOPS",
    discovery_function = discover_cluster,
    check_function = get_cluster_iops,
)


check_plugin_cluster_latency = CheckPlugin(
    name = "simplivity_cluster_latency",
    sections=["simplivity"],
    service_name = "Cluster %s Latency",
    discovery_function = discover_cluster,
    check_function = get_cluster_latency,
)

check_plugin_cluster_throughput = CheckPlugin(
    name = "simplivity_cluster_throughput",
    sections=["simplivity"],
    service_name = "Cluster %s Throughput",
    discovery_function = discover_cluster,
    check_function = get_cluster_throughput,
)

### Hosts ###

check_plugin_host_id = CheckPlugin(
    name = "simplivity_host_id",
    sections=["simplivity"],
    service_name = "Host %s ID",
    discovery_function = discover_hosts,
    check_function = get_host_id,
)


check_plugin_host_ovc = CheckPlugin(
    name = "simplivity_host_ovc",
    sections=["simplivity"],
    service_name = "Host %s OVC Controller",
    discovery_function = discover_hosts,
    check_function = get_host_virtual_controller_name,
)


check_plugin_host_iops = CheckPlugin(
    name = "simplivity_host_iops",
    sections=["simplivity"],
    service_name = "Host %s IOPS",
    discovery_function = discover_hosts,
    check_function = get_hosts_iops,
)


check_plugin_host_latency = CheckPlugin(
    name = "simplivity_host_latency",
    sections=["simplivity"],
    service_name = "Host %s Latency",
    discovery_function = discover_hosts,
    check_function = get_hosts_latency,
)

check_plugin_host_throughput = CheckPlugin(
    name = "simplivity_host_throughput",
    sections=["simplivity"],
    service_name = "Host %s Throughput",
    discovery_function = discover_hosts,
    check_function = get_hosts_throughput,
)


check_plugin_host_capacity = CheckPlugin(
    name = "simplivity_host_capacity",
    sections=["simplivity"],
    service_name = "Host %s Capacity",
    discovery_function = discover_hosts,
    check_function = get_hosts_capacity,
)
