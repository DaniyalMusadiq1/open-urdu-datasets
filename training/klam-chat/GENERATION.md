# Scaling Klam Chat with local generation

The target is one million rows total, counting both script variants. Each new scenario contributes two rows, one in Urdu script and one in Roman Urdu. The generator writes unreviewed synthetic candidates to SQLite. Original validation and test rows stay in their original splits.

Install the project dependencies and start Ollama locally with a model that handles both scripts. Replace MODEL with an installed model name. Start with a small batch and read the output before scaling.

```bash
python scripts/generate_klam_chat.py --db klam-candidates.sqlite --model MODEL --max-pairs 10
python scripts/generate_klam_chat.py --db klam-candidates.sqlite --model MODEL --export klam-pilot
```

Repeat generation with the same database and model to resume. Use a fresh export directory for each snapshot. Keep the database and generated files outside version control. The model must be available at the standard local Ollama endpoint.

Checks cover message structure, turn order, a basic script check, and exact normalized opening-prompt duplicates across the starter and new candidates. Similar prompts and mismatched answers can still pass. Review candidates for natural language, correctness, alignment between scripts and near-duplicates before a public release. The existing evaluation sets remain small.
