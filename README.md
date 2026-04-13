# Battledot — Distributed Ring Topology Simulation

## Overview

Battledot is a **peer-to-peer distributed system simulation** implemented in Python. It models a dynamic ring topology where independent nodes (players) communicate over sockets, exchange messages, and reconfigure the network in response to node failures.

Each node operates autonomously, maintaining only local knowledge of its neighbors while participating in a global game state.

---

## Problem Statement

This project explores a fundamental distributed systems challenge:

> How do independently running nodes maintain a consistent communication structure when nodes fail dynamically?

Battledot simulates this using a game abstraction:

* Each node represents a player in a ring
* Nodes communicate only with adjacent peers
* When a node is eliminated, the network must **self-heal** by reconnecting its neighbors

---

## System Design

### Topology

* Nodes are arranged in a **unidirectional ring**
* Each node:

  * Sends messages to one neighbor (outgoing)
  * Receives messages from another neighbor (incoming)

Example:
A → B → C → D → A

---

### Communication Model

* Peer-to-peer communication using **IP + Port-based socket connections**
* No central coordinator or server
* Each node:

  * Sends attack messages
  * Receives attack results
  * Updates neighbors on topology changes

---

### Failure Handling & Recovery

When a node is eliminated:

1. It notifies its adjacent nodes
2. The adjacent nodes reconnect to each other
3. The ring topology is restored without global coordination

Example:
A → B → C → D → A
If C is eliminated →
A → B → D → A

---

## Game Mechanics (Abstraction Layer)

* Each node maintains a 10x10 grid
* A single “ship” is randomly placed
* Nodes attack neighbors with random coordinates
* If a ship is hit → node is eliminated
* The game continues until only one node remains

---

## Key Engineering Concepts

* **Decentralized system design**
* **Ring topology maintenance**
* **Fault tolerance via local recovery**
* **Peer-to-peer communication**
* **Dynamic network reconfiguration**

---

## Limitations

* Assumes reliable message delivery (no packet loss handling)
* No synchronization guarantees between nodes
* Minimal fault tolerance beyond node elimination
* Single-file implementation limits modularity and scalability

---

## How to Run

### Same Machine (Multiple Ports)

Run each node as a separate process:

```bash
python Battledot.py N/A N/A <PortA> <PortB> <NumPlayers> <MyPort>
```

Initialize the final node with:

```bash
python Battledot.py N/A N/A <PortA> <PortB> <NumPlayers> <MyPort> first
```

---

### Different Machines (Networked)

```bash
python Battledot.py <IP_A> <IP_B> <PortA> <PortB> <NumPlayers> <MyPort>
```

Final node:

```bash
python Battledot.py <IP_A> <IP_B> <PortA> <PortB> <NumPlayers> <MyPort> first
```

---

## Example Output

* "Sent attack to X"
* "Received attack from Y"
* "Hit! Player Lose"
* "Reconnecting neighbors"
* "You are the last player remaining"

---

## Future Improvements

* Refactor into modular components (networking, game logic, state management)
* Add message protocol definitions
* Introduce failure scenarios (network drops, retries)
* Build a visualization layer for ring topology
* Add simulation mode for large-scale testing

---

## Why This Project

This project was originally built as a take-home assessment but evolved into an exploration of **distributed systems fundamentals**, particularly:

* decentralized coordination
* topology repair
* and fault handling without a central authority

---

## Tech Stack

* Python 3
* Socket Programming
* Multi-process execution (manual orchestration)

---
