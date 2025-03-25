#!/usr/bin/env python3

import argparse
import hashlib
import json
import os

HASH_FILE_NAME = ".file_hashes.json"

def calculate_hash(filepath):
    """Calculates the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as file:
            while True:
                chunk = file.read(4096)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None

def get_hash_file_path(input_path):
    """Determines the location of the hash file."""
    if os.path.isdir(input_path):
        return os.path.join(input_path, HASH_FILE_NAME)
    else:
        return os.path.join(os.path.dirname(input_path) or '.', HASH_FILE_NAME)

def store_hashes(hashes, filepath):
    """Stores the computed hashes to a JSON file."""
    try:
        with open(filepath, 'w') as f:
            json.dump(hashes, f, indent=4)
        return True
    except Exception as e:
        print(f"Error storing hashes: {e}")
        return False

def load_hashes(filepath):
    """Loads the stored hashes from a JSON file."""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading hashes: {e}")
        return {}

def process_path(path):
    """Returns a list of file paths from a given path (single file or directory)."""
    if os.path.isfile(path):
        return [path]
    elif os.path.isdir(path):
        return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    else:
        print(f"Error: Invalid path: {path}")
        return

def init_command(args):
    """Initializes and stores hashes of log files."""
    input_path = args.path
    files_to_hash = process_path(input_path)
    if not files_to_hash:
        return

    hashes = {}
    for file_path in files_to_hash:
        hash_value = calculate_hash(file_path)
        if hash_value:
            hashes[file_path] = hash_value

    hash_file_path = get_hash_file_path(input_path)
    if store_hashes(hashes, hash_file_path):
        print("Hashes stored successfully.")

def check_command(args):
    """Checks the integrity of log files by comparing hashes."""
    input_path = args.path
    files_to_check = process_path(input_path)
    if not files_to_check:
        return

    hash_file_path = get_hash_file_path(input_path)
    stored_hashes = load_hashes(hash_file_path)

    if not stored_hashes:
        print("Warning: Hash file not found. Please run 'init' first.")
        return

    discrepancies = False
    for file_path in files_to_check:
        current_hash = calculate_hash(file_path)
        if current_hash:
            if file_path in stored_hashes:
                if current_hash == stored_hashes[file_path]:
                    print(f"Status for {file_path}: Unmodified")
                else:
                    print(f"Status for {file_path}: Modified (Hash mismatch)")
                    discrepancies = True
            else:
                print(f"Status for {file_path}: New file (Not in initial hash list)")
                discrepancies = True

    if discrepancies:
        print("\nPossible file tampering detected.")
    elif files_to_check:
        print("\nAll checked files are unmodified.")

def update_command(args):
    """Updates the stored hash for a specific log file."""
    file_path = args.path
    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}")
        return

    hash_file_path = get_hash_file_path(file_path)
    stored_hashes = load_hashes(hash_file_path)

    current_hash = calculate_hash(file_path)
    if current_hash:
        stored_hashes[file_path] = current_hash
        if store_hashes(stored_hashes, hash_file_path):
            print("Hash updated successfully.")

def main():
    parser = argparse.ArgumentParser(description="File Integrity Checker")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Initialize command
    init_parser = subparsers.add_parser("init", help="Initialize and store hashes")
    init_parser.add_argument("path", help="Directory or single log file path")
    init_parser.set_defaults(func=init_command)

    # Check command
    check_parser = subparsers.add_parser("check", help="Check file integrity")
    check_parser.add_argument("path", help="Directory or single log file path to check")
    check_parser.set_defaults(func=check_command)

    # Alternative check command (with -check prefix)
    check_alt_parser = subparsers.add_parser("-check", help="Check file integrity (alternative)")
    check_alt_parser.add_argument("path", help="Directory or single log file path to check")
    check_alt_parser.set_defaults(func=check_command)

    # Update command
    update_parser = subparsers.add_parser("update", help="Update hash for a file")
    update_parser.add_argument("path", help="Single log file path to update")
    update_parser.set_defaults(func=update_command)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()