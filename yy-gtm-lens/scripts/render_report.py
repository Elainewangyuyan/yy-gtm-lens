#!/usr/bin/env python3
import argparse
import html
import json
import math
import shutil
from pathlib import Path

THEMES = {
    "01": "blue", "02": "violet", "03": "mint", "04": "blue",
    "05": "peach", "06": "mint", "07": "violet", "08": "peach",
    "09": "violet", "10": "gold",
}

NAV_LABELS = {
    "01": "总览", "02": "赛道与竞争", "03": "产品与商业模式",
    "04": "用户、收入与增长", "05": "资本与估值",
    "06": "模型、数据与开源", "07": "团队、组织与招聘",
    "08": "GTM 难题与增长建议", "10": "催化剂、风险与观察",
}


def esc(value):
    return html.escape(str(value), quote=True)


def split_section(section):
    pages, current = [], []
    for block in section.get("blocks", []):
        if block.get("page_break_before") and current:
            pages.append(current)
            current = []
        current.append(block)
    pages.append(current)
    return pages


def block_markdown(block):
    kind = block.get("type")
    if kind == "paragraph":
        return block.get("text", "")
    if kind == "heading":
        return f"### {block.get('text', '')}"
    if kind == "quote":
        return "\n".join(f"> {line}" for line in block.get("text", "").splitlines())
    if kind == "list":
        ordered = block.get("ordered", False)
        return "\n".join(
            f"{i + 1}. {item}" if ordered else f"- {item}"
            for i, item in enumerate(block.get("items", []))
        )
    if kind == "table":
        headers = block.get("headers", [])
        rows = block.get("rows", [])
        head = "| " + " | ".join(map(str, headers)) + " |"
        rule = "| " + " | ".join(["---"] * len(headers)) + " |"
        body = ["| " + " | ".join(map(str, row)) + " |" for row in rows]
        return "\n".join([head, rule, *body])
    return ""


def block_html(block):
    kind = block.get("type")
    if kind == "paragraph":
        return f"<p>{esc(block.get('text', ''))}</p>"
    if kind == "heading":
        return f"<h3>{esc(block.get('text', ''))}</h3>"
    if kind == "quote":
        return f"<div class=\"quote\">{esc(block.get('text', ''))}</div>"
    if kind == "list":
        tag = "ol" if block.get("ordered") else "ul"
        items = "".join(f"<li>{esc(item)}</li>" for item in block.get("items", []))
        return f"<{tag}>{items}</{tag}>"
    if kind == "table":
        headers = "".join(f"<th>{esc(x)}</th>" for x in block.get("headers", []))
        rows = "".join(
            "<tr>" + "".join(f"<td>{esc(x)}</td>" for x in row) + "</tr>"
            for row in block.get("rows", [])
        )
        return f"<table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>"
    return ""


def report_markdown(data, private=False):
    meta = data["meta"]
    if private:
        sections = [data["private_section"]]
        title = f"# {meta['company']} 私密第 09 部分"
    else:
        sections = data["sections"]
        title = f"# {meta['company']} 深度研究"
    out = [
        title,
        "",
        f"- 研究截止：{meta['research_date']}",
        f"- 核心受众：{meta['audience']}",
        "",
    ]
    for section in sections:
        out.extend([
            f"## {section['number']} {section['title']}",
            "",
            f"**判断：{section['judgment']}**",
            "",
        ])
        for block in section.get("blocks", []):
            out.extend([block_markdown(block), ""])
    if not private:
        out.extend(["## 来源附件", ""])
        current = None
        for source in data.get("sources", []):
            if source.get("category") != current:
                current = source.get("category", "其他")
                out.extend([f"### {current}", ""])
            dates = []
            if source.get("published_date"):
                dates.append(f"发布 {source['published_date']}")
            if source.get("accessed_date"):
                dates.append(f"访问 {source['accessed_date']}")
            suffix = f"（{'；'.join(dates)}）" if dates else ""
            out.append(f"{source['id']}. [{source['title']}]({source['url']}){suffix}")
    return "\n".join(out).strip() + "\n"


