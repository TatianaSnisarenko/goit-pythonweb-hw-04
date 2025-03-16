import asyncio
import aiopath
import aioshutil
import logging
import argparse

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Async file sorter")
    parser.add_argument("src", type=str, help="Path to source folder")
    parser.add_argument("dst", type=str, help="Path to destination folder")
    return parser.parse_args()


async def read_folder(src: aiopath.AsyncPath, dst: aiopath.AsyncPath):
    """Recursively reads all files in the source folder."""
    tasks = []
    file_count = 0
    files = [item async for item in src.rglob("*") if await item.is_file()]

    for file in files:
        file_count += 1
        tasks.append(copy_file(file, dst))

    if file_count == 0:
        logging.warning("The source folder is empty.")
        return

    await asyncio.gather(*tasks)


async def copy_file(file_path: aiopath.AsyncPath, dst: aiopath.AsyncPath):
    """Copies a file to the corresponding subfolder in the destination folder based on its extension."""
    try:
        extension = file_path.suffix[1:] or "unknown"
        target_folder = dst / extension
        await target_folder.mkdir(parents=True, exist_ok=True)
        target_path = target_folder / file_path.name

        await aioshutil.copy2(file_path, target_path)
        logging.info(f"Copied: {file_path} -> {target_path}")
    except Exception as e:
        logging.error(f"Error copying {file_path}: {e}")


async def main():
    """Main entry point for the script."""
    args = parse_arguments()
    source_path = aiopath.AsyncPath(args.src)
    destination_path = aiopath.AsyncPath(args.dst)

    # Check if the source folder exists and is a directory
    if not await source_path.exists():
        logging.error(f"Source folder does not exist: {source_path}")
        return
    if not await source_path.is_dir():
        logging.error(f"Source path is not a directory: {source_path}")
        return

    try:
        logging.info(
            f"Starting the copying process from: {source_path} to {destination_path}"
        )
        async for _ in source_path.iterdir():
            break
        else:
            await destination_path.mkdir(parents=True, exist_ok=True)
            logging.info("Source folder is empty. Created empty destination folder.")
            return

        await read_folder(source_path, destination_path)
        logging.info("Copying process completed.")
    except (KeyboardInterrupt, SystemExit):
        logging.info("Process interrupted by user.")


if __name__ == "__main__":
    asyncio.run(main())
