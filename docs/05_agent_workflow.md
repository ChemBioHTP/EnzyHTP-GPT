# AI Agent Workflow

The core of EnzyHTP-GPT's intelligence lies in its AI agents, which are powered by OpenAI's GPT models. The workflow is orchestrated by a series of prompts and agents that guide the user through the process of designing and analyzing experiments.

*(Placeholder for an agent workflow diagram)*

## Main Agents

The main agents in the workflow are:

1.  **Question Analyzer**: This agent's primary role is to take the user's initial scientific question and refine it. It decomposes and revises the question to ensure it is clear, specific, and actionable for the subsequent steps in the workflow.

2.  **Metrics Planner**: Once the scientific question is clarified, this agent helps the user select the appropriate computational metrics to measure the desired properties of the protein. It provides suggestions and explanations for the available metrics.

3.  **Mutant Planner**: This agent translates the user's natural language description of desired mutations into the precise syntax required by the EnzyHTP library. This allows for a more intuitive and less error-prone way to define the mutation space for an experiment.

## Prompts

The prompts that define the behavior of these agents can be found in the `flask-server/prompts` directory.

## Benchmarking

The `flask-server/agent_benchmark` directory contains scripts and data for evaluating and benchmarking the performance of the LLM agents.
