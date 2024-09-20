# Folder Synchronization Script

This Python script synchronizes the contents of a source folder with a replica folder at regular intervals. It ensures
that files and directories in the source folder are copied or updated in the replica folder, while removing any files or
directories from the replica that do not exist in the source. The script also logs all operations to a specified log
file.

## Features

- **One-way synchronization**: Updates the replica folder based on the contents of the source folder.
- **File comparison by modification time**: Only files with a newer modification time in the source folder are copied to
  the replica.
- **Automatic deletion**: Files and directories in the replica that are no longer present in the source folder are
  deleted.
- **Logging**: Logs all synchronization actions (file updates, deletions, errors) in a specified log file.
- **Periodic synchronization**: Runs synchronization continuously at a set interval.
- **Reliability in deep directories**: Handles synchronization of files and directories at any depth, thanks to the
  usage of os.walk function.

## Requirements

- Python 3.x
- Modules: `os`, `shutil`, `hashlib`, `time`, `logging`, `sys`

These modules are part of Python's standard library, so no external dependencies are needed.

## Usage

To run the script, use the following command:

```bash
python sync_folders.py <source_folder> <replica_folder> <interval> <log_file>

- `<source_folder>`: The path to the source folder to be synchronized.
- `<replica_folder>`: The path to the replica folder that will be updated.
- `<interval>`: The synchronization interval in seconds (e.g., 60 for 1 minute).
- `<log_file>`: The path to the log file where synchronization actions will be recorded().
```

## Author & License

- André Santos Oliveira.
- This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



