import json, os

P = r"L:/Project/src/apps/Fleeting-Bloom-Chronicles/data/pages-map.json"
m = json.load(open(P, encoding="utf-8"))
pages = m["pages"]

def find(author):
    for i, e in enumerate(pages):
        if e.get("author") == author:
            return i
    return -1

# ---- 任务1：张心茹 -2.jpg 为背景图，标记 noZoom（不做放大热区）----
for e in pages:
    if e.get("author") == "张心茹":
        for md in e.get("media", []):
            if md["file"].endswith("-2.jpg"):
                md["noZoom"] = True
                print("已标记不放大:", md["file"].split("/")[-1])

# ---- 任务2：黄伟超放到范柏唱后面；彭岑放到张有强后面 ----
fan = find("范柏唱")
huang = find("黄伟超")
assert fan >= 0 and huang >= 0, "找不到范柏唱/黄伟超"
huang_e = pages.pop(huang)
pages.insert(fan + 1, huang_e)          # 范柏唱之后紧邻

zhang = find("张有强")
peng = find("彭岑")
assert zhang >= 0 and peng >= 0, "找不到张有强/彭岑"
peng_e = pages.pop(peng)
pages.insert(zhang + 1, peng_e)          # 张有强之后紧邻

m["pages"] = pages

# 校验顺序
order = [e["author"] for e in pages]
print("\n范柏唱后:", order[order.index("范柏唱"):order.index("范柏唱")+2])
print("张有强后:", order[order.index("张有强"):order.index("张有强")+2])
print("总数:", len(pages))

json.dump(m, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("\n已写回 pages-map.json")
