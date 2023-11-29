import os

import zeebe_utils


async def main():
    # process_instance = await zeebe_utils.run_process_with_result()
    topology = await zeebe_utils.get_topology()

    # print(f"Process instance result: {process_instance}")
    print(f"Topology: {topology}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
