# Shift Brief AI CLI
## Adrienn Varn

Comments are somewhat sparse because the files are already heavily commented by the lab developers.

README adapted from existing lab README.

## Setup

Install dependencies before running the tests.

### Option 1: Pipenv (Recommended)

From the project root, run:

```bash
pipenv install --dev
pipenv shell
```

### Option 2: pip

From the project root, run:

```bash
python -m pip install -r requirements.txt
```

---

## Running the Tests

Run the test suite from the project root:

```bash
pytest
```

## Manual Run

After your tests pass, your CLI should have full functionality.

To try it out, from the project root, run:

```bash
python lib/shift_cli
```

Generated AI responses may vary because the model creates the output.

---

## Example CLI Session

When you start the application, you should see command guidance similar to this:

```txt
Shift Handoff Brief CLI
Create and revise AI-assisted shift handoff briefs.

Commands:
- brief <shift notes>     Create a new handoff brief.
- revise <feedback>      Revise the previous brief using feedback.
- history                Show the current conversation message count.
- reset                  Clear conversation history.
- help                   Show this command list.
- exit or quit           Stop the program.
```

Create a new brief:

```txt
> brief Register 2 froze twice during closing. Maya restarted it, but it may need IT review tomorrow. Stockroom still has three carts of unsorted returns.
```

Example output:

```txt
Shift Handoff Brief
Shift Summary:
Register 2 froze twice during closing and may need IT review. The stockroom still has three carts of unsorted returns.

Open Issues:
Register 2 may still need IT review. Three carts of returns remain unsorted.

Action Items:
Ask IT to inspect Register 2. Assign staff to sort the remaining returns.

Follow-Up Questions:
Did Register 2 display an error code? Are the returns time-sensitive?

Risk Notes:
A frozen register may slow checkout if the issue continues. Unsorted returns may affect the next shift’s workflow.
```

Revise the previous brief:

```txt
> revise Make the action items more specific and include who should review Register 2.
```

Example output:

```txt
Revised Shift Handoff Brief
Shift Summary:
Register 2 froze twice during closing and may need IT review. The stockroom still has three carts of unsorted returns.

Open Issues:
Register 2 may continue to freeze during checkout. Three carts of returns remain unsorted.

Action Items:
Ask the IT team to inspect Register 2 before the next busy checkout period. Ask the opening manager to assign staff to sort the remaining returns.

Follow-Up Questions:
Did Register 2 display an error code? Is there a backup register available if the problem happens again?

Risk Notes:
A frozen register may slow checkout. Unsorted returns may delay restocking or create extra work for the next shift.
```

Check conversation history:

```txt
> history
```

Example output:

```txt
Conversation messages: 4
```

Reset conversation history:

```txt
> reset
```

Example output:

```txt
Conversation history reset.
```

Exit the application:

```txt
> exit
```

Example output:

```txt
Goodbye!
```
