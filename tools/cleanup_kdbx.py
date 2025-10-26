"""Utility for removing obsolete KeePass entries based on an allow-list of emails.

This script uses pykeepass to open a KeePass database (.kdbx), reads an allow-list of
email addresses from a CSV file, and deletes every entry inside specific groups whose
email address is not present in the allow-list. The email address for an entry is
resolved using the following priority:

1. A custom field named "Email" or "E-Mail" (case-insensitive)
2. The username field

Example usage::

    python tools/cleanup_kdbx.py \
        --database /path/to/database.kdbx \
        --password secret \
        --csv active_accounts.csv \
        --groups "Root/Clients/Acme" "Root/Clients/Beta" \
        --email-column email \
        --dry-run

Use ``--dry-run`` to preview the deletions without modifying the database. By default
all matching entries will be removed and the database will be saved in-place. Pass
``--output`` to save the cleaned database to a different file instead.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Set

from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsError, CompositeSignatureError

EMAIL_FIELD_CANDIDATES = ("email", "e-mail")


class CleanupError(Exception):
    """Custom error type for cleanup operations."""


def read_allowed_emails(csv_path: Path, column: Optional[str]) -> Set[str]:
    """Read the CSV file and return a set of normalized email addresses."""
    try:
        with csv_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            fieldnames = reader.fieldnames or []
            if not fieldnames:
                raise CleanupError("CSV file does not contain any headers")

            if column is None:
                # If no column is provided, use the first column in the file
                target_column = fieldnames[0]
            else:
                column_lower = column.lower()
                matches = [name for name in fieldnames if name.lower() == column_lower]
                if not matches:
                    raise CleanupError(
                        f"Column '{column}' not found in CSV. Available columns: {', '.join(fieldnames)}"
                    )
                target_column = matches[0]

            emails = set()
            for row in reader:
                raw_value = row.get(target_column)
                normalized = normalize_email(raw_value)
                if normalized:
                    emails.add(normalized)
            if not emails:
                raise CleanupError(
                    f"No email addresses found in column '{target_column}' of {csv_path}"
                )
            return emails
    except FileNotFoundError as exc:
        raise CleanupError(f"CSV file not found: {csv_path}") from exc
    except OSError as exc:
        raise CleanupError(f"Unable to read CSV file: {csv_path}") from exc


def normalize_email(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    return value.lower()


def extract_entry_email(entry) -> Optional[str]:
    """Return the best-effort email address for a KeePass entry."""
    for field in EMAIL_FIELD_CANDIDATES:
        value = entry.get_custom_property(field)
        normalized = normalize_email(value)
        if normalized:
            return normalized
    return normalize_email(entry.username)


def resolve_group(kp: PyKeePass, group_path: str):
    """Return the KeePass group matching the provided slash-delimited path."""
    parts = [part for part in group_path.strip("/").split("/") if part]
    if not parts:
        raise CleanupError("Group path must not be empty")

    group = kp.root_group
    for part in parts:
        next_group = next((g for g in group.subgroups if g.name == part), None)
        if next_group is None:
            raise CleanupError(f"Group '{part}' not found under '{group.name}'")
        group = next_group
    return group


def collect_entries(group) -> List:
    """Collect all entries recursively from the given group."""
    entries = list(group.entries)
    for subgroup in group.subgroups:
        entries.extend(collect_entries(subgroup))
    return entries


def delete_obsolete_entries(
    kp: PyKeePass,
    groups: Sequence[str],
    allowed_emails: Set[str],
    dry_run: bool,
) -> List[str]:
    """Delete entries not present in the allowed email set.

    Returns a list of entry titles that were deleted (or would be deleted in dry-run).
    """
    deleted_entries: List[str] = []

    for group_path in groups:
        group = resolve_group(kp, group_path)
        for entry in collect_entries(group):
            entry_email = extract_entry_email(entry)
            if entry_email and entry_email in allowed_emails:
                continue
            deleted_entries.append(entry.title or "<Untitled>")
            if not dry_run:
                kp.delete_entry(entry)

    return deleted_entries


def parse_arguments(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True, help="Path to the KeePass database (.kdbx)")
    parser.add_argument("--password", help="Master password for the database")
    parser.add_argument("--keyfile", help="Optional keyfile for the database")
    parser.add_argument("--csv", required=True, help="CSV file containing active accounts")
    parser.add_argument(
        "--email-column",
        help="Name of the column in the CSV that contains email addresses. Defaults to the first column.",
    )
    parser.add_argument(
        "--groups",
        nargs="+",
        required=True,
        help="Slash-separated paths of KeePass groups to clean, e.g. 'Root/Folder/SubFolder'.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to save the cleaned database. Defaults to overwriting the original file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview deletions without modifying the database.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_arguments(argv)

    csv_path = Path(args.csv)
    database_path = Path(args.database)

    try:
        allowed_emails = read_allowed_emails(csv_path, args.email_column)
    except CleanupError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        kp = PyKeePass(str(database_path), password=args.password, keyfile=args.keyfile)
    except (CredentialsError, CompositeSignatureError) as exc:
        print("Error: Unable to unlock KeePass database - check password/keyfile.", file=sys.stderr)
        return 2
    except FileNotFoundError:
        print(f"Error: KeePass database not found: {database_path}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error: Unable to open KeePass database: {exc}", file=sys.stderr)
        return 1

    deleted_entries = delete_obsolete_entries(kp, args.groups, allowed_emails, args.dry_run)

    if deleted_entries:
        print("Entries to delete:" if args.dry_run else "Deleted entries:")
        for title in deleted_entries:
            print(f" - {title}")
    else:
        print("No entries need to be deleted.")

    if not args.dry_run:
        output_path = Path(args.output) if args.output else database_path
        try:
            kp.save(str(output_path))
        except OSError as exc:
            print(f"Error: Unable to save database to {output_path}: {exc}", file=sys.stderr)
            return 1
        print(f"Database saved to {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
