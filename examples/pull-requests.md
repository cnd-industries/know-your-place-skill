# Pull request descriptions

## AI footer

Wrong:

```markdown
## Summary
- Add pagination to the `/users` endpoint
- Cap page size at 100

## Test plan
- [x] Unit tests for page boundaries

Generated with [Claude Code](https://claude.com/claude-code)
```

Right:

```markdown
## Summary
- Add pagination to the `/users` endpoint
- Cap page size at 100

## Test plan
- [x] Unit tests for page boundaries
```

## The assistant talking about itself

Wrong:

```markdown
As an AI assistant, I've updated the error handling to be more robust.
Let me know if you'd like me to make any other changes!
```

Right:

```markdown
Wrap database errors in `StorageError` so callers can tell them apart from validation failures.
```

## Review replies

Wrong:

> Good catch! Claude has updated the function to handle the empty case.

Right:

> Fixed: the function now returns early on empty input.