def quality_markdown(data):
    quality = data.get("quality_review", {})
    out = [
        f"# {data['meta']['company']} 研究质量复核",
        "",
        f"- 状态：{quality.get('status', 'pending')}",
        f"- 复核日期：{quality.get('reviewed_date', '')}",
        f"- 复核人：{quality.get('reviewer', '')}",
        "",
        quality.get("summary", ""),
        "",
    ]
    for level in ("p0", "p1", "p2"):
        out.append(f"## {level.upper()}")
        findings = quality.get(level, [])
        out.extend([f"- {item}" for item in findings] or ["- 无"])
        out.append("")
    out.append("## 尚未解决的未知信息")
    out.extend(
        [f"- {item}" for item in quality.get("unresolved_unknowns", [])] or ["- 无"]
    )
    return "\n".join(out).strip() + "\n"


def tags_html(tags):
    return "<div class=\"tags\">" + "".join(
        f"<span class=\"tag\">{esc(item['label'])} <b>{esc(item['value'])}</b></span>"
        for item in tags
    ) + "</div>"


def signals_html(signals):
    return "<div class=\"signals\">" + "".join(
        f"<div class=\"signal\"><small>{esc(item['label'])}</small>"
        f"<strong>{esc(item['value'])}</strong><span>{esc(item.get('note', ''))}</span></div>"
        for item in signals
    ) + "</div>"


def visual_html(visual):
    items = visual.get("items", [])
    if not items:
        return ""
    if visual.get("type") == "bars":
        bars = "".join(
            f"<div class=\"bar\"><span>{esc(item.get('label', ''))}</span>"
            f"<i><b style=\"width:{max(0, min(100, int(item.get('score', 0))))}%\"></b></i>"
            f"<strong>{esc(item.get('value', item.get('score', '')))}</strong></div>"
            for item in items
        )
        return f"<div class=\"visual\"><div class=\"bars\">{bars}</div></div>"
    cols = 2 if visual.get("type") in {"matrix", "balance"} else min(4, max(2, len(items)))
    cards = "".join(
        f"<div class=\"v-card\"><small>{esc(item.get('label', ''))}</small>"
        f"<strong>{esc(item.get('value', ''))}</strong>"
        f"<span>{esc(item.get('note', ''))}</span></div>"
        for item in items
    )
    return f"<div class=\"visual\"><div class=\"visual-grid\" style=\"--cols:{cols}\">{cards}</div></div>"


def owner_views_html():
    return """
    <section class="opinions">
      <h3>我的观点</h3>
      <p>可继续新增，不改动经过质检的正式正文。</p>
      <div class="opinion-grid" data-owner-views></div>
      <form class="opinion-form no-print" data-opinion-form>
        <input name="title" required placeholder="观点标题">
        <input name="tags" placeholder="标签，用逗号分隔">
        <textarea name="body" required placeholder="判断、反例或准备验证的增长假设"></textarea>
        <button class="btn primary" type="submit">新增观点</button>
      </form>
    </section>"""


def page_html(section, blocks, part, total, page_number, private=False):
    number = section["number"]
    theme = section.get("theme") or THEMES[number]
    continuation = f"<span class=\"part\">PART {part} / {total}</span>" if total > 1 else ""
    body = "".join(block_html(block) for block in blocks)
    body = f"<div class=\"judgment\">判断：{esc(section['judgment'])}</div>{body}"
    visual = visual_html(section.get("visual", {})) if part == total else ""
    return f"""
    <article class="page {theme}" id="section-{number}{'-' + str(part) if part > 1 else ''}">
      <header class="head">
        <span class="num">{number}</span>
        <div class="title-wrap">
          <div class="title-row"><h2>{esc(section['title'])}</h2>{continuation}</div>
          {tags_html(section['tags'])}
        </div>
      </header>
      {signals_html(section['signals'])}
      <div class="copy">{body}</div>
      {visual}
      <footer class="footer"><span>{'PRIVATE DECISION MEMO' if private else 'YY GTM LENS'}</span><span>{page_number:02}</span></footer>
    </article>"""


