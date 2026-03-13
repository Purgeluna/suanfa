#第五天  Python 异步 + requests/tqdm 写异步请求、进度条可视化
'''
# 在一个线程中，CPU执行代码的速度极快，然而，一旦遇到IO操作，如读写文件、发送网络数据时，就需要等待IO操作完成，才能继续进行下一步操作。这种情况称为同步IO。
# 在IO操作的过程中，当前线程被挂起，而其他需要CPU执行的代码就无法被当前线程执行了。
#
# 因为一个IO操作就阻塞了当前线程，导致其他代码无法执行，所以我们必须使用多线程或者多进程来并发执行代码，为多个用户服务。每个用户都会分配一个线程，如果遇到IO导致线程被挂起，其他用户的线程不受影响。
# 多线程和多进程的模型虽然解决了并发问题，但是系统不能无上限地增加线程。由于系统切换线程的开销也很大，所以，一旦线程数量过多，CPU的时间就花在线程切换上了，真正运行代码的时间就少了，结果导致性能严重下降。

# 要解决的问题 ;CPU高速执行能力和IO设备的龟速严重不匹配
# 解决方法1：多线程多进程，但线程数量过多会导致性能下降
# 解决方法2：异步IO，单线程通过事件循环机制来实现并发

# 什么是异步IO： 当代码需要执行一个耗时的IO操作时，它只发出IO指令，并不等待IO结果，然后就去执行其他代码了。一段时间后，当IO返回结果时，再通知CPU进行处理。

'普通顺序写出的代码:'

read_text=open('test.txt','r').read()
result=read_text.read()   # <== 线程停在此处等待IO操作结果
print(result)


'''
'''
'异步IO写出的代码:'
'''
import threading

# loop=get_envent_loop()  # 获取事件循环对象
# while True:
#     event=loop.get_event()  # 获取事件
#     process_evente(event)  # 处理事件
'''
异步IO模型需要一个消息循环，在消息循环中，主线程不断地重复“读取消息-处理消息”这一过程：最经典的例子中左面应用程序开发,
个GUI程序的主线程就负责不停地读取消息并处理消息。所有的键盘、鼠标等消息都被发送到GUI程序的消息队列中，然后由GUI程序的主线程处理。


协程:

子程序，或者称为函数，在所有语言中都是层级调用，比如A调用B，B在执行过程中又调用了C，C执行完毕返回，B执行完毕返回，最后是A执行完毕。
所以子程序调用是通过栈实现的，一个线程就是执行一个子程序。

协程看上去也是子程序，但执行过程中，在子程序内部可中断，然后转而执行别的子程序，在适当的时候再返回来接着执行。

协程极高的执行效率。因为子程序切换不是线程切换，而是由程序自身控制，因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显。

第二大优势就是不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。

Python对协程的支持是通过generator实现的:

asyncio ,模块内部实现了EventLoop，把需要执行的协程扔到EventLoop中执行，就实现了异步IO。

'''
# import asyncio
#
# async def hello():
#     print("Hello world!")
#     # 异步调用asyncio.sleep(1):
#     await asyncio.sleep(1)
#     print("Hello again!")
#
# asyncio.run(hello())
'''
Hello world!
Hello again!
'''

'''
# 传入name参数:
async def hello(name):
    # 打印name和当前线程:
    print("Hello %s! (%s)" % (name, threading.current_thread))
    # 异步调用asyncio.sleep(1):
    await asyncio.sleep(1)
    print("Hello %s again! (%s)" % (name, threading.current_thread))
    return name
async def main():
    L = await asyncio.gather(hello("Bob"), hello("Alice"))
    print(L)

asyncio.run(main())

# requests库是一个基于HTTP协议的第三方库，提供了更简单易用的API来发送HTTP请求和处理响应。它支持多种HTTP方法，如GET、POST、PUT、DELETE等，并且可以轻松地处理URL参数、请求头、请求体等。
import requests

response=requests.get('https://www.baidu.com')                         #发送GET请求
# response2=requests.post('https://www.baidu.com',data={'key':'value'})    #提交数据

print(response.status_code)  #获取响应状态码
print(response.text)         #获取响应内容
# print(response.json())         #获取响应的JSON数据
但是 requests库是一个同步的HTTP库，在发送请求时会阻塞当前线程，直到收到响应为止。如果需要发送大量的HTTP请求，
或者需要在请求过程中执行其他任务，就需要使用异步HTTP库，如aiohttp。

进度条库 tqdm
from tqdm import tqdm
import time

for i in tqdm(range(100),desc='处理中'):

    time.sleep(0.1)  # 模拟处理过程
import requests
urls = [f"https://httpbin.org/get?num={i}" for i in range(10)]

for url in tqdm(urls, desc="请求进度"):
    response = requests.get(url)
'''

# 综合实战

import asyncio
import aiohttp
import logging
import csv
import json
from typing import List, Dict, Optional
from tqdm import tqdm
from datetime import datetime
from collections import Counter

# ====================== 1. 配置项 ======================
# 日志配置（记录过程和错误）
import asyncio
import aiohttp
import logging
import csv
import json
from typing import List, Dict, Optional
from tqdm import tqdm
from datetime import datetime
from collections import Counter

# ====================== 1. 配置项 ======================
# 日志配置（记录过程和错误）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # 输出到控制台
)
logger = logging.getLogger(__name__)

# API配置
TEST_API_URL = "https://httpbin.org/get"  # 公开测试API
BATCH_SIZE = 10  # 要采集的样本数量
MAX_CONCURRENT = 5  # 最大异步并发数
TIMEOUT = 10  # 请求超时时间（秒）

