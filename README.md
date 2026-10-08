# Toy Vault: a red-team practice safe

**A tiny vault with fake money and four planted mistakes.** This is a toy for a workshop. It is not a wallet, a bank, a payment app, or Bitcoin software. There is no network, nothing to install, and no way to lose anything. All names and amounts are invented.

## Get it

```sh
git clone https://github.com/Rob1Ham/toy-vault.git
cd toy-vault
python3 -m unittest discover -s tests -v
```

No Git? Download the ZIP from the green **Code** button and skip the clone.

## Two ways to play

**No-code track (anyone):** Read `rules-card.md`, pick ONE rule, and write a cheat script in plain English: who you are, what you send, what you expect to happen, and what the rule says should happen instead. That's it — you just did a threat model.

**Code track (if you read code):** Open `toy_vault.py`, pick ONE rule, and find the lines where the code fails to enforce it. If you have an AI coding helper like OpenCode, point it at this folder and ask it to check your rule — then check its answer yourself.

Both tracks end in the same place: **one claim, one piece of evidence, one honest limit** (something you did not check).

## The full loop (workshop demo)

The grown-up version of this exercise is a cycle, and every step uses the same thinking:

1. **Scan** — ask an AI helper (or your own eyes) where one rule fails. Demand line numbers.
2. **Evaluate** — turn each claim into a test you can run. Keep what survives; keep a note on what you couldn't check.
3. **Propose** — write the fix and a test that fails on the old code, and open a pull request.
4. **Review** — have a different set of eyes (human, AI, or both) check that the fix works and breaks nothing honest.
5. **Merge** — a human decides.
6. **Retest** — run the tests again and rescan. The old flaw should now be impossible; the honest spends should still work.

Repeat per flaw. That's the whole professional loop: scan → evaluate → propose → review → merge → retest.

## Run it (optional, code track)

Python 3.11+ is enough:

```sh
python3 -m unittest discover -s tests -v
```

The two passing tests show ordinary, honest behavior. They do **not** prove the rules below hold — that's your job.

## The rules every vault must keep

1. **Only the owner** — or someone the owner named — may hand a spend request to the vault.
2. **Two different approved people** must say yes. The same name twice is one person.
3. **The vault can never go below zero** — the fee counts as part of the spend.
4. **The same request must never pay twice.**
5. **The preview and the real spend must agree.**

Your goal: pick one rule and show how it breaks, using made-up accounts. Say what you did NOT test. Never connect this code to anything real, and never try this logic on a system you don't own.

## If you're using an AI helper

Point it at this folder and say the target is intentionally vulnerable. Good opening questions:

- "If I wanted to cheat this vault, where would I start? Which line would I abuse? How would you check?"
- "Does anything check that the person submitting is the owner? Cite lines."
- "Can the same payment happen twice? What stops it, exactly?"
- "Can the vault end up negative? Trace the fee."

Treat every answer as a **hunch until you test it**. Ask for line numbers, then look yourself. A confident answer with no line numbers is a rumor.

## Public alternative

Prefer a bigger playground? [OWASP Juice Shop](https://github.com/juice-shop/juice-shop) is a well-known intentionally insecure practice website. Run it **on your own machine** (`docker run --rm -p 127.0.0.1:3000:3000 bkimminich/juice-shop`), never against its shared public demo instance.