def opinion_page_html(page_number):
    return f"""
    <article class="page peach" id="section-08-opinions">
      <header class="head">
        <span class="num">08</span>
        <div class="title-wrap">
          <div class="title-row"><h2>我的观点与互动补充</h2><span class="part">OWNER VIEW</span></div>
          <div class="tags">
            <span class="tag">区域性质 <b>互动补充</b></span>
            <span class="tag">正文关系 <b>不改质检正文</b></span>
            <span class="tag">适用场景 <b>GTM 观察</b></span>
          </div>
        </div>
      </header>
      <div class="signals">
        <div class="signal"><small>ADD</small><strong>新观点</strong><span>本地保存</span></div>
        <div class="signal"><small>USE</small><strong>标题/话术/假设</strong><span>可继续补充</span></div>
        <div class="signal"><small>PRIVACY</small><strong>公开区</strong><span>不要写私密职业判断</span></div>
      </div>
      {owner_views_html()}
      <footer class="footer"><span>YY GTM LENS</span><span>{page_number:02}</span></footer>
    </article>"""


def cover_html(meta, private=False):
    return f"""
    <article class="page cover" id="top">
      <div class="cover-copy">
        <p class="eyebrow">{'PRIVATE CAREER MEMO' if private else 'AI-NATIVE COMPANY DEEP DIVE'}</p>
        <h1>{esc(meta['company'])}<span>{esc(meta['subtitle'])}</span></h1>
        <p>{esc(meta['audience'])} · 研究截止 {esc(meta['research_date'])}</p>
        <div class="pills">
          <span>{'仅限本人' if private else '公开研究'}</span>
          <span>质检修订版</span>
          <span>{'第 09 部分' if private else '01–08、10'}</span>
        </div>
      </div>
      <div class="moon"></div>
      <footer class="footer"><span>{'PRIVATE' if private else 'PUBLIC'} REPORT</span><span>01</span></footer>
    </article>"""


def source_pages_html(data, start_page):
    sources = data.get("sources", [])
    chunks = [sources[i:i + 10] for i in range(0, len(sources), 10)] or [[]]
    pages = []
    for index, chunk in enumerate(chunks, 1):
        items = "".join(
            f"<li><b>{esc(source.get('title', ''))}</b><br>"
            f"<a href=\"{esc(source.get('url', ''))}\">{esc(source.get('url', ''))}</a>"
            f"<br><small>{esc(source.get('source_type', ''))} · "
            f"{esc(source.get('accessed_date', ''))}</small></li>"
            for source in chunk
        )
        pages.append(f"""
        <article class="page gold" id="sources-{index}">
          <header class="head">
            <span class="num">S</span>
            <div class="title-wrap">
              <div class="title-row"><h2>来源附件</h2><span class="part">PART {index} / {len(chunks)}</span></div>
              <div class="tags">
                <span class="tag">附件 <b>公开</b></span>
                <span class="tag">来源数量 <b>{len(sources)}</b></span>
                <span class="tag">研究日期 <b>{esc(data['meta']['research_date'])}</b></span>
              </div>
            </div>
          </header>
          <div class="signals">
            <div class="signal"><small>PRIMARY FIRST</small><strong>官方 / 论文 / 仓库</strong><span>优先一手来源</span></div>
            <div class="signal"><small>MEDIA</small><strong>融资与市场</strong><span>明确标记媒体披露</span></div>
            <div class="signal"><small>DYNAMIC</small><strong>记录访问日期</strong><span>避免历史口径冒充当前</span></div>
          </div>
          <div class="copy"><ol class="source-list" start="{(index - 1) * 10 + 1}">{items}</ol></div>
          <footer class="footer"><span>YY GTM LENS</span><span>{start_page + index - 1:02}</span></footer>
        </article>""")
    return pages


