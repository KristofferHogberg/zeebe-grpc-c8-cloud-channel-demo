import os

import zeebe_utils


async def main():
    process_instance = await zeebe_utils.run_process_with_result()

    print(f"Process instance result: {process_instance}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
