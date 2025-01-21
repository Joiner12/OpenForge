import asyncio


async def fetch_data():
    print("开始获取数据...")
    await asyncio.sleep(2)  # 模拟一个耗时的 I/O 操作
    print("数据获取完成!")
    return {"data": "some data"}


async def main():
    result = await fetch_data()
    print(result)


# 运行异步主函数
asyncio.run(main())
