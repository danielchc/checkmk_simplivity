# HPE SimpliVity Checkmk Plugin

Monitor HPE SimpliVity clusters (VMware) and hosts from Checkmk using the SimpliVity REST API.

## Requirements

- Checkmk 2.3.0 or newer
- Network access from the Checkmk site to the SimpliVity API over HTTPS
- A SimpliVity account with permission to read cluster, host, VM, capacity, and hardware information

## Installation and setup

Install the plugin as a Checkmk extension package, or place its `agent_based`, `graphing`, `libexec`, `rulesets`, and `server_side_calls` directories under the site-local plugin directory:

```text
~/local/lib/python3/cmk_addons/plugins/simplivity/
```

Activate the changes in Checkmk, then create a **HPE Simplivity** special agent rule and assign it to a host. The assigned host's name is used as the SimpliVity API hostname. Enter the API username and password in the rule, then run service discovery on that host.

## Monitored data

### Clusters

- Cluster ID and SimpliVity version
- Read and write IOPS, latency, and throughput
- Physical capacity, including used and free space
- VM health counts for safe, syncing, degraded, and unknown VMs

### Hosts

- Host ID, state, and virtual controller name
- Read and write IOPS, latency, and throughput
- Capacity metrics, including used and free space
- Host, RAID, and disk hardware health

Latency and capacity checks report threshold states. Read and write performance metrics are also available for Checkmk graphs.

## Default thresholds

| Check                 |   Warning |  Critical |
| --------------------- | --------: | --------: |
| Read latency          | 20,000 µs | 25,000 µs |
| Write latency         | 25,000 µs | 30,000 µs |
| Cluster used capacity |       80% |       90% |
| Host used capacity    |       80% |       90% |
| Safe VMs              | Below 80% | Below 70% |

Latency thresholds are upper limits. Safe VM percentage uses lower limits, so falling below the warning or critical percentage raises the corresponding state.

## TLS note

The special agent currently disables TLS certificate verification for API requests. Connections are encrypted, but the server certificate is not validated. Use this plugin only on trusted networks until certificate verification is implemented.
