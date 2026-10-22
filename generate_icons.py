import os
import math
from PIL import Image, ImageDraw

ICONS_DIR = os.path.join(os.path.dirname(__file__), "static", "icons")
os.makedirs(ICONS_DIR, exist_ok=True)

# 1. Create SVG Vector Logo
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080D1A"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00E5FF"/>
      <stop offset="50%" stop-color="#3B82F6"/>
      <stop offset="100%" stop-color="#8B5CF6"/>
    </linearGradient>
    <linearGradient id="coreGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#EF4444"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="14" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Background rounded hexagon / shield -->
  <rect width="512" height="512" rx="120" fill="url(#bgGrad)"/>
  <rect x="16" y="16" width="480" height="480" rx="108" fill="none" stroke="url(#ringGrad)" stroke-width="6" opacity="0.4"/>

  <!-- Outer Chronometer Dial -->
  <circle cx="256" cy="256" r="170" fill="none" stroke="url(#ringGrad)" stroke-width="12" filter="url(#glow)"/>
  <circle cx="256" cy="256" r="140" fill="none" stroke="#1E293B" stroke-width="4" stroke-dasharray="8 12"/>

  <!-- Hour markers -->
  <circle cx="256" cy="96" r="6" fill="#00E5FF"/>
  <circle cx="416" cy="256" r="6" fill="#3B82F6"/>
  <circle cx="256" cy="416" r="6" fill="#8B5CF6"/>
  <circle cx="96" cy="256" r="6" fill="#00E5FF"/>

  <!-- Dynamic Chronos Time Hands / Sentinel Sword -->
  <polygon points="256,120 270,256 256,275 242,256" fill="url(#ringGrad)"/>
  <polygon points="256,256 360,285 256,275" fill="#00E5FF" opacity="0.9"/>

  <!-- Radiant Core (Center) -->
  <circle cx="256" cy="256" r="28" fill="url(#coreGrad)" filter="url(#glow)"/>
  <circle cx="256" cy="256" r="12" fill="#FFFFFF"/>
</svg>
"""

with open(os.path.join(ICONS_DIR, "logo.svg"), "w", encoding="utf-8") as f:
    f.write(svg_content)

# 2. Render PNG Icons using Pillow (512x512 and 192x192)
def draw_chronos_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    scale = size / 512.0

    # Background rounded rect
    bg_color = (8, 13, 26, 255)
    r = int(120 * scale)
    draw.rounded_rectangle([0, 0, size, size], radius=r, fill=bg_color)

    # Border
    border_color = (0, 229, 255, 120)
    draw.rounded_rectangle([int(8*scale), int(8*scale), size-int(8*scale), size-int(8*scale)], radius=r-int(8*scale), outline=border_color, width=int(6*scale))

    # Outer Chronometer ring
    cx, cy = size // 2, size // 2
    radius = int(170 * scale)
    ring_color = (0, 229, 255, 230)
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=ring_color, width=int(12 * scale))

    # Inner dashed ring
    radius_inner = int(140 * scale)
    inner_color = (30, 41, 59, 255)
    draw.ellipse([cx - radius_inner, cy - radius_inner, cx + radius_inner, cy + radius_inner], outline=inner_color, width=int(4 * scale))

    # Dial marker dots
    dot_r = int(7 * scale)
    draw.ellipse([cx - dot_r, cy - radius - dot_r, cx + dot_r, cy - radius + dot_r], fill=(0, 229, 255, 255))
    draw.ellipse([cx + radius - dot_r, cy - dot_r, cx + radius + dot_r, cy + dot_r], fill=(59, 130, 246, 255))
    draw.ellipse([cx - dot_r, cy + radius - dot_r, cx + dot_r, cy + radius + dot_r], fill=(139, 92, 246, 255))
    draw.ellipse([cx - radius - dot_r, cy - dot_r, cx - radius + dot_r, cy + dot_r], fill=(0, 229, 255, 255))

    # Hour hand (Pointing up/north)
    p1 = (cx, int(120 * scale))
    p2 = (int(272 * scale), cx)
    p3 = (cx, int(278 * scale))
    p4 = (int(240 * scale), cx)
    draw.polygon([p1, p2, p3, p4], fill=(0, 229, 255, 255))

    # Minute hand
    m1 = (cx, cx)
    m2 = (int(360 * scale), int(290 * scale))
    m3 = (cx, int(275 * scale))
    draw.polygon([m1, m2, m3], fill=(59, 130, 246, 240))

    # Radiant Core
    core_r = int(28 * scale)
    draw.ellipse([cx - core_r, cy - core_r, cx + core_r, cy + core_r], fill=(245, 158, 11, 255))
    inner_core_r = int(12 * scale)
    draw.ellipse([cx - inner_core_r, cy - inner_core_r, cx + inner_core_r, cy + inner_core_r], fill=(255, 255, 255, 255))

    return img

icon_512 = draw_chronos_icon(512)
icon_512.save(os.path.join(ICONS_DIR, "icon-512.png"))

icon_192 = draw_chronos_icon(192)
icon_192.save(os.path.join(ICONS_DIR, "icon-192.png"))

# Favicon 64x64
favicon = draw_chronos_icon(64)
favicon.save(os.path.join(ICONS_DIR, "favicon.png"))
favicon.save(os.path.join(ICONS_DIR, "favicon.ico"), format="ICO")

# 3. Create University of the People Logo (Clean official blue crest with book & globe)
def draw_uopeople_icon():
    size = 128
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Deep Navy Blue circular background
    navy = (11, 35, 75, 255)
    gold = (212, 160, 23, 255)
    draw.ellipse([4, 4, 124, 124], fill=navy)
    draw.ellipse([8, 8, 120, 120], outline=gold, width=3)

    # Open Book
    # Left page
    draw.polygon([(64, 75), (28, 62), (28, 48), (64, 60)], fill=(255, 255, 255, 255))
    # Right page
    draw.polygon([(64, 75), (100, 62), (100, 48), (64, 60)], fill=(255, 255, 255, 255))

    # Globe meridian arcs above book
    draw.arc([44, 24, 84, 64], start=0, end=360, fill=gold, width=2)
    draw.line([(64, 24), (64, 64)], fill=gold, width=2)
    draw.line([(44, 44), (84, 44)], fill=gold, width=2)

    # "UoPeople" text or initial "U"
    draw.rectangle([54, 84, 74, 98], fill=gold)
    draw.rectangle([58, 84, 70, 94], fill=navy)

    return img

uop_img = draw_uopeople_icon()
uop_img.save(os.path.join(ICONS_DIR, "uopeople.png"))

print("All icons successfully generated in static/icons/")
