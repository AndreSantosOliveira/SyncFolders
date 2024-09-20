#  Author: André Santos Oliveira

#  Description: This script synchronizes two folders by copying files from the source folder to the replica folder.
#  It also removes files and directories from the replica that don't exist in the source.
#  The synchronization is performed at regular intervals, specified by the user.
#  The script logs all operations to a file.

# The script takes 4 arguments: source folder path, replica folder path, synchronization interval (in seconds),
# and log file path. Usage: python sync_folders.py <source> <replica> <interval> <log_file>

import os
import shutil
import hashlib
import time
import logging as log
from sys import argv, exit


# Auxiliary functions
def calculate_md5(file_path):
    """Calculates the MD5 hash of a file."""
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        log.error(f"Failed to calculate MD5 for {file_path}: {e}")
        return None


def setup_logging(log_file):
    """Configures the logging module."""
    # Ensure the directory for the log file exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log.basicConfig(filename=log_file, level=log.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


# Main function
def sync_folders(source, replica):
    """Synchronizes the source folder with the replica folder."""
    log.info("Starting synchronization...")
    changes_made = False

    try:
        # Ensure source and replica directories exist
        for folder, name in [(source, "source"), (replica, "replica")]:
            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
                log.info(f"Created {name} directory: {folder}")
                changes_made = True
    except OSError as e:
        log.error(f"Failed to create directories: {replica} '|' {source}. Error: {e}")
        return changes_made

    try:
        # Synchronize all files and directories from source to replica
        for root, dirs, files in os.walk(source):
            relative_path = os.path.relpath(root, source)
            replica_root = os.path.join(str(replica),
                                        str(relative_path) if relative_path != '.' else '')

            # Ensure directories exist in the replica
            for dir_name in dirs:
                try:
                    os.makedirs(os.path.join(replica_root, dir_name), exist_ok=True)
                except OSError as e:
                    log.error(f"Failed to create directory: {replica_root}/{dir_name}. Error: {e}")

            # Copy and update files from source to replica
            for file_name in files:
                source_file = os.path.join(root, file_name)
                replica_file = os.path.join(replica_root, file_name)

                if not os.path.exists(replica_file) or calculate_md5(source_file) != calculate_md5(replica_file):
                    shutil.copy2(str(source_file), str(replica_file))
                    log.info(f"Copied/Updated file from {source_file} to {replica_file}")
                    changes_made = True

        # Remove files and directories in the replica that don't exist in the source
        for root, dirs, files in os.walk(replica):
            source_root = os.path.join(str(source), str(os.path.relpath(root, replica)))

            # Remove files and directories in the replica that don't exist in the source
            for name in files + dirs:
                replica_path = os.path.join(root, name)
                source_path = os.path.join(source_root, name)
                try:
                    if not os.path.exists(source_path):
                        if os.path.isdir(replica_path):
                            shutil.rmtree(replica_path)
                            log.info(f"Deleted directory: {replica_path}")
                        else:
                            os.remove(replica_path)
                            log.info(f"Deleted file: {replica_path}")
                        changes_made = True
                except OSError as e:
                    log.error(f"Failed to delete {replica_path}. Error: {e}")

    except Exception as e:
        log.error(f"Error during synchronization: {e}")

    if not changes_made:
        log.info("No changes made in synchronization.")

    log.info("Synchronization completed.\n")
    print("Synchronization completed.\nAwaiting interval...\n")


def main():
    if len(argv) < 5:
        print("Usage: python sync_folders.py <source> <replica> <interval> <log_file>")
        exit(1)

    source_folder, replica_folder, sync_interval, log_file = argv[1], argv[2], int(argv[3]), argv[4]
    setup_logging(log_file)

    while True:
        try:
            sync_folders(source_folder, replica_folder)
        except Exception as e:
            log.error(f"Error during synchronization: {e}")
        time.sleep(sync_interval)


if __name__ == "__main__":
    main()
