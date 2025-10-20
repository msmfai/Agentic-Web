---
tags: [type/pattern, category/behavioral]
---

# Strategy Pattern

The Strategy Pattern is a behavioral design pattern that enables selecting an algorithm at runtime.

## Intent

Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

## Structure

- **Strategy**: Interface common to all algorithms
- **Concrete Strategies**: Different implementations of the algorithm
- **Context**: Uses a Strategy to execute the algorithm

## Benefits

- Open/Closed Principle: New strategies can be added without changing context
- Single Responsibility: Each strategy handles one algorithm
- Runtime flexibility: Switch algorithms dynamically

## Usage in Calculator

The calculator uses the Strategy Pattern to encapsulate different arithmetic operations:

- Each operation (add, subtract, multiply, divide) is a separate strategy
- Operations can be executed through a common interface
- New operations can be added without modifying existing code

## Implementation

This pattern is used in:

- [[operations.py|Operations Module]]

## Related Concepts

- [[arithmetic-operations.md|Arithmetic Operations]]
