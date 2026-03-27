# LLM-Based Automated Unit Test Generation System

## Overview
This project implements an automated unit test generation system using Large Language Models (LLMs).

The system takes Java classes as input and generates JUnit test cases, then iteratively improves them using feedback from compilation, execution, and mutation testing.

## Project Structure

- testgen-runner/  
  Python-based pipeline for test generation, validation, and repair

- testgen-lab/  
  Java project under test (Maven-based)

## Features

- LLM-based test generation
- Compile error detection and repair
- Test execution using Maven
- Failure parsing and semantic repair
- Mutation testing (PIT) integration
- Iterative improvement loop

## Requirements

- Python 3.10+
- Java JDK 17
- Maven 3.9+
- Ollama (for local LLM)

## Setup

1. Clone the repository
2. Install Python dependencies
3. Install Java and Maven
4. Install Ollama and pull a model (e.g. deepseek / llama)

## Usage

Run the pipeline:
