# 🛡️ File Integrity Checker

A simple Python tool to verify the integrity of application log files and detect tampering. This tool uses cryptographic hashing (SHA-256) to ensure that no unauthorized changes have been made to your log files.

## ✨ Features

* ✅ Accepts a directory or a single log file as input.
* 🔒 Utilizes SHA-256 hashing algorithm for robust integrity checks.
* 💾 Stores initial file hashes securely for comparison.
* 🔍 Detects and reports discrepancies indicating potential file tampering.
* 🚦 Clearly reports the status of each checked file (Modified or Unmodified).
* 🔄 Allows for manual re-initialization of log file integrity.
* ✍️ Supports updating the stored hash for a specific file.

## 🚀 Getting Started

1.  **Download the script:** You can download the `integrity-check.py` file directly from your repository or clone the entire repository:

    ```
    git clone https://github.com/Anamelechi/file-integrity-checker
    cd file-integrity-checker
    ```

2.  **Make the script executable:**

    ```
    chmod +x integrity-check.py
    ```

## 🛠️ Usage

The tool can be used with the following commands:

### ⚙️ Initialization

To initialize the integrity check for a directory or a single file, use the `init` command:

```bash
./integrity-check.py init <path_to_directory_or_file>
```
### Example:

```bash
./integrity-check.py init /var/log  # Initializes all log files in the directory
> Hashes stored successfully.

./integrity-check.py init /var/log/syslog # Initializes a single log file
> Hashes stored successfully.
```
### 👀 Checking Integrity
To check the integrity of a directory or a single file against the stored hashes, use the check or -check command:

```bash 
./integrity-check.py check <path_to_directory_or_file>
```
Alternatively:

```bash
./integrity-check.py -check <path_to_directory_or_file>
```
### Examples:

```bash
./integrity-check.py check /var/log/syslog
> Status for /var/log/syslog: Modified (Hash mismatch)

./integrity-check.py -check /var/log/auth.log
> Status for /var/log/auth.log: Unmodified

./integrity-check.py check /var/log/  # Checks all files in the directory
> Status for /var/log/file1.log: Unmodified
> Status for /var/log/file2.log: Modified (Hash mismatch)
> Status for /var/log/new_file.log: New file (Not in initial hash list)
> Possible file tampering detected.
```
### 🔄 Updating Hash
If you have verified that changes to a log file are legitimate and you want to update the stored hash, use the update command:

```bash
./integrity-check.py update <path_to_log_file>
```
### Example:

```

./integrity-check.py update /var/log/syslog
> Hash updated successfully.
```

### ⚠️ Important Considerations

 - 🔒 Security of Hash File: The .file_hashes.json file is critical. Ensure it's protected from unauthorized access or modification.
 - ⏱️ Performance: For very large log files or directories with many files, the initial hashing and checks might take some time.
 - 🔄 Log Rotation: Be aware that log rotation mechanisms might rename or replace log files, leading to "New file" or "Modified" statuses.
 - 🔑 Permissions: Ensure the script has the necessary permissions to read the log files and write to the location where the hash file is stored. You might need to use sudo in some cases.
 - ❗ False Positives: Legitimate log rotations or application updates can change log files. Use the update command after verifying such changes.

### 🤝 Contributing
 Feel free to contribute to the project by submitting pull requests or reporting issues.

📜 [License](LICENSE)

✍️ Author
[Anamelechi](https://github.com/Anamelechi)

Part of [Roadmap.sh](https://roadmap.sh/projects/file-integrity-checker) DevOps projects












