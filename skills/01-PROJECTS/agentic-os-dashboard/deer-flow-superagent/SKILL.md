---
name: deer-flow-superagent
description: >
  MUST USE when orchestrating complex multi-step tasks that require sub-agents,
  sandboxing, or long-horizon execution (minutes to hours).
  
  Features:
  - Sub-agent spawning and coordination
  - Memory management across agents
  - Sandboxed execution
  - Skill composition
  - Podcast output mode
  
  NOT for: simple single-step tasks, quick queries.
metadata:
  hermes:
    tags: [deer-flow, superagent, orchestration, sub-agents, multi-step]
    priority: high
---

# Deer Flow — SuperAgent Harness

## Overview
SuperAgent harness for complex task orchestration. Handles tasks from minutes to hours.

## Key Features

### 1. Sub-Agent Spawning
- Spawn specialized sub-agents for parallel tasks
- Coordinate results across agents
- Manage agent lifecycle

### 2. Memory Management
- Persistent memory across agent sessions
- Context sharing between sub-agents
- Long-term knowledge retention

### 3. Sandboxed Execution
- Isolated execution environments
- Safe code testing
- Resource limits

### 4. Skill Composition
- Combine multiple skills in a single workflow
- Chain skill outputs
- Conditional skill selection

### 5. Output Modes
- Text reports
- Code generation
- Podcast/audio output
- Multi-format delivery

## Usage Guidelines
1. Use for tasks requiring >5 steps
2. Decompose complex problems into sub-tasks
3. Monitor sub-agent progress
4. Aggregate results before delivery
