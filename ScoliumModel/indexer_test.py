from indexer import Indexer, _lazy_load_pdf

def test_indexer():
    indexer = Indexer()
    assert indexer is not None

async def test_lazy_load_pdf():
    pages = await _lazy_load_pdf("./ScholiumModel/sample_data/DistilBERT.pdf")
    print(pages)


import asyncio

async def main():
    await test_lazy_load_pdf()

asyncio.run(main())
# if __name__ == "__main__":
#     asyncio.run(main())