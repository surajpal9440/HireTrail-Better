# AI Usage Guidelines — HireTrail

## How AI Was Used

AI assistance (GitHub Copilot / ChatGPT / similar) was used in the following ways:

- **Boilerplate generation**: Scaffold Flask app factory, Marshmallow schema stubs
- **Test case ideas**: Suggested edge cases to test (invalid URL, missing required fields, unknown status values)
- **CSS tokens**: Helped define initial CSS custom property names and dark theme palette

## What AI Was Allowed To Do

- Suggest code structure and patterns
- Generate first drafts of boilerplate (models, schemas, fixtures)
- Help write test cases and docstrings
- Suggest variable names and error messages

## What AI Was NOT Allowed To Do

- Make architectural decisions (those were human-defined upfront)
- Copy-paste output blindly into the codebase
- Define API contracts or database schema
- Choose libraries or dependencies

## Review Process

Every AI-generated snippet was:
1. Read and understood before being used
2. Tested manually or via automated tests
3. Refactored for clarity if needed
4. Verified against the project's coding standards

## Prompting Rules

- Prompts included full context: "Given this Flask app factory pattern, generate a service layer for job CRUD..."
- Outputs were reviewed for correctness, not just copied
- If the AI output was wrong, it was corrected — not blindly trusted

## Coding Standards Enforced

- No magic strings: all statuses in `JobStatus` class constants
- All API responses through `response.success()` / `response.error()` — never raw `jsonify`
- Validation only in schemas, never in routes or services
- Service functions return model objects, not dicts — serialization happens in routes

## Banned Patterns

- Inline SQL (SQLAlchemy ORM only)
- try/except swallowing errors silently
- Hardcoded URLs on the frontend
- Business logic in React components (use API layer)
