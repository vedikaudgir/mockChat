from PIL import Image, ImageDraw, ImageFont
import textwrap
import os


def load_icon(path, size):
    icon = Image.open(path).convert("RGBA")
    return icon.resize(size, Image.Resampling.LANCZOS)


def make_circle(image, size):
    image = image.resize(size).convert("RGBA")

    mask = Image.new("L", size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, size[0], size[1]), fill=255)

    final = Image.new("RGBA", size)
    final.paste(image, (0, 0), mask)

    return final


def renderWhatsApp(chat_id, messages, header, dp_path):
    width = 1080
    height = 2000
    padding = 20

    wallpaper = Image.open("utils/assets/whatsapp/wallpaper.png").resize((width, height))
    img = Image.new("RGB", (width, height))
    img.paste(wallpaper, (0, 0))

    draw = ImageDraw.Draw(img)

    name_font = ImageFont.truetype("static/fonts/Roboto-Regular.ttf", 48)
    status_font = ImageFont.truetype("static/fonts/Roboto-Regular.ttf", 32)
    msg_font = ImageFont.truetype("static/fonts/Roboto-Regular.ttf", 42)
    time_font = ImageFont.truetype("static/fonts/Roboto-Regular.ttf", 24)

    wa_green = (7, 94, 84)
    header_h = 200

    draw.rectangle((0, 0, width, header_h), fill=wa_green)

    back = load_icon("utils/assets/whatsapp/icons/back.png", (110, 110))
    img.paste(back, (5, 50), back)

    if dp_path and os.path.exists(dp_path):
        dp = Image.open(dp_path).convert("RGB").resize((130, 130))
        mask = Image.new("L", (130, 130), 0)
        m = ImageDraw.Draw(mask)
        m.ellipse((0, 0, 130, 130), fill=255)
        img.paste(dp, (100, 35), mask)

    name, status = header

    draw.text((260, 55), name, fill="white", font=name_font)
    draw.text((260, 125), status, fill=(220, 240, 220), font=status_font)

    video = load_icon("utils/assets/whatsapp/icons/video.png", (120, 120))
    call = load_icon("utils/assets/whatsapp/icons/call.png", (110, 110))
    menu = load_icon("utils/assets/whatsapp/icons/menu.png", (115, 115))

    img.paste(video, (width - 330, 45), video)
    img.paste(call,  (width - 210, 45), call)
    img.paste(menu,  (width - 110, 45), menu)

    y = header_h + 20
    max_w = int(width * 0.80)

    bubble_in = (255, 255, 255)
    bubble_out = (220, 248, 198)

    for sender, text, time, direction in messages:

        wrapped = textwrap.fill(text, width=26)
        bbox = draw.textbbox((0, 0), wrapped, font=msg_font)

        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        bubble_w = min(text_w + 170, max_w)
        bubble_h = max(text_h + 50, 50)

        if direction == "out":
            x = width - bubble_w - padding
            color = bubble_out
        else:
            x = padding
            color = bubble_in

        draw.rounded_rectangle(
            (x, y, x + bubble_w, y + bubble_h),
            radius=25,
            fill=color
        )

        draw.text((x + 35, y + 20), wrapped, font=msg_font, fill="black")

        if direction == "out":
            time_x = x + bubble_w - 80
            time_y = y + bubble_h - 35
        else:
            time_x = x + bubble_w - 80
            time_y = y + bubble_h - 40

        draw.text((time_x, time_y), time, font=time_font, fill=(80, 80, 80))

        y += bubble_h + 25

    bar_top = height - 150
    bar_bottom = height - 20

    draw.rounded_rectangle(
        (20, bar_top + 10, width - 170, bar_bottom - 10),
        radius=45,
        fill="white"
    )

    emoji = load_icon("utils/assets/whatsapp/icons/emoji.png", (70, 70))
    attach = load_icon("utils/assets/whatsapp/icons/attach.png", (80, 80))
    camera = load_icon("utils/assets/whatsapp/icons/camera.png", (90, 90))
    mic = load_icon("utils/assets/whatsapp/icons/mic.png", (100, 100))

    img.paste(emoji, (40, bar_top + 30), emoji)
    img.paste(attach, (110, bar_top + 30), attach)
    img.paste(camera, (width - 280, bar_top + 20), camera)

    mic_circle = make_circle(mic, (90, 90))
    img.paste(mic_circle, (width - 140, bar_top + 15), mic_circle)

    out_path = f"static/output/chat_{chat_id}.png"
    img.save(out_path)
    return out_path