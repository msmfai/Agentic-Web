---
tags: [type/pattern, category/solid-principles]
---

# Single Responsibility Principle

A class should have only one reason to change, meaning it should have only one job or responsibility.

## Definition

Every module, class, or function should have responsibility over a single part of the functionality, and that responsibility should be entirely encapsulated by the class.

## Benefits

- **Easier maintenance**: Changes to one responsibility don't affect others
- **Better testability**: Focused units are easier to test
- **Improved readability**: Clear purpose for each component
- **Reduced coupling**: Components are more independent

## Application in Calculator

The calculator application separates responsibilities:

- **Operations**: Handle arithmetic logic only
- **Calculator**: Manage user interaction and coordinate operations
- **Main**: Handle application entry and setup

## Implementation

This principle is demonstrated in:

- [[operations.py|Operations Module]] - Only handles arithmetic
- [[calculator.py|Calculator Class]] - Only handles user interaction

## Related Patterns

- [[strategy-pattern.md|Strategy Pattern]]
