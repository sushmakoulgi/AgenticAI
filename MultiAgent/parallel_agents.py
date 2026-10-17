#demo
import asyncio
import time

async def run_agent(name,time):
    print(f"Entering {name} ")
    await asyncio.sleep(time)
    print(f"Exsiting {name}")


async def run_sequential():
    start=time.perf_counter()

    await run_agent("Research",3)
    await run_agent("Techonology",2)
    await run_agent("Marketing",4)

    end=time.perf_counter()-start


    print(f"time of execution {end:.2f}")

async def run_parallel():
    start=time.perf_counter()

    await asyncio.gather(
     run_agent("Research",3),
     run_agent("Techonology",2),
     run_agent("Marketing",4)

    )
   
    end=time.perf_counter()-start


    print(f"time of execution {end:.2f}")


async def main():
    print("Running Sequential")
    await run_sequential()
    print("Running in Parallel")
    await run_parallel()


if __name__ =="__main__":
    asyncio.run(main())
