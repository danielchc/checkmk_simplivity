# HPE SimpliVity Checkmk Plugin

This Checkmk plugin provides monitoring for **HPE SimpliVity clusters and hosts**.

## Features

- Cluster-level and host-level performance metrics
- Latency and throughput monitoring
- Capacity reporting
- Basic health validation

### **General**

## 🧩 Cluster Data

Each discovered cluster includes:

### Cluster ID

Unique identifier of the cluster.

### Cluster Version

SimpliVity software/firmware version.

### Cluster IOPS

- **Reads** – Read operations per second
- **Writes** – Write operations per second

### Cluster Latency

- **Read latency** (with WARN/CRIT thresholds)
- **Write latency**

Latency values are automatically rendered as human-readable time spans.

### Cluster Throughput

- **Read throughput** – Data read per second
- **Write throughput** – Data written per second

---

## 🧩 Host Data

Each discovered host shows:

### **Host ID**

Unique host ID in the SimpliVity environment.

### **Host State**

- `ALIVE` → OK
- Anything else → WARN

### **OVC Controller Name**

The virtual controller assigned to the host.

### **Host IOPS**

Read and write IOPS.

### **Host Latency**

Read and write latency (threshold-based).

### **Host Throughput**

Read and write throughput as bandwidth metrics.

### **Host Capacity**

Dynamic storage metrics such as:

- total
- used
- free
