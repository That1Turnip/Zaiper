import os
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sync'))

load_dotenv()

WIDTH = 1080
HEIGHT = 1920
DURATION = 4
AUDIO_PATH = os.path.join(os.path.dirname(__file__), "background.mp3")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output.mp4")

def wrap_text(text, max_chars=22):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= max_chars:
            current += (" " if current else "") + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return "\n".join(lines)

def make_hook_frame():
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(10, 10, 10))
    draw = ImageDraw.Draw(img)

    try:
        font_xl = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 110)
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except:
        font_xl = ImageFont.load_default()
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    for i in range(0, HEIGHT, 60):
        draw.line([0, i, WIDTH, i], fill=(20, 20, 20), width=1)

    draw.rectangle([80, 300, WIDTH - 80, 900], fill=(20, 20, 20), outline=(60, 60, 60), width=2)

    draw.text((100, 340), "still copying", font=font_large, fill=(136, 136, 136))
    draw.text((100, 440), "assignments", font=font_large, fill=(136, 136, 136))
    draw.text((100, 540), "manually?", font=font_large, fill=(255, 255, 255))

    draw.rectangle([100, 660, WIDTH - 100, 670], fill=(255, 255, 255))

    draw.text((100, 700), "there's a", font=font_medium, fill=(136, 136, 136))
    draw.text((100, 760), "better way.", font=font_medium, fill=(100, 100, 255))

    draw.text((100, HEIGHT - 400), "Zaiper", font=font_xl, fill=(255, 255, 255))
    draw.text((100, HEIGHT - 280), "canvas → notion.", font=font_medium, fill=(136, 136, 136))
    draw.text((100, HEIGHT - 220), "automatically.", font=font_medium, fill=(100, 100, 255))
    draw.text((100, HEIGHT - 120), "zaiper.app ↓", font=font_small, fill=(80, 80, 80))

    return np.array(img)

def make_assignment_frame(assignment_name, course_name, due_date, index, total):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(10, 10, 10))
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        font_xs = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_xs = ImageFont.load_default()

    for i in range(0, HEIGHT, 60):
        draw.line([0, i, WIDTH, i], fill=(20, 20, 20), width=1)

    draw.rectangle([80, 120, WIDTH - 80, HEIGHT - 120], fill=(18, 18, 18), outline=(40, 40, 40), width=2)

    draw.rectangle([100, 140, 300, 200], fill=(100, 100, 255))
    draw.text((115, 150), f"{index} of {total}", font=font_xs, fill=(255, 255, 255))

    draw.text((100, 240), "due soon", font=font_small, fill=(136, 136, 136))

    wrapped = wrap_text(assignment_name, max_chars=20)
    draw.text((100, 320), wrapped, font=font_large, fill=(255, 255, 255))

    line_count = wrapped.count("\n") + 1
    y_after_title = 320 + (line_count * 90)

    draw.rectangle([100, y_after_title + 20, WIDTH - 100, y_after_title + 22], fill=(40, 40, 40))

    draw.text((100, y_after_title + 50), "course", font=font_xs, fill=(80, 80, 80))
    draw.text((100, y_after_title + 90), course_name, font=font_small, fill=(200, 200, 200))

    draw.text((100, y_after_title + 200), "due date", font=font_xs, fill=(80, 80, 80))
    if due_date:
        draw.text((100, y_after_title + 240), due_date[:10], font=font_medium, fill=(100, 100, 255))
    else:
        draw.text((100, y_after_title + 240), "No due date", font=font_medium, fill=(80, 80, 80))

    draw.rectangle([80, HEIGHT - 220, WIDTH - 80, HEIGHT - 120], fill=(20, 20, 40), outline=(60, 60, 120), width=2)
    draw.text((120, HEIGHT - 195), "sync this automatically →  zaiper.app", font=font_xs, fill=(100, 100, 255))

    return np.array(img)

def make_cta_frame():
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(10, 10, 40))
    draw = ImageDraw.Draw(img)

    try:
        font_xl = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 110)
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except:
        font_xl = ImageFont.load_default()
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.rectangle([80, 200, WIDTH - 80, HEIGHT - 200], fill=(15, 15, 50), outline=(80, 80, 200), width=3)

    draw.text((100, 260), "never miss", font=font_large, fill=(255, 255, 255))
    draw.text((100, 360), "a deadline", font=font_large, fill=(255, 255, 255))
    draw.text((100, 460), "again.", font=font_xl, fill=(100, 100, 255))

    draw.rectangle([100, 620, WIDTH - 100, 622], fill=(80, 80, 200))

    draw.text((100, 660), "Zaiper syncs your Canvas", font=font_small, fill=(180, 180, 255))
    draw.text((100, 710), "assignments to Notion", font=font_small, fill=(180, 180, 255))
    draw.text((100, 760), "automatically. Free.", font=font_small, fill=(255, 255, 255))

    draw.rectangle([100, HEIGHT - 500, WIDTH - 100, HEIGHT - 380], fill=(100, 100, 255))
    draw.text((200, HEIGHT - 470), "try it free →", font=font_medium, fill=(255, 255, 255))

    draw.text((100, HEIGHT - 320), "zaiper.app", font=font_large, fill=(255, 255, 255))
    draw.text((100, HEIGHT - 240), "link in bio ↑", font=font_small, fill=(136, 136, 136))

    return np.array(img)

def generate_video():
    print("Building engaging video...")

    assignments = [
        {"assignment_name": "Midterm Project", "course_name": "Computer Science 101", "due_date": "2026-06-01T23:59:00"},
        {"assignment_name": "Lab Report 3", "course_name": "Engineering Physics", "due_date": "2026-06-05T23:59:00"},
        {"assignment_name": "Algorithm Assignment", "course_name": "Data Structures", "due_date": "2026-06-10T23:59:00"},
    ]

    upcoming = [a for a in assignments if a["due_date"]][:5]

    clips = []

    hook = ImageClip(make_hook_frame()).set_duration(DURATION)
    hook = fadein(hook, 0.5)
    hook = fadeout(hook, 0.5)
    clips.append(hook)

    for i, a in enumerate(upcoming):
        frame = make_assignment_frame(a["assignment_name"], a["course_name"], a["due_date"], i + 1, len(upcoming))
        clip = ImageClip(frame).set_duration(DURATION)
        clip = fadein(clip, 0.5)
        clip = fadeout(clip, 0.5)
        clips.append(clip)

    cta = ImageClip(make_cta_frame()).set_duration(DURATION)
    cta = fadein(cta, 0.5)
    cta = fadeout(cta, 0.5)
    clips.append(cta)

    final = concatenate_videoclips(clips, method="compose")

    if os.path.exists(AUDIO_PATH):
        audio = AudioFileClip(AUDIO_PATH).subclip(0, final.duration).volumex(0.4)
        final = final.set_audio(audio)
        print("Audio added.")
    else:
        print("No audio file found — skipping music.")

    final.write_videofile(OUTPUT_PATH, fps=24, codec="libx264", audio_codec="aac")
    print(f"Video saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_video()