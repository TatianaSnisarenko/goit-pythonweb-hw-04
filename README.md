# Async File Sorter

This program asynchronously copies files from a source folder to a destination folder, organizing them into subfolders based on file extensions.

## Requirements

Before running the program, make sure you have all the necessary dependencies installed. You can install them using the `requirements.txt` file.

```sh
pip install -r requirements.txt
```

## Usage

To run the program, use the following command:

```sh
python main.py <source_folder> <destination_folder>
```

where:

- `<source_folder>` is the path to the source folder from which files will be copied.
- `<destination_folder>` is the path to the destination folder where files will be copied.

## Example

Suppose you have a folder `from_folder` with files that you want to copy to the `to_folder`. Use the following command:

```sh
python main.py from_folder to_folder
```

## Logging

The program logs the file copying process. The logs include information about the start and end of the copying process, as well as each copied file.

## Error Handling

- If the source folder does not exist or is not a directory, the program will output an appropriate error message and terminate.
- If the source folder is empty, the program will create an empty destination folder and terminate with an appropriate message in the logs.

## Termination

The program handles user interruptions (e.g., pressing `Ctrl+C`) and logs an appropriate message before terminating.
