#!/usr/bin/env python3
"""Build a classroom PPT for 八年级上册 第一单元 第3课."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

FILE = "/Users/zengweihao/Desktop/信息技术/out/第3课_探秘农业物联网云平台.pptx"

FONT = "Microsoft YaHei"
FONT_LATIN = "Calibri"

DARK = "1B3A28"
PAPER = "F6F3EA"
PRIMARY = "2C5F2D"
MOSS = "7BA05B"
GOLD = "C4A35A"
WHEAT = "E8D9A8"
TERR = "B85042"
TEXT = "2D2D2D"
MUTED = "5E735F"
WHITE = "FFFFFF"
CARD = "FFFFFF"
PALE = "E7F0DC"
CREAM = "FBF8F1"

S = 0
TOTAL = 28


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    r = subprocess.run(["officecli", *args], check=False, text=True, capture_output=True)
    if check and r.returncode != 0:
        print("CMD", " ".join(args[:8]))
        print(r.stdout)
        print(r.stderr)
        raise SystemExit(r.returncode)
    return r


def batch(ops: list[dict]) -> None:
    if not ops:
        return
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(ops, f, ensure_ascii=False)
    try:
        r = subprocess.run(
            ["officecli", "batch", FILE, "--input", path, "--json"],
            check=False,
            text=True,
            capture_output=True,
        )
        if r.returncode != 0:
            print(r.stdout)
            print(r.stderr)
            raise SystemExit(f"batch failed on slide {S}")
        data = json.loads(r.stdout) if r.stdout.strip().startswith("{") else {}
        if data.get("data", {}).get("atomicRolledBack") or data.get("atomicRolledBack"):
            print(r.stdout)
            raise SystemExit(f"batch rolled back on slide {S}")
    finally:
        os.remove(path)


def add_slide(bg: str, name: str) -> None:
    global S
    S += 1
    r = run(
        "add",
        FILE,
        "/",
        "--type",
        "slide",
        "--prop",
        "layout=blank",
        "--prop",
        f"background={bg}",
        "--prop",
        f"name={name}",
        "--prop",
        "transition=fade",
    )
    print(f"slide {S:02d}  {name}")


def shp(**props: str) -> dict:
    return {"command": "add", "parent": f"/slide[{S}]", "type": "shape", "props": props}


def chart(**props: str) -> dict:
    return {"command": "add", "parent": f"/slide[{S}]", "type": "chart", "props": props}


def connector(a: str, b: str, **extra: str) -> dict:
    props = {
        "from": f"/slide[{S}]/shape[@name={a}]",
        "to": f"/slide[{S}]/shape[@name={b}]",
        "shape": extra.get("shape", "straight"),
        "color": extra.get("color", PRIMARY),
        "tailEnd": "triangle",
        "lineWidth": extra.get("lineWidth", "1.75pt"),
    }
    return {"command": "add", "parent": f"/slide[{S}]", "type": "connector", "props": props}


def T(
    name: str,
    text: str,
    x: float,
    y: float,
    w: float,
    h: float,
    size: int = 18,
    bold: bool = False,
    color: str = TEXT,
    align: str = "left",
    valign: str = "top",
    fill: str = "none",
    preset: str | None = None,
    margin: str | None = None,
    italic: bool = False,
) -> dict:
    p = {
        "name": name,
        "text": text,
        "x": f"{x}cm",
        "y": f"{y}cm",
        "width": f"{w}cm",
        "height": f"{h}cm",
        "font": FONT,
        "font.ea": FONT,
        "font.latin": FONT_LATIN,
        "size": str(size),
        "color": color,
        "align": align,
        "valign": valign,
        "fill": fill,
        "line": "none",
        "autoFit": "none",
    }
    if bold:
        p["bold"] = "true"
    if italic:
        p["italic"] = "true"
    if preset:
        p["preset"] = preset
    p["margin"] = margin or "0.05cm"
    # CJK line-box is taller than Latin; grow single-line labels so glyphs are not clipped.
    if "\n" not in text:
        need = round(size * 0.052 + 0.32, 2)
        if h < need:
            h = need
            p["height"] = f"{h}cm"
    return shp(**p)


def box(
    name: str,
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str,
    preset: str = "roundRect",
) -> dict:
    p = {
        "name": name,
        "preset": preset,
        "fill": fill,
        "line": "none",
        "x": f"{x}cm",
        "y": f"{y}cm",
        "width": f"{w}cm",
        "height": f"{h}cm",
    }
    if preset == "roundRect":
        p["adj"] = "adj:val 8000"
    return shp(**p)


def chrome(dark: bool = False) -> list[dict]:
    band = GOLD if dark else PRIMARY
    foot_c = "A8C4A0" if dark else MUTED
    num_fill = GOLD if dark else PRIMARY
    num_c = DARK if dark else WHITE
    return [
        box("Band", 0, 0, 0.36, 19.05, band, preset="rect"),
        T(
            "Footer",
            "教育科学出版社《信息科技 八年级上册》  ·  第一单元第3课",
            1.5,
            17.42,
            26.8,
            0.9,
            size=11,
            color=foot_c,
            valign="middle",
        ),
        box("PgBg", 31.2, 17.28, 1.4, 1.4, num_fill, preset="ellipse"),
        T(
            "PgNum",
            f"{S:02d}",
            31.2,
            17.28,
            1.4,
            1.4,
            size=12,
            bold=True,
            color=num_c,
            align="center",
            valign="middle",
        ),
    ]


def title(text: str, dark: bool = False) -> dict:
    return T(
        "Title",
        text,
        1.5,
        0.72,
        29.3,
        1.85,
        size=36,
        bold=True,
        color=WHITE if dark else PRIMARY,
        valign="middle",
    )


def kicker(text: str, dark: bool = False) -> dict:
    return T(
        "Kicker",
        text,
        1.5,
        0.38,
        20,
        0.5,
        size=14,
        color=GOLD if dark else MOSS,
        bold=True,
        valign="middle",
    )


def finish(ops: list[dict], note: str) -> None:
    ops.append({"command": "add", "parent": f"/slide[{S}]", "type": "notes", "props": {"text": note}})
    batch(ops)


def slide_cover() -> None:
    add_slide(DARK, "封面")
    ops = [
        box("GoldBar", 0, 0, 0.42, 19.05, GOLD, preset="rect"),
        T(
            "Ghost",
            "03",
            22.5,
            11.8,
            10.5,
            6.4,
            size=120,
            bold=True,
            color="2A4A36",
            align="right",
            valign="bottom",
        ),
        T(
            "Series",
            "第一单元  认识物联网  ·  探秘智慧农业示范区",
            2.1,
            3.4,
            28,
            0.7,
            size=18,
            color=WHEAT,
            valign="middle",
        ),
        T(
            "Main",
            "探秘农业物联网云平台",
            2.1,
            4.5,
            29,
            2.4,
            size=44,
            bold=True,
            color=WHITE,
            valign="middle",
        ),
        T(
            "Sub",
            "数据怎样离开温室，走进云端",
            2.1,
            7.1,
            28,
            1.0,
            size=22,
            color=GOLD,
            valign="middle",
        ),
        box("MetaBg", 2.1, 14.4, 24.2, 2.5, "163224", preset="roundRect"),
        T(
            "Meta",
            "教育科学出版社  ·  信息科技 八年级上册\n教材第14–18页  ·  建议课时 1 课时",
            2.4,
            14.55,
            23.6,
            2.2,
            size=18,
            color=WHITE,
            valign="middle",
        ),
    ]
    finish(
        ops,
        "出示课题。先不要讲协议名词。问：离开温室以后，传感器测到的数去了哪里？谁来决定要不要浇水？把学生猜想记在黑板右侧，课末回看。",
    )


def slide_position() -> None:
    add_slide(PAPER, "本课在单元中的位置")
    cards = [
        ("01", "第1课", "认识智慧农业", "知道智慧农业能做什么"),
        ("02", "第2课", "探索智慧温室大棚", "知道数据从哪些设备来"),
        ("03", "第3课", "探秘农业物联网云平台", "知道数据怎样传输与处理"),
    ]
    xs = [1.5, 12.08, 22.66]
    ops = chrome() + [title("本课在单元中的位置")]
    for i, (num, lesson, name, goal) in enumerate(cards):
        fill = PRIMARY if i == 2 else CARD
        tc = WHITE if i == 2 else TEXT
        mc = GOLD if i == 2 else MOSS
        gc = WHEAT if i == 2 else MUTED
        x = xs[i]
        ops += [
            box(f"C{i}", x, 3.15, 9.58, 7.8, fill),
            T(f"N{i}", num, x + 0.45, 3.5, 8.6, 1.3, size=28, bold=True, color=mc),
            T(f"L{i}", lesson, x + 0.45, 5.0, 8.6, 0.8, size=18, color=gc if i == 2 else MUTED),
            T(f"A{i}", name, x + 0.45, 6.0, 8.6, 2.4, size=24, bold=True, color=tc),
            T(f"G{i}", goal, x + 0.45, 9.0, 8.6, 4.6, size=18, color=tc),
        ]
    finish(
        ops,
        "用三张卡片把单元线索说清楚：第1课看功能，第2课看设备，第3课看数据如何汇入云平台。强调本课学习成果仍要回到单元思维导图。",
    )


def slide_goals() -> None:
    add_slide(PAPER, "本课学习目标")
    items = [
        ("01", "说清作用", "能用自己的话说明农业物联网云平台做什么：采集、显示、存储、分析、报警与控制。"),
        ("02", "画出路径", "能按顺序说出：传感器采集，经有线或无线设备上传，到达云平台。"),
        ("03", "比较协议", "能举出 ZigBee、MQTT 等协议，并说出它们主要解决哪一类通信问题。"),
        ("04", "完成导图", "在“智慧农业示范区”思维导图中，补上“农业物联网云平台”分支。"),
    ]
    ops = chrome() + [title("本课学习目标")]
    ys = [3.1, 6.45, 9.8, 13.15]
    for i, (num, head, body) in enumerate(items):
        y = ys[i]
        ops += [
            box(f"B{i}", 1.5, y, 30.7, 3.1, CARD),
            box(f"N{i}", 1.9, y + 0.7, 1.7, 1.7, PRIMARY, preset="ellipse"),
            T(f"NT{i}", num, 1.9, y + 0.7, 1.7, 1.7, size=14, bold=True, color=WHITE, align="center", valign="middle"),
            T(f"H{i}", head, 4.0, y + 0.35, 27.4, 0.9, size=22, bold=True, color=PRIMARY, valign="middle"),
            T(f"BD{i}", body, 4.0, y + 1.3, 27.4, 1.5, size=18, color=TEXT, valign="middle"),
        ]
    finish(
        ops,
        "四项目标对应教材：云平台作用、上传路径、通信协议、思维导图。告诉学生：这节课结束时，要用证据解释“远处的水阀怎么知道温室缺水”。",
    )


def slide_focus() -> None:
    add_slide(PAPER, "走进网络中控室")
    ops = chrome() + [
        title("走进网络中控室"),
        box("Q", 1.5, 3.05, 15.2, 4.3, PRIMARY),
        T("QT", "聚焦", 1.95, 3.3, 14.3, 0.7, size=16, bold=True, color=GOLD),
        T(
            "QB",
            "离开温室大棚，走进网络中控室。屏幕上的数字在变化——这些数据从哪里来，又要去哪里？",
            1.95,
            4.1,
            14.3,
            2.9,
            size=20,
            color=WHITE,
        ),
        box("T1", 1.5, 7.6, 15.2, 4.3, CARD),
        T("T1H", "本课要弄清的事", 1.95, 7.85, 14.3, 0.7, size=18, bold=True, color=PRIMARY),
        T(
            "T1B",
            "云平台怎样接收和处理数据\n设备之间靠什么约定交换消息\n如何把本课关键词写进思维导图",
            1.95,
            8.65,
            14.3,
            2.9,
            size=18,
            color=TEXT,
        ),
        box("ChartCard", 17.0, 3.05, 15.2, 13.0, CARD),
        T("CH", "中控室里可能看到的变化", 17.4, 3.25, 14.4, 0.7, size=18, bold=True, color=PRIMARY),
        T("CS", "示例曲线，只用于观察趋势", 17.4, 15.35, 14.4, 0.5, size=12, color=MUTED),
        chart(
            name="SoilChart",
            chartType="line",
            categories="08:00,09:00,10:00,11:00,12:00",
            **{
                "series1.name": "土壤湿度示数",
                "series1.values": "48,42,36,30,26",
                "series1.color": PRIMARY,
            },
            x="17.35cm",
            y="4.1cm",
            width="14.5cm",
            height="10.9cm",
            title="一号棚土壤湿度示数",
            autotitledeleted="false",
            axismin="0",
            axismax="60",
            showlegend="false",
        ),
    ]
    finish(
        ops,
        "读聚焦段。右侧曲线是课堂示意，不是某基地实测。问：数字变小说明什么？谁先发现？管理员不在棚里时，怎样及时知道？转入数据上传。",
    )


def slide_path() -> None:
    add_slide(PAPER, "数据从传感器到云平台")
    labels = [
        ("采集", "传感器测温度、\n湿度、光照"),
        ("汇聚", "节点或网关\n收集现场数据"),
        ("传输", "有线或无线网络\n把数据送出去"),
        ("入云", "农业物联网\n云平台接收处理"),
    ]
    xs = [1.5, 9.55, 17.6, 25.65]
    ops = chrome() + [
        title("数据从传感器到云平台"),
        T(
            "Lead",
            "智能传感器采集的数据，要经过物联网设备，才能到达云平台。",
            1.5,
            2.7,
            30.7,
            0.8,
            size=18,
            color=MUTED,
            valign="middle",
        ),
    ]
    for i, (h, b) in enumerate(labels):
        x = xs[i]
        ops += [
            box(f"Step{i+1}", x, 4.4, 6.7, 6.3, PRIMARY if i % 2 == 0 else CARD),
            T(
                f"Num{i+1}",
                f"{i+1:02d}",
                x + 0.4,
                4.7,
                5.9,
                1.2,
                size=28,
                bold=True,
                color=GOLD if i % 2 == 0 else MOSS,
            ),
            T(
                f"H{i+1}",
                h,
                x + 0.4,
                6.1,
                5.9,
                1.2,
                size=24,
                bold=True,
                color=WHITE if i % 2 == 0 else PRIMARY,
            ),
            T(
                f"B{i+1}",
                b,
                x + 0.4,
                7.6,
                5.9,
                4.4,
                size=18,
                color=WHITE if i % 2 == 0 else TEXT,
            ),
        ]
    ops += [
        connector("Step1", "Step2"),
        connector("Step2", "Step3"),
        connector("Step3", "Step4"),
        T(
            "FootNote",
            "网关不是每套系统都必须单独出现。具备联网能力的终端，也可以直接把数据发到服务器。",
            1.5,
            13.3,
            30.7,
            3.7,
            size=18,
            color=TEXT,
            fill=PALE,
            preset="roundRect",
            valign="middle",
            margin="0.35cm",
        ),
    ]
    finish(
        ops,
        "请两位学生用“先……再……然后……”说出路径。纠正两种误解：1）传感器自己把水浇了；2）所有系统都必须经过独立网关。强调云平台是数据汇合的地方。",
    )


def slide_devices_quiz() -> None:
    add_slide(PAPER, "三类常见物联网设备")
    cards = [
        ("设备 A", "常见于家庭和教室联网", "负责把终端接入无线局域网"),
        ("设备 B", "距离近、体积小", "适合鼠标、耳机、传感器近距连接"),
        ("设备 C", "像一座小型调度站", "汇集多种设备，再与平台通信"),
    ]
    xs = [1.5, 12.08, 22.66]
    ops = chrome() + [
        title("三类常见物联网设备"),
        T(
            "Lead",
            "先根据描述判断：这类设备通常叫什么？写下你的名称，再听同学的理由。",
            1.5,
            2.7,
            30.7,
            0.8,
            size=18,
            color=MUTED,
            valign="middle",
        ),
    ]
    for i, (h, a, b) in enumerate(cards):
        x = xs[i]
        ops += [
            box(f"C{i}", x, 3.8, 9.58, 10.5, CARD),
            box(f"Top{i}", x, 3.8, 9.58, 1.15, GOLD, preset="rect"),
            T(f"H{i}", h, x + 0.4, 3.85, 8.8, 1.05, size=20, bold=True, color=DARK, align="center", valign="middle"),
            T(f"A{i}", a, x + 0.45, 5.3, 8.7, 2.4, size=18, color=TEXT),
            T(f"B{i}", b, x + 0.45, 7.8, 8.7, 3.0, size=18, color=PRIMARY, bold=True),
            T(f"Blank{i}", "我的命名：________", x + 0.45, 11.4, 8.7, 2.2, size=18, color=MUTED, valign="middle"),
        ]
    finish(
        ops,
        "对应教材第14页“做一做”。不要立刻给标准答案。鼓励学生用生活经验命名：路由器、蓝牙适配器、智能网关/控制中心都可以讨论。下一页给课堂参考名称。",
    )


def slide_devices_key() -> None:
    add_slide(PAPER, "设备名称参考")
    cards = [
        ("无线网络连接", "无线路由器", "把计算机、手机、物联网终端接入无线局域网，再通向更大的网络。"),
        ("近距离无线连接", "蓝牙等近距模块", "适合短距离、低功耗的设备互连，例如传感器与附近终端。"),
        ("智能家居控制中心", "智能网关", "汇集多种协议的设备，完成转发、转换，并与云平台通信。"),
    ]
    xs = [1.5, 12.08, 22.66]
    ops = chrome() + [title("设备名称参考")]
    for i, (kind, name, body) in enumerate(cards):
        x = xs[i]
        ops += [
            box(f"C{i}", x, 3.15, 9.58, 8.2, CARD),
            T(f"K{i}", kind, x + 0.45, 3.5, 8.7, 0.8, size=16, color=MOSS, bold=True),
            T(f"N{i}", name, x + 0.45, 4.5, 8.7, 2.4, size=24, bold=True, color=PRIMARY),
            T(f"B{i}", body, x + 0.45, 7.2, 8.7, 6.8, size=18, color=TEXT),
        ]
    finish(
        ops,
        "参考名称对应教材插图功能，不是唯一商标名。强调：同一功能在农场里可能叫农业网关。点明三者分别服务“接入网络”“近距连接”“汇聚转发”。",
    )


def slide_platform_role() -> None:
    add_slide(PAPER, "云平台的核心作用")
    rows = [
        ("采集", "接收温度、湿度、光照等环境参数"),
        ("显示", "在软件界面集中查看各节点数据"),
        ("存储", "保存历史数据，便于查询和比较"),
        ("分析", "把数据与作物生长条件对照"),
        ("报警", "数值异常时及时提示"),
        ("控制", "联动灌溉、施肥、喷药、降温、补光"),
    ]
    ops = chrome() + [
        title("云平台的核心作用"),
        T(
            "Lead",
            "云平台把分散的田间信息汇到一处，再帮助人做出判断和操作。",
            1.5,
            2.7,
            30.7,
            0.75,
            size=18,
            color=MUTED,
            valign="middle",
        ),
    ]
    for i, (h, b) in enumerate(rows):
        col = i % 2
        row = i // 2
        x = 1.5 + col * 15.7
        y = 3.7 + row * 4.25
        ops += [
            box(f"C{i}", x, y, 15.0, 3.95, CARD),
            box(f"Tag{i}", x + 0.4, y + 1.15, 3.4, 1.6, PRIMARY, preset="roundRect"),
            T(f"H{i}", h, x + 0.4, y + 1.15, 3.4, 1.6, size=20, bold=True, color=WHITE, align="center", valign="middle"),
            T(f"B{i}", b, x + 4.2, y + 0.7, 10.3, 2.5, size=18, color=TEXT, valign="middle"),
        ]
    finish(
        ops,
        "六项作用来自教材第15页，改写成课堂语言。追问：只看到数字，算不算已经自动浇水？答案：还不算。自动控制需要规则、指令和执行设备。",
    )


def slide_distributed() -> None:
    add_slide(PAPER, "分散采集与集中管理")
    ops = chrome() + [
        title("分散采集与集中管理"),
        box("L", 1.5, 3.15, 15.0, 10.2, CARD),
        T("LH", "分散采集", 2.0, 3.5, 14.0, 1.0, size=24, bold=True, color=PRIMARY),
        T(
            "LB",
            "温度、湿度、光照等参数，由不同位置的传感器分别测量。\n\n大棚一角、田间一块、水池一处，都可以成为采集点。\n\n系统规模可以按需要增加或减少节点。",
            2.0,
            4.8,
            14.0,
            10.8,
            size=18,
            color=TEXT,
        ),
        box("R", 17.2, 3.15, 15.0, 10.2, PRIMARY),
        T("RH", "集中管理", 17.7, 3.5, 14.0, 1.0, size=24, bold=True, color=GOLD),
        T(
            "RB",
            "各个节点把数据交给上位机和云平台。\n\n管理员不必逐棚巡视，也能查看数值、设置参数、存储记录、接收报警。\n\n人仍然负责规则和核查，平台负责及时汇集信息。",
            17.7,
            4.8,
            14.0,
            10.8,
            size=18,
            color=WHITE,
        ),
    ]
    finish(
        ops,
        "用“很多探头、一个中控室”类比。强调灵活增减节点。提醒：集中管理提高效率，不等于取消田间观察。下一页把作用收成四个“智能”。",
    )


def slide_four_smart() -> None:
    add_slide(PAPER, "感知、分析、预警、决策")
    items = [
        ("智能感知", "传感器与通信网络\n获取生产环境信息"),
        ("智能分析", "对照作物需求\n理解数据含义"),
        ("智能预警", "发现异常趋势\n提前提示风险"),
        ("智能决策", "给出灌溉、施肥等\n操作建议或指令"),
    ]
    xs = [1.5, 9.55, 17.6, 25.65]
    ops = chrome() + [
        title("感知、分析、预警、决策"),
        T(
            "Lead",
            "云平台是现代农业的技术底座之一，推动生产向数字化、智慧化发展。",
            1.5,
            2.7,
            30.7,
            0.75,
            size=18,
            color=MUTED,
            valign="middle",
        ),
    ]
    for i, (h, b) in enumerate(items):
        x = xs[i]
        ops += [
            box(f"C{i}", x, 3.8, 6.7, 6.6, PRIMARY if i in (0, 3) else CARD),
            T(
                f"N{i}",
                f"{i+1:02d}",
                x + 0.35,
                4.15,
                6.0,
                1.3,
                size=28,
                bold=True,
                color=GOLD if i in (0, 3) else MOSS,
            ),
            T(
                f"H{i}",
                h,
                x + 0.35,
                5.6,
                6.0,
                1.5,
                size=22,
                bold=True,
                color=WHITE if i in (0, 3) else PRIMARY,
            ),
            T(
                f"B{i}",
                b,
                x + 0.35,
                7.4,
                6.0,
                5.4,
                size=18,
                color=WHITE if i in (0, 3) else TEXT,
            ),
        ]
    ops += [
        connector("C0", "C1"),
        connector("C1", "C2"),
        connector("C2", "C3"),
    ]
    ops.append(
        T(
            "Ex",
            "教材中的自动监控例子：灌溉、施肥、喷药、降温、补光。这些动作发生在“决策”之后。",
            1.5,
            13.8,
            30.7,
            3.2,
            size=18,
            color=TEXT,
            fill=PALE,
            preset="roundRect",
            valign="middle",
            margin="0.35cm",
        )
    )
    finish(
        ops,
        "四个词来自教材第15页。不要让学生背形容词。改成问题：感知回答“现在怎样”，分析回答“这意味着什么”，预警回答“要不要注意”，决策回答“下一步做什么”。",
    )


def slide_app_devices() -> None:
    add_slide(PAPER, "云平台连接的田间设备")
    items = [
        ("多光谱无人机", "从空中观察作物长势"),
        ("无人抛秧机", "按方案完成栽插作业"),
        ("无人旋耕机", "远程调度田间整地"),
        ("无人收割机", "把收获过程纳入管理"),
        ("卫星遥感", "大范围掌握地块信息"),
        ("虫情报警灯", "监测并提示虫害风险"),
        ("气象站", "记录温度、降水、风力"),
        ("水位与土壤仪", "掌握水和土壤状况"),
    ]
    ops = chrome() + [
        title("云平台连接的田间设备"),
        T(
            "Lead",
            "以“中联智农云”这类应用为例：平台可以连接农机、遥感和田间监测设备。",
            1.5,
            2.7,
            30.7,
            0.75,
            size=18,
            color=MUTED,
            valign="middle",
        ),
    ]
    for i, (h, b) in enumerate(items):
        col = i % 4
        row = i // 4
        x = 1.5 + col * 7.9
        y = 3.7 + row * 6.5
        ops += [
            box(f"C{i}", x, y, 7.5, 6.1, CARD),
            T(f"N{i}", f"{i+1:02d}", x + 0.35, y + 0.35, 6.8, 0.8, size=16, bold=True, color=MOSS),
            T(f"H{i}", h, x + 0.35, y + 1.25, 6.8, 1.8, size=20, bold=True, color=PRIMARY),
            T(f"B{i}", b, x + 0.35, y + 3.2, 6.8, 2.4, size=18, color=TEXT),
        ]
    finish(
        ops,
        "设备名单出自教材第15页案例，用于说明“云平台能连接什么”，不是要求记住品牌。问：这些设备采集的信息，如果互不相通，管理员要打开多少个界面？由此体会平台的集中作用。",
    )


def slide_case() -> None:
    add_slide(PAPER, "田间作业怎样用上平台")
    ops = chrome() + [
        title("田间作业怎样用上平台"),
        box("L", 1.5, 3.15, 15.0, 10.4, CARD),
        T("LH", "平台可以做什么", 2.0, 3.5, 14.0, 1.0, size=22, bold=True, color=PRIMARY),
        T(
            "LB",
            "远程查看农机与传感器状态。\n\n根据数据提出田间作业建议。\n\n帮助实现节肥、减药、增产。",
            2.0,
            4.8,
            14.0,
            10.8,
            size=20,
            color=TEXT,
        ),
        box("R", 17.2, 3.15, 15.0, 10.4, PRIMARY),
        T("RH", "人还要做什么", 17.7, 3.5, 14.0, 1.0, size=22, bold=True, color=GOLD),
        T(
            "RB",
            "教材案例：湖南益阳大通湖。\n\n平台推送病虫害防治方案。\n\n农技人员到田里核查。\n\n未达防治标准的田块，不盲目施药。",
            17.7,
            4.8,
            14.0,
            10.8,
            size=20,
            color=WHITE,
        ),
    ]
    finish(
        ops,
        "这是教材中的真实应用情境。核心教学点：云平台给出建议，地面核查决定是否行动。防止学生得出“App说喷药就必须喷”的结论。可问：如果传感器误报虫害，缺少核查会怎样？",
    )


def slide_comm_key() -> None:
    add_slide(PAPER, "通信成为物联网的关键问题")
    ops = chrome() + [
        title("通信成为物联网的关键问题"),
        box("Hero", 1.5, 3.15, 30.7, 4.4, PRIMARY),
        T(
            "HeroT",
            "设备越来越多，它们怎样互相连接，就成了必须面对的技术问题。",
            2.1,
            3.5,
            29.5,
            3.6,
            size=24,
            bold=True,
            color=WHITE,
            valign="middle",
        ),
        box("A", 1.5, 7.9, 15.0, 8.65, CARD),
        T("AH", "近距离无线通信", 2.0, 8.25, 14.0, 1.0, size=22, bold=True, color=PRIMARY),
        T(
            "AB",
            "温室内部、设备与网关之间，常用短距离方式交换数据。要考虑距离、遮挡和耗电。",
            2.0,
            9.5,
            14.0,
            6.4,
            size=18,
            color=TEXT,
        ),
        box("B", 17.2, 7.9, 15.0, 8.65, CARD),
        T("BH", "移动通信与远程连接", 17.7, 8.25, 14.0, 1.0, size=22, bold=True, color=PRIMARY),
        T(
            "BB",
            "田块分散、管理人员不在现场时，需要把数据送到更远的平台。覆盖和资费成为现实约束。",
            17.7,
            9.5,
            14.0,
            6.4,
            size=18,
            color=TEXT,
        ),
    ]
    finish(
        ops,
        "从“设备多了”过渡到通信。不要把近距和远程说成互相对立，二者常配合：棚内近距汇聚，再经移动网络上云。下一页引入“协议”。",
    )


def slide_protocol_def() -> None:
    add_slide(PAPER, "通信协议是必须遵守的约定")
    ops = chrome() + [
        title("通信协议是必须遵守的约定"),
        box("Def", 1.5, 3.15, 30.7, 5.6, PRIMARY),
        T("DH", "一句话", 2.1, 3.45, 29.5, 0.8, size=18, bold=True, color=GOLD),
        T(
            "DB",
            "通信协议是双方完成通信或服务时，必须共同遵守的规则和约定。",
            2.1,
            4.4,
            29.5,
            3.8,
            size=26,
            bold=True,
            color=WHITE,
            valign="middle",
        ),
        box("C1", 1.5, 9.1, 15.0, 7.45, CARD),
        T("C1H", "像交通规则", 2.0, 9.45, 14.0, 1.0, size=22, bold=True, color=PRIMARY),
        T(
            "C1B",
            "红灯停、绿灯行。没有共同规则，车辆再多也无法安全通过路口。",
            2.0,
            10.7,
            14.0,
            5.3,
            size=18,
            color=TEXT,
        ),
        box("C2", 17.2, 9.1, 15.0, 7.45, CARD),
        T("C2H", "像寄包裹的写法", 17.7, 9.45, 14.0, 1.0, size=22, bold=True, color=PRIMARY),
        T(
            "C2B",
            "收件人、地址、物件内容要按规定填写。写错地址，包裹就到不了想去的地方。",
            17.7,
            10.7,
            14.0,
            5.3,
            size=18,
            color=TEXT,
        ),
    ]
    finish(
        ops,
        "用类比建立“协议”概念，再回到物联网。问：传感器和云平台如果“说话方式”不同，会出现什么？学生容易说“连不上”或“听不懂”，即可进入下一页的协议分层。",
    )


def slide_on_tcp() -> None:
    add_slide(PAPER, "物联网协议运行在互联网之上")
    layers = [
        ("应用与消息", "MQTT、网页访问等\n约定“说什么、给谁”"),
        ("传输与网络", "TCP/IP\n约定“如何可靠送达”"),
        ("连接与介质", "网线、Wi-Fi、移动网络\n约定“走哪条路”"),
    ]
    ops = chrome() + [
        title("物联网协议运行在互联网之上"),
        T(
            "Lead",
            "教材指出：许多物联网通信协议运行在传统互联网 TCP/IP 之上，负责设备经互联网交换数据。",
            1.5,
            2.7,
            30.7,
            1.1,
            size=18,
            color=MUTED,
        ),
    ]
    for i, (h, b) in enumerate(layers):
        y = 4.1 + i * 3.95
        fill = PRIMARY if i == 0 else (MOSS if i == 1 else CARD)
        tc = WHITE if i < 2 else TEXT
        hc = GOLD if i == 0 else (WHITE if i == 1 else PRIMARY)
        ops += [
            box(f"L{i}", 4.8, y, 24.2, 3.6, fill),
            T(f"H{i}", h, 5.3, y + 0.3, 23.2, 1.0, size=22, bold=True, color=hc),
            T(f"B{i}", b, 5.3, y + 1.35, 23.2, 1.9, size=18, color=tc),
        ]
    finish(
        ops,
        "这是“能量加油站”的关键句。用三层示意帮助学生建立位置感：MQTT 不是网线，TCP/IP 不是土壤传感器。为后面纠正“MQTT 比 TCP/IP 更慢”这类混层判断做铺垫。",
    )


def slide_zigbee_def() -> None:
    add_slide(PAPER, "紫蜂 ZigBee 的定义")
    ops = chrome() + [
        title("紫蜂 ZigBee 的定义"),
        box("Hero", 1.5, 3.15, 30.7, 6.3, PRIMARY),
        T("EN", "ZigBee", 2.1, 3.5, 29.5, 1.3, size=28, bold=True, color=GOLD),
        T(
            "DEF",
            "一种低速、短距离的无线通信协议，常被看成高可靠的无线传输网络。",
            2.1,
            5.0,
            29.5,
            3.8,
            size=24,
            bold=True,
            color=WHITE,
            valign="middle",
        ),
        box("A", 1.5, 9.8, 15.0, 6.75, CARD),
        T("AH", "记住两个限定", 2.0, 10.15, 14.0, 0.9, size=20, bold=True, color=PRIMARY),
        T("AB", "低速：适合少量状态和传感数据，不适合传高清视频。\n短距离：覆盖温室局部，不单独承担跨县传输。", 2.0, 11.2, 14.0, 4.8, size=18, color=TEXT),
        box("B", 17.2, 9.8, 15.0, 6.75, CARD),
        T("BH", "在本课中的位置", 17.7, 10.15, 14.0, 0.9, size=20, bold=True, color=PRIMARY),
        T("BB", "它主要解决“附近设备怎么连”。云平台上的消息交换，还要靠更上层的应用协议，例如 MQTT。", 17.7, 11.2, 14.0, 4.8, size=18, color=TEXT),
    ]
    finish(
        ops,
        "对应教材第16页能量加油站。读定义后立刻加两个限定，避免学生把 ZigBee 说成“万能农业网”。可问：无人机航拍图像适合用 ZigBee 回传吗？为什么？",
    )


def slide_zigbee_use() -> None:
    add_slide(PAPER, "ZigBee 的场景与特点")
    feats = [
        ("低耗电", "适合长期布置的传感节点"),
        ("低成本", "便于大量节点铺开"),
        ("支持多种网络", "可组成星型或网状等结构"),
        ("速度较慢", "相对 Wi-Fi 等更适合短报文"),
        ("穿墙较弱", "金属和墙壁会挡住信号"),
    ]
    ops = chrome() + [
        title("ZigBee 的场景与特点"),
        box("Sc", 1.5, 3.1, 30.7, 3.15, PALE),
        T(
            "ScT",
            "教材中的生活场景：智能插座、智能照明、智能窗帘。农业中也常用于棚内传感与控制节点。",
            2.0,
            3.35,
            29.7,
            2.65,
            size=18,
            color=TEXT,
            valign="middle",
        ),
    ]
    for i, (h, b) in enumerate(feats):
        x = 1.5 + i * 6.28
        ops += [
            box(f"C{i}", x, 6.55, 6.05, 9.95, CARD if i != 3 else PRIMARY),
            T(
                f"H{i}",
                h,
                x + 0.28,
                6.9,
                5.5,
                2.4,
                size=20,
                bold=True,
                color=WHITE if i == 3 else PRIMARY,
            ),
            T(
                f"B{i}",
                b,
                x + 0.28,
                9.5,
                5.5,
                6.4,
                size=18,
                color=WHITE if i == 3 else TEXT,
            ),
        ]
    finish(
        ops,
        "五个特点来自教材。讲解“速度慢、穿墙弱”时加限定：是相对于 Wi-Fi、以太网的课堂对比，不是说 ZigBee 不能用。点出低功耗才是田间传感器看重的原因。",
    )


def slide_protocols() -> None:
    add_slide(PAPER, "农业物联网常见协议")
    items = [
        ("ZigBee", "近距无线", "棚内传感、照明、插座一类短距控制"),
        ("蓝牙 BLE", "近距无线", "手持终端、可穿戴设备、近距调试"),
        ("MQTT", "消息协议", "设备按主题发布，平台或手机按需订阅"),
        ("NB-IoT / LoRa", "远距低功耗", "分散田块把少量数据送到远处平台"),
    ]
    ops = chrome() + [
        title("农业物联网常见协议"),
        T(
            "Lead",
            "做一做：查找农业物联网常见协议的作用、场景和特点。先抓住“它主要解决哪一层问题”。",
            1.5,
            2.7,
            30.7,
            1.05,
            size=18,
            color=MUTED,
        ),
    ]
    for i, (h, tag, b) in enumerate(items):
        col = i % 2
        row = i // 2
        x = 1.5 + col * 15.7
        y = 4.05 + row * 6.35
        ops += [
            box(f"C{i}", x, y, 15.0, 6.05, CARD),
            T(f"H{i}", h, x + 0.5, y + 0.4, 14.0, 1.1, size=24, bold=True, color=PRIMARY),
            T(f"Tag{i}", tag, x + 0.5, y + 1.6, 14.0, 0.8, size=16, bold=True, color=MOSS),
            T(f"B{i}", b, x + 0.5, y + 2.6, 14.0, 2.9, size=18, color=TEXT),
        ]
    finish(
        ops,
        "此页对应第16页查找任务，给出课堂支架而不是让学生抄百科。MQTT 出现在教材第18页拓展，却最贴近“云平台收消息”。强调：ZigBee 管近距无线，MQTT 管消息怎么订阅，不要当成同一种东西。",
    )


def slide_mqtt() -> None:
    add_slide(PAPER, "MQTT 的发布与订阅")
    roles = [
        ("发布者", "土壤采集终端\n把读数发给服务器"),
        ("Broker", "MQTT 消息服务器\n按主题匹配后再分发"),
        ("订阅者", "云平台或手机\n只接收自己关心的消息"),
    ]
    xs = [1.5, 12.08, 22.66]
    ops = chrome() + [
        title("MQTT 的发布与订阅"),
        T(
            "Lead",
            "云平台要同时面对许多设备和许多用户。MQTT 用“发布 / 订阅”来组织消息，而不是一对一打电话。",
            1.5,
            2.7,
            30.7,
            1.05,
            size=18,
            color=MUTED,
        ),
    ]
    for i, (h, b) in enumerate(roles):
        x = xs[i]
        fill = PRIMARY if i == 1 else CARD
        ops += [
            box(f"R{i}", x, 4.1, 9.58, 8.8, fill),
            T(
                f"H{i}",
                h,
                x + 0.45,
                4.5,
                8.7,
                1.4,
                size=24,
                bold=True,
                color=WHITE if i == 1 else PRIMARY,
            ),
            T(
                f"B{i}",
                b,
                x + 0.45,
                6.2,
                8.7,
                6.1,
                size=18,
                color=WHITE if i == 1 else TEXT,
            ),
        ]
    ops += [
        connector("R0", "R1"),
        connector("R1", "R2"),
        T(
            "Tip",
            "Broker 负责把消息送给订阅者。作物要不要浇水，由平台里的规则程序判断，不是 Broker 在种田。",
            1.5,
            13.3,
            30.7,
            3.7,
            size=18,
            color=TEXT,
            fill=PALE,
            preset="roundRect",
            valign="middle",
            margin="0.35cm",
        ),
    ]
    finish(
        ops,
        "用寄信类比：发布者写信，主题是地址类别，Broker 是邮局，订阅者是订了某类信件的人。强调一个设备可以既发布又订阅。不要把 Broker 讲成“智慧大脑”。",
    )


def slide_topic() -> None:
    add_slide(PAPER, "主题决定谁能收到消息")
    ops = chrome() + [
        title("主题决定谁能收到消息"),
        box("Pub", 1.5, 3.15, 15.0, 6.5, PRIMARY),
        T("PH", "本次发布", 2.0, 3.5, 14.0, 0.8, size=18, bold=True, color=GOLD),
        T("PT", "farm/1/soil", 2.0, 4.5, 14.0, 1.6, size=28, bold=True, color=WHITE),
        T("PB", "一号棚的土壤读数\n内容示例：28%", 2.0, 6.3, 14.0, 2.9, size=18, color=WHITE),
        box("Sub", 17.2, 3.15, 15.0, 6.5, CARD),
        T("SH", "手机当前订阅", 17.7, 3.5, 14.0, 0.8, size=18, bold=True, color=MOSS),
        T("ST", "farm/2/soil", 17.7, 4.5, 14.0, 1.6, size=28, bold=True, color=PRIMARY),
        T("SB", "二号棚的土壤读数\n主题不一致，不会投递到这部手机", 17.7, 6.3, 14.0, 2.9, size=18, color=TEXT),
        box("Q", 1.5, 10.0, 30.7, 6.55, PALE),
        T("QH", "课堂判断", 2.1, 10.35, 29.5, 0.8, size=20, bold=True, color=PRIMARY),
        T(
            "QB",
            "发布主题和订阅主题要对得上，消息才会被接收。棚号写错，人就会看错地块。\nJSON 只是本课装数据的一种写法，MQTT 并不规定内容必须是 JSON。",
            2.1,
            11.3,
            29.5,
            4.7,
            size=18,
            color=TEXT,
        ),
    ]
    finish(
        ops,
        "用反例让学生理解主题。可板书 farm/棚号/对象。选做：+ 号匹配一层，farm/+/soil 能同时关心多个棚的土壤。提醒大小写要一致。不要把 JSON 讲成编程课。",
    )


def slide_keywords() -> None:
    add_slide(PAPER, "设计：找出本课关键词")
    words = [
        ("传输设备", "路由器  网关  节点"),
        ("云平台功能", "采集  存储  报警  控制"),
        ("近距协议", "ZigBee  蓝牙"),
        ("消息协议", "MQTT  主题  发布  订阅"),
        ("远距连接", "移动通信  NB-IoT"),
        ("思维成果", "农业物联网云平台"),
    ]
    ops = chrome() + [
        title("设计：找出本课关键词"),
        T(
            "Lead",
            "先在草稿上圈出关键词，再考虑它们怎样连成分支。不要一上来抄完整句子。",
            1.5,
            2.7,
            30.7,
            0.8,
            size=18,
            color=MUTED,
            valign="middle",
        ),
    ]
    for i, (h, b) in enumerate(words):
        col = i % 3
        row = i // 3
        x = 1.5 + col * 10.55
        y = 3.8 + row * 6.5
        ops += [
            box(f"C{i}", x, y, 10.15, 6.15, CARD if i != 5 else PRIMARY),
            T(f"H{i}", h, x + 0.45, y + 0.45, 9.25, 1.4, size=22, bold=True, color=WHITE if i == 5 else PRIMARY),
            T(f"B{i}", b, x + 0.45, y + 2.1, 9.25, 3.5, size=18, color=WHITE if i == 5 else TEXT),
        ]
    finish(
        ops,
        "对应教材第16页设计。学生先写词，再连线。巡视时看是否把“设备”和“协议”分成两类。有人把 MQTT 写成无线信号，当场用上一页主题例子纠正。",
    )


def slide_map_blank() -> None:
    add_slide(PAPER, "实践：补全思维导图")
    ops = chrome() + [
        title("实践：补全思维导图"),
        T(
            "Lead",
            "打开“智慧农业示范区”文件，添加“农业物联网云平台”子主题。\n先填设备，再填协议。",
            1.5,
            2.58,
            30.7,
            1.75,
            size=18,
            color=MUTED,
            valign="middle",
        ),
        box("Root", 1.5, 8.55, 6.4, 3.2, PRIMARY),
        T("RootT", "农业物联网\n云平台", 1.6, 8.55, 6.2, 3.2, size=18, bold=True, color=WHITE, align="center", valign="middle"),
        box("Dev", 10.2, 4.5, 6.6, 2.9, MOSS),
        T("DevT", "常见的\n传输设备", 10.3, 4.5, 6.4, 2.9, size=18, bold=True, color=WHITE, align="center", valign="middle"),
        box("Pro", 10.2, 12.7, 6.6, 2.9, MOSS),
        T("ProT", "常见的\n通信协议", 10.3, 12.7, 6.4, 2.9, size=18, bold=True, color=WHITE, align="center", valign="middle"),
        box("D1", 19.3, 4.5, 12.5, 2.1, CARD),
        T("D1T", "设备 1  ________", 19.5, 4.5, 12.1, 2.1, size=18, color=MUTED, valign="middle"),
        box("D2", 19.3, 6.8, 12.5, 2.1, CARD),
        T("D2T", "设备 2  ________", 19.5, 6.8, 12.1, 2.1, size=18, color=MUTED, valign="middle"),
        box("D3", 19.3, 9.1, 12.5, 2.1, CARD),
        T("D3T", "设备 3  ________", 19.5, 9.1, 12.1, 2.1, size=18, color=MUTED, valign="middle"),
        box("P1", 19.3, 11.5, 12.5, 2.1, CARD),
        T("P1T", "ZigBee  特点：________", 19.5, 11.5, 12.1, 2.1, size=18, color=MUTED, valign="middle"),
        box("P2", 19.3, 13.8, 12.5, 2.1, CARD),
        T("P2T", "MQTT  作用：________", 19.5, 13.8, 12.1, 2.1, size=18, color=MUTED, valign="middle"),
        connector("Root", "Dev", shape="elbow"),
        connector("Root", "Pro", shape="elbow"),
        connector("Dev", "D1", shape="elbow"),
        connector("Dev", "D2", shape="elbow"),
        connector("Dev", "D3", shape="elbow"),
        connector("Pro", "P1", shape="elbow"),
        connector("Pro", "P2", shape="elbow"),
    ]
    finish(
        ops,
        "对应教材第17页实践。限时4–6分钟。允许学生用自己的词，但分支上至少要出现设备和协议两类。下一页再出示参考，避免先看后抄。",
    )


def slide_map_key() -> None:
    add_slide(PAPER, "思维导图参考结构")
    ops = chrome() + [
        title("思维导图参考结构"),
        box("Root", 1.5, 8.15, 6.4, 3.4, PRIMARY),
        T("RootT", "农业物联网\n云平台", 1.6, 8.15, 6.2, 3.4, size=18, bold=True, color=WHITE, align="center", valign="middle"),
        box("Dev", 9.9, 4.0, 6.3, 3.0, MOSS),
        T("DevT", "传输设备", 10.0, 4.0, 6.1, 3.0, size=18, bold=True, color=WHITE, align="center", valign="middle"),
        box("Pro", 9.9, 12.45, 6.3, 3.0, MOSS),
        T("ProT", "通信协议", 10.0, 12.45, 6.1, 3.0, size=18, bold=True, color=WHITE, align="center", valign="middle"),
        box("D1", 18.0, 3.15, 14.2, 2.15, CARD),
        T("D1T", "无线路由器：接入无线局域网", 18.2, 3.15, 13.8, 2.15, size=18, color=TEXT, valign="middle"),
        box("D2", 18.0, 5.5, 14.2, 2.15, CARD),
        T("D2T", "近距模块：完成短距离连接", 18.2, 5.5, 13.8, 2.15, size=18, color=TEXT, valign="middle"),
        box("D3", 18.0, 7.85, 14.2, 2.15, CARD),
        T("D3T", "智能网关：汇聚并转发数据", 18.2, 7.85, 13.8, 2.15, size=18, color=TEXT, valign="middle"),
        box("P1", 18.0, 10.7, 14.2, 2.5, CARD),
        T("P1T", "ZigBee：低功耗、短距离、低速", 18.2, 10.7, 13.8, 2.5, size=18, color=TEXT, valign="middle"),
        box("P2", 18.0, 13.4, 14.2, 2.5, CARD),
        T("P2T", "MQTT：按主题发布和订阅消息", 18.2, 13.4, 13.8, 2.5, size=18, color=TEXT, valign="middle"),
        connector("Root", "Dev", shape="elbow"),
        connector("Root", "Pro", shape="elbow"),
        connector("Dev", "D1", shape="elbow"),
        connector("Dev", "D2", shape="elbow"),
        connector("Dev", "D3", shape="elbow"),
        connector("Pro", "P1", shape="elbow"),
        connector("Pro", "P2", shape="elbow"),
    ]
    finish(
        ops,
        "参考结构对应教材框图，并补上 MQTT，因为它是云平台收数的关键。评价看关系是否说清，不看是否和示例用词完全一致。请同伴用一句话复述对方的图。",
    )


def slide_classify() -> None:
    add_slide(PAPER, "通信技术的三种分类")
    cols = [
        (
            "按通信介质",
            "无线：蜂窝、Wi-Fi、蓝牙、ZigBee、LoRa\n有线：以太网、电力线载波等",
        ),
        (
            "按传输速率",
            "低速：蓝牙、ZigBee、NB-IoT、LoRa\n中高速：Wi-Fi、以太网、4G/5G",
        ),
        (
            "按功耗高低",
            "低功耗：蓝牙、ZigBee、NB-IoT\n较高功耗：Wi-Fi、多代移动通信",
        ),
    ]
    xs = [1.5, 12.08, 22.66]
    ops = chrome() + [
        title("通信技术的三种分类"),
        T(
            "Lead",
            "拓展页把技术按介质、速率、功耗分开看。同一技术会出现在不同分类里，这是正常的。",
            1.5,
            2.7,
            30.7,
            0.85,
            size=18,
            color=MUTED,
            valign="middle",
        ),
    ]
    for i, (h, b) in enumerate(cols):
        x = xs[i]
        ops += [
            box(f"C{i}", x, 3.85, 9.58, 12.7, PRIMARY if i == 0 else CARD),
            T(
                f"H{i}",
                h,
                x + 0.45,
                4.2,
                8.7,
                1.6,
                size=22,
                bold=True,
                color=WHITE if i == 0 else PRIMARY,
            ),
            T(
                f"B{i}",
                b,
                x + 0.45,
                6.1,
                8.7,
                9.8,
                size=18,
                color=WHITE if i == 0 else TEXT,
            ),
        ]
    finish(
        ops,
        "不要让学生背完整分类树。抓住方法：遇到一种技术，问它走无线还是有线、快还是慢、费不费电。指出教材把 LTE Cat.1、Sigfox 等列入，课堂只需认识分类角度。",
    )


def slide_compare() -> None:
    add_slide(PAPER, "物联网协议与互联网协议")
    ops = chrome() + [
        title("物联网协议与互联网协议"),
        box("L", 1.5, 3.15, 15.0, 13.4, CARD),
        T("LH", "物联网侧常见", 2.0, 3.5, 14.0, 1.0, size=22, bold=True, color=PRIMARY),
        T(
            "LB",
            "蓝牙、ZigBee、MQTT 等。\n\n面对的是大量终端、较短报文、有时供电受限。\n\n更关心低功耗、按需连接、按主题分发。",
            2.0,
            4.8,
            14.0,
            10.8,
            size=18,
            color=TEXT,
        ),
        box("R", 17.2, 3.15, 15.0, 13.4, PRIMARY),
        T("RH", "互联网侧常见", 17.7, 3.5, 14.0, 1.0, size=22, bold=True, color=GOLD),
        T(
            "RB",
            "TCP/IP 是基础。\nHTTP、FTP、SMTP 等很常见。\n\n面对的是网页、文件、邮件等应用。\n\n更关心通用、高速、稳定地交换信息。",
            17.7,
            4.8,
            14.0,
            10.8,
            size=18,
            color=WHITE,
        ),
    ]
    finish(
        ops,
        "对应教材第18页比较表。先让学生说相同点：都要双方遵守约定，都为了交换信息。不同点先让他们用本页关键词说，不要直接念“物联网协议更慢、更不稳定”。下一页专门澄清层次。",
    )


def slide_layers() -> None:
    add_slide(PAPER, "分层看协议更准确")
    ops = chrome() + [
        title("分层看协议更准确"),
        box("Warn", 1.5, 3.1, 30.7, 3.4, "F4E6D8"),
        T(
            "WT",
            "教材把蓝牙、ZigBee、MQTT 与 TCP/IP 放在一起比较。课堂里要补一句：它们并不都在同一层。",
            2.0,
            3.35,
            29.7,
            2.9,
            size=18,
            color=TEXT,
            valign="middle",
        ),
        box("A", 1.5, 6.8, 15.0, 9.75, CARD),
        T("AH", "不要混在一起的判断", 2.0, 7.15, 14.0, 1.1, size=20, bold=True, color=TERR),
        T(
            "AB",
            "“MQTT 比 TCP/IP 慢”不合适。MQTT 通常正是跑在 TCP/IP 上。\n\n“ZigBee 比 HTTP 不稳定”也不合适。一个管近距无线，一个管网页访问。",
            2.0,
            8.5,
            14.0,
            7.5,
            size=18,
            color=TEXT,
        ),
        box("B", 17.2, 6.8, 15.0, 9.75, PRIMARY),
        T("BH", "更准确的课堂说法", 17.7, 7.15, 14.0, 1.1, size=20, bold=True, color=GOLD),
        T(
            "BB",
            "ZigBee、蓝牙：解决附近设备如何无线连接。\n\nTCP/IP：解决数据在互联网中如何传送。\n\nMQTT：解决海量设备如何按主题发布和订阅。",
            17.7,
            8.5,
            14.0,
            7.5,
            size=18,
            color=WHITE,
        ),
    ]
    finish(
        ops,
        "这页是教师必须讲清的科学表述。尊重教材比较表，同时避免错误层次观。学生能说出“MQTT 在 TCP/IP 之上、ZigBee 是近距无线”即可，不引入 OSI 全称记忆。",
    )


def slide_quiz() -> None:
    add_slide(PAPER, "课堂检测")
    qs = [
        ("01", "云平台的作用", "只显示当前数字，算不算已经完成自动控制？还缺什么？"),
        ("02", "协议分工", "ZigBee 和 MQTT 能不能互相替代？各管什么？"),
        ("03", "主题匹配", "手机订阅 farm/1/soil，终端发布 farm/2/soil，手机收得到吗？"),
    ]
    ops = chrome() + [title("课堂检测")]
    for i, (n, h, b) in enumerate(qs):
        y = 3.15 + i * 4.55
        ops += [
            box(f"C{i}", 1.5, y, 30.7, 4.25, CARD),
            box(f"N{i}", 1.95, y + 1.15, 2.0, 2.0, PRIMARY, preset="ellipse"),
            T(f"NT{i}", n, 1.95, y + 1.15, 2.0, 2.0, size=16, bold=True, color=WHITE, align="center", valign="middle"),
            T(f"H{i}", h, 4.4, y + 0.45, 27.2, 1.0, size=22, bold=True, color=PRIMARY, valign="middle"),
            T(f"B{i}", b, 4.4, y + 1.6, 27.2, 2.1, size=18, color=TEXT, valign="middle"),
        ]
    finish(
        ops,
        "先独立写，再两人互说理由。不要齐答。进度紧时只做第2、第3题。第1题用来区分监测与控制，第2题区分层次，第3题检查主题概念。",
    )


def slide_close() -> None:
    add_slide(DARK, "本课收获")
    ops = chrome(dark=True) + [
        title("本课收获", dark=True),
        T(
            "Lead",
            "回到开头那句话：远处的水阀，怎样知道温室可能缺水？",
            1.5,
            2.75,
            30.7,
            0.9,
            size=18,
            color=WHEAT,
            valign="middle",
        ),
        box("A", 1.5, 3.9, 9.58, 9.3, "163224"),
        T("AH", "数据", 1.95, 4.25, 8.7, 1.1, size=22, bold=True, color=GOLD),
        T("AB", "传感器采集，经节点或网关，由网络送到云平台。", 1.95, 5.6, 8.7, 7.0, size=18, color=WHITE),
        box("B", 12.08, 3.9, 9.58, 9.3, "163224"),
        T("BH", "约定", 12.53, 4.25, 8.7, 1.1, size=22, bold=True, color=GOLD),
        T("BB", "近距可用 ZigBee 等；上云常用 MQTT 按主题发布和订阅。", 12.53, 5.6, 8.7, 7.0, size=18, color=WHITE),
        box("C", 22.66, 3.9, 9.58, 9.3, "163224"),
        T("CH", "行动", 23.11, 4.25, 8.7, 1.1, size=22, bold=True, color=GOLD),
        T("CB", "平台分析、预警、辅助决策；人设置规则并核查田间结果。", 23.11, 5.6, 8.7, 7.0, size=18, color=WHITE),
        T(
            "Home",
            "课后：补完思维导图；用一段话解释“采集—传输—处理—控制”。选做：查一种农业场景中的 MQTT 主题该怎么命名。",
            1.5,
            13.5,
            30.7,
            3.5,
            size=18,
            color=WHITE,
            fill="163224",
            preset="roundRect",
            valign="middle",
            margin="0.35cm",
        ),
    ]
    finish(
        ops,
        "请两名学生用自己的话回答导入问题。优秀回答应包含设备、网络/协议、云平台判断、执行与核查。布置思维导图为必交作业。强调本课阈值、曲线均为教学示意。",
    )


def prepare() -> None:
    os.makedirs(os.path.dirname(FILE), exist_ok=True)
    if os.path.exists(FILE):
        run("close", FILE, check=False)
        os.remove(FILE)
    run("create", FILE)
    run("open", FILE)
    blank = run("view", FILE, "outline").stdout
    if "Slide 1" in blank:
        run("remove", FILE, "/slide[1]")
    run(
        "set",
        FILE,
        "/",
        "--prop",
        "title=探秘农业物联网云平台",
        "--prop",
        "author=信息科技课堂课件",
        "--prop",
        "description=教育科学出版社《信息科技 八年级上册》第一单元第3课课堂课件",
        "--prop",
        "keywords=物联网,云平台,ZigBee,MQTT,智慧农业",
        check=False,
    )


def main() -> None:
    prepare()
    builders = [
        slide_cover,
        slide_position,
        slide_goals,
        slide_focus,
        slide_path,
        slide_devices_quiz,
        slide_devices_key,
        slide_platform_role,
        slide_distributed,
        slide_four_smart,
        slide_app_devices,
        slide_case,
        slide_comm_key,
        slide_protocol_def,
        slide_on_tcp,
        slide_zigbee_def,
        slide_zigbee_use,
        slide_protocols,
        slide_mqtt,
        slide_topic,
        slide_keywords,
        slide_map_blank,
        slide_map_key,
        slide_classify,
        slide_compare,
        slide_layers,
        slide_quiz,
        slide_close,
    ]
    global TOTAL
    TOTAL = len(builders)
    for fn in builders:
        fn()
    run("save", FILE)
    print("built", FILE, "slides", S)
    print(run("view", FILE, "outline").stdout)


if __name__ == "__main__":
    main()