# 文件输出路径
RAW_DATA_PATH = "raw_user_data.json"  # 原始数据文件
CLEANED_DATA_PATH = "cleaned_user_data.csv"  # 清洗后数据
STATS_PATH = "user_stats.csv"  # 统计结果文件


# ====================== 2. 异步数据采集 ======================
async def fetch_user_data(
        session: aiohttp.ClientSession,
        user_id: int,
        pbar: tqdm
) -> Optional[Dict]:
    """异步采集单个用户数据（模拟）"""
    try:
        # 构造带参数的请求URL（模拟不同用户）
        params = {
            "user_id": user_id,
            "region": ["北京", "上海", "广州", "深圳", "成都"][user_id % 5],  # 模拟地区
            "register_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        async with session.get(TEST_API_URL, params=params, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as resp:
            if resp.status != 200:
                logger.error(f"用户{user_id}请求失败，状态码：{resp.status}")
                return None

            data = await resp.json()
            # 提取关键字段（模拟真实场景的数据提取）
            raw_data = {
                "user_id": user_id,
                "region": data["args"]["region"],
                "register_time": data["args"]["register_time"],
                "ip": data.get("origin", ""),
                "url": data.get("url", "")
            }
            return raw_data
    except Exception as e:
        logger.error(f"用户{user_id}采集异常：{str(e)}")
        return None
    finally:
        pbar.update(1)  # 无论成败，更新进度条


async def batch_fetch_data() -> List[Dict]:
    """批量异步采集数据"""
    logger.info(f"开始采集{MAX_CONCURRENT}个用户数据...")

    # 初始化进度条
    pbar = tqdm(total=BATCH_SIZE, desc="数据采集进度", unit="条")

    # 创建异步会话（复用连接）
    async with aiohttp.ClientSession() as session:
        # 生成所有采集任务
        tasks = [fetch_user_data(session, i + 1, pbar) for i in range(BATCH_SIZE)]
        # 执行异步任务
        results = await tqdm.asyncio.tqdm.gather(*tasks, desc="异步执行中")

    pbar.close()
    # 过滤掉采集失败的数据
    valid_data = [item for item in results if item is not None]
    logger.info(f"采集完成，有效数据{len(valid_data)}/{BATCH_SIZE}条")

    # 保存原始数据（便于排查问题）
    with open(RAW_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(valid_data, f, ensure_ascii=False, indent=2)
    logger.info(f"原始数据已保存至：{RAW_DATA_PATH}")

    return valid_data


# ====================== 3. 数据清洗 ======================
def clean_user_data(raw_data: List[Dict]) -> List[Dict]:
    """清洗用户数据：去重、格式标准化、缺失值处理"""
    logger.info("开始数据清洗...")
    cleaned_data = []
    seen_user_ids = set()  # 用于去重

    # 进度条展示清洗进度
    for item in tqdm(raw_data, desc="数据清洗进度", unit="条"):
        # 1. 去重（根据user_id）
        if item["user_id"] in seen_user_ids:
            logger.warning(f"用户{item['user_id']}数据重复，已跳过")
            continue
        seen_user_ids.add(item["user_id"])

        # 2. 缺失值处理
        cleaned_item = {
            "user_id": item["user_id"],
            "region": item.get("region", "未知地区"),  # 缺失值填充
            # 时间格式标准化（转为YYYY-MM-DD）
            "register_date": item["register_time"].split(" ")[0] if item.get("register_time") else "未知时间",
            "ip": item.get("ip", "未知IP").strip()  # 去除首尾空格
        }

        # 3. 数据校验（确保地区是有效值）
        valid_regions = ["北京", "上海", "广州", "深圳", "成都"]
        if cleaned_item["region"] not in valid_regions:
            cleaned_item["region"] = "其他地区"

        cleaned_data.append(cleaned_item)

    logger.info(f"数据清洗完成，清洗后数据{len(cleaned_data)}条")
    return cleaned_data


# ====================== 4. 数据统计 & 导出 ======================
def export_data(cleaned_data: List[Dict]):
    """导出清洗后数据和统计结果"""
    # 1. 导出清洗后的数据到CSV
    logger.info("开始导出清洗后数据...")
    csv_headers = ["user_id", "region", "register_date", "ip"]
    with open(CLEANED_DATA_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(cleaned_data)
    logger.info(f"清洗后数据已导出至：{CLEANED_DATA_PATH}")

    # 2. 统计各地区用户数
    logger.info("开始统计数据指标...")
    region_counter = Counter([item["region"] for item in cleaned_data])
    stats_data = [{"region": k, "user_count": v} for k, v in region_counter.items()]

    # 3. 导出统计结果
    with open(STATS_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["region", "user_count"])
        writer.writeheader()
        writer.writerows(stats_data)
    logger.info(f"统计结果已导出至：{STATS_PATH}")

    # 打印统计摘要
    logger.info("\n===== 数据统计摘要 =====")
    for region, count in region_counter.most_common():
        logger.info(f"{region}: {count}人")


# ====================== 5. 主流程入口 ======================
def main():
    """端到端数据处理主流程"""
    try:
        # 适配Windows异步环境
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        # 步骤1：异步采集数据
        raw_data = asyncio.run(batch_fetch_data())
        if not raw_data:
            logger.error("无有效采集数据，程序终止")
            return

        # 步骤2：数据清洗
        cleaned_data = clean_user_data(raw_data)

        # 步骤3：数据导出 & 统计
        export_data(cleaned_data)

        logger.info("\n全流程执行完成！")

    except KeyboardInterrupt:
        logger.error("\n用户中断程序执行")
    except Exception as e:
        logger.error(f"程序执行异常：{str(e)}", exc_info=True)


if __name__ == "__main__":
    # 安装依赖（首次运行需执行）
    # pip install aiohttp tqdm
    main()


