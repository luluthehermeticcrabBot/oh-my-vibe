# Migrating from upstream Vibe

Oh My Vibe deliberately does not read or adopt `~/.vibe` state, and it does not
interpret `VIBE_HOME` as `OMV_HOME`. Existing upstream state remains untouched.

To make an explicit copy, provide both source and destination and run the
migration helper with `--apply`:

```bash
python scripts/migrate_vibe_state.py \
  --source ~/.vibe \
  --destination ~/.omv \
  --apply
```

The helper validates that the source is a directory, the destination is not
inside the source, and that the destination is absent or an existing directory.
It reports the planned files first and will not write unless `--apply` is
present. The copy is additive and never deletes, moves, or rewrites the source.
Review the output before using the copied configuration, especially credentials
in `.env`; never paste credentials into issue reports or logs.

If you previously used the `vibe`, `vibe-acp`, or `vibe-app-server` commands,
install Oh My Vibe and use `omv`, `omv-acp`, and `omv-app-server` instead. The
old commands are not installed as compatibility shims.