def public_html(data):
    meta = data["meta"]
    nav = "".join(
        f"<a href=\"#section-{section['number']}\"><span class=\"n\">{section['number']}</span>"
        f"<span class=\"label\">{esc(section.get('nav_label') or NAV_LABELS[section['number']])}</span></a>"
        for section in data["sections"]
    )
    pages = [cover_html(meta)]
    page_number = 2
    for section in data["sections"]:
        chunks = split_section(section)
        for part, blocks in enumerate(chunks, 1):
            pages.append(page_html(section, blocks, part, len(chunks), page_number))
            page_number += 1
        if section["number"] == "08":
            pages.append(opinion_page_html(page_number))
            page_number += 1
    source_pages = source_pages_html(data, page_number)
    pages.extend(source_pages)
    config = json.dumps({
        "slug": meta["output_slug"],
        "ownerViews": data.get("owner_views", []),
        "comments": data.get("comments", {}),
    }, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html><html lang="zh-CN"><head>
      <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
      <title>{esc(meta['company'])} 深度研究</title>
      <link rel="stylesheet" href="./styles.css?v=3">
      <link rel="stylesheet" href="./print.css?v=1" media="print">
    </head><body>
      <div class="progress" data-progress></div>
      <header class="topbar"><a class="brand" href="#top"><span class="mark"></span>
        <span><strong>YY GTM LENS</strong><small>AI 公司 × 增长 × GTM 研究</small></span></a>
        <div class="actions"><button class="btn" data-share>复制链接</button>
        <button class="btn primary" data-print>导出 PDF</button></div></header>
      <div class="layout"><aside class="nav"><small>CONTENTS</small>{nav}
        <a href="#sources-1"><span class="n">S</span><span class="label">来源附件</span></a>
        <div class="privacy">第 09 部分已物理分离，不进入公开网页、PDF 或发布包。</div>
      </aside><main class="report">{''.join(pages)}
        <section class="comments no-print"><div data-comments></div></section>
      </main></div>
      <script>window.REPORT_CONFIG={config};</script><script src="./app.js?v=1"></script>
    </body></html>"""


def private_html(data):
    meta = data["meta"]
    section = data["private_section"]
    pages = [cover_html(meta, private=True)]
    chunks = split_section(section)
    for index, blocks in enumerate(chunks, 1):
        pages.append(page_html(section, blocks, index, len(chunks), index + 1, private=True))
    return f"""<!doctype html><html lang="zh-CN"><head>
      <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
      <title>{esc(meta['company'])} 私密第 09 部分</title>
      <link rel="stylesheet" href="../public-site/styles.css?v=2">
      <link rel="stylesheet" href="../public-site/print.css?v=1" media="print">
    </head><body><main class="report"><div class="private-banner">仅限本人：不得发布或进入公开仓库。</div>
      {''.join(pages)}</main></body></html>"""


def copy_web_assets(skill_dir, public_site):
    template = skill_dir / "assets" / "web-template"
    for name in ("styles.css", "print.css", "app.js"):
        shutil.copy2(template / name, public_site / name)


def pdf_color(theme):
    from reportlab.lib.colors import HexColor
    return {
        "blue": HexColor("#F2F5FF"),
        "mint": HexColor("#EFFAF6"),
        "violet": HexColor("#F5F1FC"),
        "peach": HexColor("#FFF3ED"),
        "gold": HexColor("#FBF5E9"),
    }[theme]


def create_pdf(data, path, private=False):
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfgen import canvas
        from reportlab.platypus import Paragraph, Table, TableStyle
    except ImportError as exc:
        raise SystemExit(
            "reportlab is required for PDF rendering. Install it or run with --skip-pdf."
        ) from exc

    font_candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
        Path("/System/Library/AssetsV2/com_apple_MobileAsset_Font7/eb257c12d1a51c8c661b89f30eec56cacf9b8987.asset/AssetData/STHEITI.ttf"),
        Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttf"),
        Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
    ]
    font_path = next((candidate for candidate in font_candidates if candidate.exists()), None)
    if font_path and font_path.suffix.lower() == ".ttf":
        pdfmetrics.registerFont(TTFont("ReportCJK", str(font_path)))
        font = "ReportCJK"
    else:
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        font = "STSong-Light"
    page_w, page_h = A4
    title_style = ParagraphStyle(
        "title", fontName=font, fontSize=18, leading=22, textColor=colors.HexColor("#182235")
    )
    body_style = ParagraphStyle(
        "body", fontName=font, fontSize=8.5, leading=13.7, textColor=colors.HexColor("#34425A")
    )
    heading_style = ParagraphStyle(
        "heading", fontName=font, fontSize=11, leading=15, textColor=colors.HexColor("#182235")
    )
    source_style = ParagraphStyle(
        "source", fontName=font, fontSize=6.7, leading=9.5, textColor=colors.HexColor("#34425A")
    )
    c = canvas.Canvas(str(path), pagesize=A4)

    def background(theme):
        c.setFillColor(pdf_color(theme))
        c.rect(0, 0, page_w, page_h, stroke=0, fill=1)
        c.setStrokeColor(colors.Color(0.24, 0.32, 0.45, alpha=0.07))
        for x in range(12, 211, 16):
            c.line(x * mm, 0, x * mm, page_h)
        for y in range(12, 298, 16):
            c.line(0, y * mm, page_w, y * mm)

    def footer(page_no, label):
        c.setStrokeColor(colors.HexColor("#667FF0"))
        c.line(14 * mm, 10 * mm, 196 * mm, 10 * mm)
        c.setFont(font, 6)
        c.setFillColor(colors.HexColor("#748096"))
        c.drawString(14 * mm, 5.5 * mm, label)
        c.drawRightString(196 * mm, 5.5 * mm, f"{page_no:02}")

    def cover(page_no):
        c.setFillColor(colors.HexColor("#19233B"))
        c.rect(0, 0, page_w, page_h, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#B9C5FF"))
        c.setFont(font, 8)
        c.drawString(20 * mm, 252 * mm, "PRIVATE CAREER MEMO" if private else "AI-NATIVE COMPANY DEEP DIVE")
        c.setFillColor(colors.white)
        c.setFont(font, 29)
        c.drawString(20 * mm, 224 * mm, data["meta"]["company"])
        c.setFillColor(colors.HexColor("#A8E0D2"))
        c.setFont(font, 22)
        subtitle = Paragraph(esc(data["meta"]["subtitle"]), ParagraphStyle(
            "cover", fontName=font, fontSize=22, leading=27, textColor=colors.HexColor("#A8E0D2")
        ))
        subtitle.wrapOn(c, 155 * mm, 50 * mm)
        subtitle.drawOn(c, 20 * mm, 185 * mm)
        c.setFillColor(colors.HexColor("#D7DDEA"))
        c.setFont(font, 9)
        c.drawString(20 * mm, 168 * mm, f"研究截止 {data['meta']['research_date']}")
        footer(page_no, "PRIVATE REPORT" if private else "PUBLIC REPORT")
        c.showPage()

    def draw_tags(tags, y):
        x0, total_w, gap = 32 * mm, 164 * mm, 2 * mm
        card_w = (total_w - 2 * gap) / 3
        for index, item in enumerate(tags):
            x = x0 + index * (card_w + gap)
            c.setFillColor(colors.white)
            c.setStrokeColor(colors.HexColor("#D7DDEA"))
            c.roundRect(x, y - 7.5 * mm, card_w, 7.5 * mm, 3.5 * mm, fill=1, stroke=1)
            text = f"{item['label']}  {item['value']}"
            p = Paragraph(esc(text), ParagraphStyle(
                f"tag{index}", fontName=font, fontSize=6.6, leading=8,
                alignment=TA_CENTER, textColor=colors.HexColor("#34425A")
            ))
            _, h = p.wrap(card_w - 3 * mm, 6 * mm)
            p.drawOn(c, x + 1.5 * mm, y - 4.2 * mm - h / 2)
        return y - 7.5 * mm

    def draw_signals(signals, y):
        x0, total_w, gap = 32 * mm, 164 * mm, 2 * mm
        card_w = (total_w - 2 * gap) / 3
        for index, item in enumerate(signals):
            x = x0 + index * (card_w + gap)
            c.setFillColor(colors.white)
            c.setStrokeColor(colors.HexColor("#D7DDEA"))
            c.roundRect(x, y - 17 * mm, card_w, 17 * mm, 3.5 * mm, fill=1, stroke=1)
            c.setFont(font, 5.8)
            c.setFillColor(colors.HexColor("#748096"))
            c.drawString(x + 3 * mm, y - 4.3 * mm, str(item["label"])[:34])
            p = Paragraph(esc(item["value"]), ParagraphStyle(
                f"signal{index}", fontName=font, fontSize=11, leading=13,
                textColor=colors.HexColor("#182235")
            ))
            _, h = p.wrap(card_w - 6 * mm, 7 * mm)
            p.drawOn(c, x + 3 * mm, y - 10.5 * mm)
            c.setFont(font, 6.2)
            c.setFillColor(colors.HexColor("#748096"))
            c.drawString(x + 3 * mm, y - 14.5 * mm, str(item.get("note", ""))[:32])
        return y - 17 * mm

    def draw_block(block, x, y, width):
        kind = block.get("type")
        if kind == "paragraph":
            p = Paragraph(esc(block.get("text", "")), body_style)
            _, h = p.wrap(width, 100 * mm)
            p.drawOn(c, x, y - h)
            return y - h - 2.4 * mm
        if kind == "heading":
            p = Paragraph(esc(block.get("text", "")), heading_style)
            _, h = p.wrap(width, 30 * mm)
            p.drawOn(c, x, y - h)
            return y - h - 1.5 * mm
        if kind == "quote":
            p = Paragraph(esc(block.get("text", "")), body_style)
            _, h = p.wrap(width - 6 * mm, 50 * mm)
            c.setFillColor(colors.white)
            c.rect(x, y - h - 4 * mm, width, h + 4 * mm, stroke=0, fill=1)
            c.setFillColor(colors.HexColor("#8E72D2"))
            c.rect(x, y - h - 4 * mm, 1 * mm, h + 4 * mm, stroke=0, fill=1)
            p.drawOn(c, x + 3 * mm, y - h - 2 * mm)
            return y - h - 6 * mm
        if kind == "list":
            for idx, item in enumerate(block.get("items", []), 1):
                marker = f"{idx}." if block.get("ordered") else "•"
                p = Paragraph(f"{marker} {esc(item)}", body_style)
                _, h = p.wrap(width - 4 * mm, 50 * mm)
                p.drawOn(c, x + 2 * mm, y - h)
                y -= h + 1.2 * mm
            return y - 1 * mm
        if kind == "table":
            table = Table(
                [block.get("headers", [])] + block.get("rows", []),
                colWidths=[width / max(1, len(block.get("headers", [])))] * len(block.get("headers", [])),
            )
            table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), font),
                ("FONTSIZE", (0, 0), (-1, -1), 6.8),
                ("LEADING", (0, 0), (-1, -1), 9),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF1FA")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#34425A")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D7DDEA")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            _, h = table.wrap(width, 70 * mm)
            table.drawOn(c, x, y - h)
            return y - h - 2.5 * mm
        return y

    def draw_visual(visual, y, theme):
        items = visual.get("items", [])
        if not items:
            return
        x, width, height = 32 * mm, 164 * mm, 43 * mm
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor("#D7DDEA"))
        c.roundRect(x, y, width, height, 4 * mm, fill=1, stroke=1)
        if visual.get("type") == "bars":
            row_h = (height - 8 * mm) / max(1, len(items))
            for index, item in enumerate(items):
                cy = y + height - 5 * mm - index * row_h
                c.setFont(font, 6.4)
                c.setFillColor(colors.HexColor("#34425A"))
                c.drawString(x + 5 * mm, cy, str(item.get("label", ""))[:20])
                bx, bw = x + 34 * mm, width - 48 * mm
                c.setFillColor(colors.HexColor("#E8EBF2"))
                c.roundRect(bx, cy - 1 * mm, bw, 2.5 * mm, 1.2 * mm, fill=1, stroke=0)
                score = max(0, min(100, int(item.get("score", 0))))
                c.setFillColor(colors.HexColor("#667FF0"))
                c.roundRect(bx, cy - 1 * mm, bw * score / 100, 2.5 * mm, 1.2 * mm, fill=1, stroke=0)
                c.drawRightString(x + width - 5 * mm, cy, str(item.get("value", score)))
            return
        cols = 2 if visual.get("type") in {"matrix", "balance"} else min(4, max(2, len(items)))
        rows = math.ceil(len(items) / cols)
        gap = 2 * mm
        card_w = (width - 8 * mm - (cols - 1) * gap) / cols
        card_h = (height - 8 * mm - (rows - 1) * gap) / rows
        for index, item in enumerate(items):
            row, col = divmod(index, cols)
            cx = x + 4 * mm + col * (card_w + gap)
            cy = y + height - 4 * mm - (row + 1) * card_h - row * gap
            c.setFillColor(pdf_color(theme))
            c.roundRect(cx, cy, card_w, card_h, 3 * mm, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#748096"))
            c.setFont(font, 6)
            c.drawString(cx + 3 * mm, cy + card_h - 5 * mm, str(item.get("label", ""))[:24])
            c.setFillColor(colors.HexColor("#182235"))
            c.setFont(font, 9)
            c.drawString(cx + 3 * mm, cy + card_h - 12 * mm, str(item.get("value", ""))[:22])
            c.setFillColor(colors.HexColor("#748096"))
            c.setFont(font, 6)
            c.drawString(cx + 3 * mm, cy + 4 * mm, str(item.get("note", ""))[:28])

    def section_page(section, blocks, page_no, part, total):
        theme = section.get("theme") or THEMES[section["number"]]
        background(theme)
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor("#D7DDEA"))
        c.roundRect(14 * mm, 267 * mm, 12 * mm, 12 * mm, 4 * mm, fill=1, stroke=1)
        c.setFillColor(colors.HexColor("#4057C9"))
        c.setFont(font, 9)
        c.drawCentredString(20 * mm, 271.3 * mm, section["number"])
        title = Paragraph(esc(section["title"]), title_style)
        _, title_h = title.wrap(164 * mm, 28 * mm)
        title_y = 279 * mm - title_h
        title.drawOn(c, 32 * mm, title_y)
        c.setFillColor(colors.HexColor("#667FF0"))
        c.rect(32 * mm, title_y - 2.5 * mm, 18 * mm, 1 * mm, stroke=0, fill=1)
        if total > 1:
            c.setFont(font, 6.5)
            c.setFillColor(colors.HexColor("#748096"))
            c.drawString(32 * mm, title_y - 6 * mm, f"PART {part} / {total}")
            tag_y = title_y - 10 * mm
        else:
            tag_y = title_y - 5.7 * mm
        tags_bottom = draw_tags(section["tags"], tag_y)
        signals_top = tags_bottom - 4 * mm
        signals_bottom = draw_signals(section["signals"], signals_top)
        body_y = signals_bottom - 5 * mm
        x, width = 32 * mm, 164 * mm
        judgment = Paragraph(f"<b>判断：</b>{esc(section['judgment'])}", ParagraphStyle(
            "judgment", fontName=font, fontSize=9.3, leading=14,
            textColor=colors.HexColor("#182235")
        ))
        _, jh = judgment.wrap(width - 7 * mm, 35 * mm)
        c.setFillColor(colors.white)
        c.rect(x, body_y - jh - 5 * mm, width, jh + 5 * mm, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#667FF0"))
        c.rect(x, body_y - jh - 5 * mm, 1 * mm, jh + 5 * mm, stroke=0, fill=1)
        judgment.drawOn(c, x + 3.5 * mm, body_y - jh - 2.5 * mm)
        y = body_y - jh - 8 * mm
        for block in blocks:
            y = draw_block(block, x, y, width)
        visual_y = 19 * mm
        visual_top = visual_y + 43 * mm
        visual = section.get("visual", {}) if part == total else {}
        if visual.get("items"):
            if y < visual_top + 5 * mm:
                raise RuntimeError(
                    f"Section {section['number']} part {part} overflows the PDF page. "
                    "Add page_break_before to a complete block."
                )
            draw_visual(visual, visual_y, theme)
        elif y < 18 * mm:
            raise RuntimeError(
                f"Section {section['number']} part {part} overflows the PDF page."
            )
        footer(page_no, "PRIVATE DECISION MEMO" if private else "AI COMPANY FIELD NOTES")
        c.showPage()

    cover(1)
    page_no = 2
    sections = [data["private_section"]] if private else data["sections"]
    for section in sections:
        chunks = split_section(section)
        for part, blocks in enumerate(chunks, 1):
            section_page(section, blocks, page_no, part, len(chunks))
            page_no += 1

    if not private:
        sources = data.get("sources", [])
        for chunk_index in range(0, len(sources), 10):
            chunk = sources[chunk_index:chunk_index + 10]
            background("gold")
            c.setFillColor(colors.HexColor("#182235"))
            c.setFont(font, 18)
            c.drawString(32 * mm, 270 * mm, "来源附件")
            y = 252 * mm
            for source in chunk:
                text = (
                    f"<b>{esc(source.get('id'))}. {esc(source.get('title', ''))}</b><br/>"
                    f"{esc(source.get('url', ''))}<br/>"
                    f"{esc(source.get('source_type', ''))} · {esc(source.get('accessed_date', ''))}"
                )
                p = Paragraph(text, source_style)
                _, h = p.wrap(164 * mm, 30 * mm)
                if y - h < 18 * mm:
                    raise RuntimeError("Source page overflow; reduce source chunk size.")
                p.drawOn(c, 32 * mm, y - h)
                y -= h + 3 * mm
            footer(page_no, "AI COMPANY FIELD NOTES")
            c.showPage()
            page_no += 1
    c.save()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", required=True)
    parser.add_argument("--skip-pdf", action="store_true")
    args = parser.parse_args()
    input_path = Path(args.input).resolve()
    data = json.loads(input_path.read_text(encoding="utf-8"))
    output = Path(args.output).resolve()
    skill_dir = Path(__file__).resolve().parent.parent

    research_dir = output / "research"
    public_site = output / "public-site"
    private_notes = output / "private-notes"
    exports = output / "exports"
    publish = output / "publish"
    qa = output / "qa"
    for directory in (research_dir, public_site, private_notes, exports, publish, qa):
        directory.mkdir(parents=True, exist_ok=True)

    (research_dir / "public.md").write_text(report_markdown(data), encoding="utf-8")
    (research_dir / "private-09.md").write_text(
        report_markdown(data, private=True), encoding="utf-8"
    )
    (research_dir / "quality-review.md").write_text(
        quality_markdown(data), encoding="utf-8"
    )
    (public_site / "index.html").write_text(public_html(data), encoding="utf-8")
    (private_notes / "index.html").write_text(private_html(data), encoding="utf-8")
    copy_web_assets(skill_dir, public_site)

    if publish.exists():
        shutil.rmtree(publish)
    shutil.copytree(public_site, publish)

    slug = data["meta"]["output_slug"]
    if not args.skip_pdf:
        create_pdf(data, exports / f"{slug}-public.pdf")
        create_pdf(data, exports / f"{slug}-private-09.pdf", private=True)

    qa_text = f"""# Visual QA

- Status: pending
- Company: {data['meta']['company']}
- Research date: {data['meta']['research_date']}

Validate desktop, mobile, actual browser export, programmatic public PDF and private PDF separately.

Required:

- P0 = 0
- P1 = 0
- title/tag/signal overlap = 0 px
- page overflow = 0 px
- private-content leakage = 0
- one PNG per page plus a contact sheet
"""
    (qa / "visual-qa.md").write_text(qa_text, encoding="utf-8")
    shutil.copy2(skill_dir / "assets" / "visual-tokens.json", qa / "visual-tokens.json")
    print(f"Rendered {data['meta']['company']} to {output}")


if __name__ == "__main__":
    main()
