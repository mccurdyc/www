---
title: "Kubernetes: Up and Running"
subtitle: ""
description: ""
author: "Colton J. McCurdy"
date: 2026-06-06T00:00:00-04:00
image: "/image/book-covers/kubernetes-up-and-running/cover.jpg"
book-tags: ["book", "2026"]
books: ["Kubernetes: Up and Running - Third Edition"]
book-authors: ["Brendan Burns", "Joe Beda", "Kelsey Hightower", "Lachlan Evenson"]
amazon: ""
thriftbooks: ""
draft: false
---

## Chapter 10

p7 - NodePort:               <unset> 32711/TCP Endpoints:              10.112.1.66:8080,10.112.2.104:8080,10.112.2.105:8080

p7 - NodePort without knowing where any of the Pods for that service are running

p7 - we can hit any of our cluster nodes on that port to access the service

p11 - Some applications (and the system itself) want to be able to use services without using a cluster IP

p13 - Cluster IPs are stable virtual IPs that load balance traffic across all of the endpoints in a service. This magic is performed by a component running on every node in the cluster called the kube-proxy

p14 - It then programs a set of iptables rules in the kernel of that host to rewrite the destinations of packets so they are directed at one of the endpoints for that service


## Chapter 11

p1 - Service object operates at Layer 4

p1 - “virtual hosting.” This is a mechanism to host many HTTP sites on a single IP address.


## Chapter 13

p1 - The Deployment object exists to manage the release of new versions


## Chapter 14

p1 - a single Pod on every node within the cluster. Generally, the motivation for replicating a Pod to every node is to land some sort of agent or daemon on each node, and the Kubernetes object for achieving this is the DaemonSet.

p1 - a single Pod per node, then a DaemonSet


## Chapter 24

p5 - With anycast networking, a single static IP address is advertised from multiple locations around the internet using core routing protocols.

p5 - Your traffic is routed to the “closest” location based on the distance in terms of network performance rather than geographic distance.


## Chapter 26

p3 - Setting Up Networking

p9 - kubeadm join --token=<token> 10.0.0.1

p9 - On the API server node (the one running DHCP and connected to the internet),run:$ sudo kubeadm init --pod-network-cidr 10.244.0.0/16 \\        --apiserver-advertise-address 10.0.0.1 \\        --apiserver-cert-extra-sans kubernetes.cluster.home

p9 - You have your node-level networking set up, but you still need to set up the Pod-to-Pod networking.
