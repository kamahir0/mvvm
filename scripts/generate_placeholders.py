import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio

os.makedirs("public/images", exist_ok=True)
os.makedirs("public/videos", exist_ok=True)

# Fonts
FONT_JP_PATH = "C:/Windows/Fonts/meiryo.ttc"
FONT_EN_PATH = "C:/Windows/Fonts/arial.ttf"

def get_font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_JP_PATH, size)
    except Exception:
        return ImageFont.load_default()

def draw_header_badge(draw, text, width, color=(46, 125, 50)):
    # Draw top banner badge
    draw.rectangle([0, 0, width, 40], fill=(20, 24, 33))
    draw.rectangle([10, 8, width - 10, 34], fill=color)
    f = get_font(16)
    draw.text((20, 10), text, fill=(255, 255, 255), font=f)

# ==========================================
# 1. party_status_tabs.png (800x480)
# ==========================================
def create_party_status_tabs():
    w, h = 800, 480
    img = Image.new("RGB", (w, h), (26, 30, 42))
    draw = ImageDraw.Draw(img)

    draw_header_badge(draw, "【スクショ置換予定】 Presentationにしかない状態（パーティステータスUI）", w, (16, 137, 255))

    # Tabs
    tab_y = 60
    tabs = [
        ("Alice  Lv.42", False),
        ("★ Bob  Lv.45  (Selected) ★", True),
        ("Carol  Lv.40", False),
    ]
    cur_x = 40
    for title, selected in tabs:
        tw = 220 if selected else 160
        bg_col = (45, 90, 140) if selected else (38, 44, 58)
        border_col = (100, 180, 255) if selected else (60, 70, 90)
        draw.rectangle([cur_x, tab_y, cur_x + tw, tab_y + 45], fill=bg_col, outline=border_col, width=2 if selected else 1)
        f = get_font(15)
        draw.text((cur_x + 15, tab_y + 12), title, fill=(255, 255, 255) if selected else (160, 170, 190), font=f)
        cur_x += tw + 12

    # Main content panel
    draw.rectangle([40, tab_y + 45, w - 40, h - 70], fill=(32, 38, 52), outline=(100, 180, 255), width=2)

    # Left: Character Avatar Placeholder
    draw.rectangle([70, tab_y + 70, 270, tab_y + 310], fill=(22, 26, 36), outline=(80, 100, 130), width=1)
    # Silhouette or wireframe circle & body
    draw.ellipse([140, tab_y + 100, 200, tab_y + 160], fill=(50, 65, 85))
    draw.polygon([(110, tab_y + 240), (230, tab_y + 240), (170, tab_y + 160)], fill=(50, 65, 85))
    draw.text((105, tab_y + 260), "Bob (Character Model)", fill=(140, 160, 180), font=get_font(13))

    # Right: Character Status
    f_title = get_font(24)
    draw.text((310, tab_y + 70), "Bob", fill=(255, 255, 255), font=f_title)
    f_sub = get_font(15)
    draw.text((380, tab_y + 78), "Paladin / Frontline", fill=(140, 160, 190), font=f_sub)

    # HP Gauge
    draw.text((310, tab_y + 120), "HP: 1,800 / 1,800", fill=(200, 220, 240), font=get_font(15))
    draw.rectangle([310, tab_y + 145, 730, tab_y + 165], fill=(20, 24, 32))
    draw.rectangle([310, tab_y + 145, 730, tab_y + 165], fill=(52, 199, 89))  # Full HP green

    # Stats Grid
    stats = [
        ("ATK", "340", "DEF", "420"),
        ("SPD", "115", "M-DEF", "310"),
        ("CRIT", "12%", "STATUS", "Normal")
    ]
    sy = tab_y + 190
    for s in stats:
        draw.text((310, sy), f"{s[0]}: {s[1]}", fill=(180, 195, 215), font=get_font(16))
        draw.text((520, sy), f"{s[2]}: {s[3]}", fill=(180, 195, 215), font=get_font(16))
        sy += 32

    # Bottom annotation
    draw.rectangle([40, h - 55, w - 40, h - 15], fill=(30, 48, 70), outline=(50, 120, 200))
    f_ann = get_font(14)
    draw.text((55, h - 47), "💡 ViewModelの役割: 「今Bobを見ている(SelectedMember=Bob)」という表示上の状態を持つ", fill=(180, 220, 255), font=f_ann)

    img.save("public/images/party_status_tabs.png")
    print("Created party_status_tabs.png")

# ==========================================
# 2. player_exploration.png (600x400)
# ==========================================
def create_player_exploration():
    w, h = 600, 400
    img = Image.new("RGB", (w, h), (24, 28, 38))
    draw = ImageDraw.Draw(img)

    draw_header_badge(draw, "【スクショ置換予定】 Simulation Actor (探索プレイヤー)", w, (220, 80, 60))

    # Ground Grid Perspective
    for i in range(0, w + 100, 50):
        draw.line([(i, 200), ((i - 300) * 2 + 300, h)], fill=(40, 48, 65), width=1)
    for y in [220, 250, 290, 340, h]:
        draw.line([(0, y), (w, y)], fill=(40, 48, 65), width=1)

    # Obstacle / Wall
    draw.rectangle([420, 180, 540, 300], fill=(50, 60, 80), outline=(180, 70, 70), width=2)
    draw.text((435, 230), "Wall Collider", fill=(255, 120, 120), font=get_font(14))

    # Player Capsule at center
    px, py = 240, 250
    # Shadow
    draw.ellipse([px - 35, py + 35, px + 35, py + 55], fill=(15, 18, 25))
    # Body
    draw.rectangle([px - 25, py - 40, px + 25, py + 40], fill=(60, 140, 220), outline=(120, 200, 255), width=2)
    draw.ellipse([px - 25, py - 60, px + 25, py - 20], fill=(60, 140, 220), outline=(120, 200, 255), width=2)
    draw.text((px - 20, py - 5), "Player", fill=(255, 255, 255), font=get_font(14))

    # Vector arrows
    # Input Vector
    draw.line([(px, py), (px + 90, py - 30)], fill=(255, 215, 0), width=3)
    draw.polygon([(px + 95, py - 32), (px + 82, py - 38), (px + 85, py - 22)], fill=(255, 215, 0))
    draw.text((px + 45, py - 55), "L-Stick Input", fill=(255, 215, 0), font=get_font(13))

    # Velocity Vector
    draw.line([(px, py), (px + 70, py)], fill=(80, 220, 120), width=2)
    draw.text((px + 30, py + 8), "Velocity", fill=(80, 220, 120), font=get_font(12))

    # Physics Raycast / Collision
    draw.line([(px + 25, py), (420, py)], fill=(255, 80, 80), width=2)
    draw.ellipse([415, py - 5, 425, py + 5], fill=(255, 50, 50))
    draw.text((310, py - 18), "Collision!", fill=(255, 100, 100), font=get_font(12))

    # Status HUD overlay
    draw.rectangle([20, 50, 260, 130], fill=(18, 22, 30, 200), outline=(70, 80, 100))
    draw.text((30, 58), "Transform.position = (14.2, 0.0, -8.1)", fill=(180, 200, 220), font=get_font(11))
    draw.text((30, 78), "CharacterController.Move(...)", fill=(180, 200, 220), font=get_font(11))
    draw.text((30, 98), "▶ 自ら世界の状態を更新する (Simulation)", fill=(255, 130, 130), font=get_font(11))

    img.save("public/images/player_exploration.png")
    print("Created player_exploration.png")

# ==========================================
# 3. battle_presentation.png (600x400)
# ==========================================
def create_battle_presentation():
    w, h = 600, 400
    img = Image.new("RGB", (w, h), (22, 26, 36))
    draw = ImageDraw.Draw(img)

    draw_header_badge(draw, "【スクショ置換予定】 View / Presentation (ターン制バトル演出)", w, (46, 160, 90))

    # Battle field background
    draw.rectangle([0, 220, w, h], fill=(28, 34, 46))
    draw.line([(0, 220), (w, 220)], fill=(50, 60, 80), width=2)

    # Player Character (Right attacking Left or Left attacking Right)
    px, py = 120, 220
    # Sword slashing pose
    draw.ellipse([px - 20, py - 50, px + 20, py - 10], fill=(70, 130, 200))
    draw.rectangle([px - 15, py - 10, px + 15, py + 50], fill=(70, 130, 200))
    # Slash Arc
    draw.arc([px + 10, py - 80, px + 190, py + 70], start=300, end=40, fill=(120, 220, 255), width=5)

    # Enemy Monster
    ex, ey = 420, 200
    draw.rectangle([ex - 40, ey - 60, ex + 40, ey + 60], fill=(180, 60, 60), outline=(230, 100, 100), width=2)
    draw.text((ex - 35, ey - 10), "Dragon", fill=(255, 255, 255), font=get_font(16))

    # Damage Popup (Big!)
    draw.rectangle([ex - 80, ey - 110, ex + 80, ey - 65], fill=(240, 180, 0), outline=(255, 255, 255), width=2)
    f_dmg = get_font(20)
    draw.text((ex - 65, ey - 105), "9,999 DMG!", fill=(0, 0, 0), font=f_dmg)

    # Model Decision Box overlay
    draw.rectangle([20, 50, 340, 130], fill=(18, 22, 30), outline=(70, 80, 100))
    draw.text((30, 58), "BattleModel: 攻撃結果は既に計算完了", fill=(180, 200, 220), font=get_font(12))
    draw.text((30, 80), "3Dキャラ & エフェクトは『結果を表現』している", fill=(180, 200, 220), font=get_font(12))
    draw.text((30, 102), "▶ 決定済み状態の投影 = Viewとして扱いやすい", fill=(100, 230, 140), font=get_font(12))

    img.save("public/images/battle_presentation.png")
    print("Created battle_presentation.png")

# ==========================================
# 4. quest_area_trigger.png (800x450)
# ==========================================
def create_quest_area_trigger():
    w, h = 800, 450
    img = Image.new("RGB", (w, h), (24, 28, 38))
    draw = ImageDraw.Draw(img)

    draw_header_badge(draw, "【スクショ置換予定】 クエスト到達条件（SimulationとModelの境界）", w, (180, 100, 40))

    # 3D Wireframe Scene (Temple Silhouette)
    # Ground
    draw.polygon([(0, 200), (w, 200), (w, h), (0, h)], fill=(28, 34, 46))
    # Temple structure in background
    tx, ty = 480, 120
    draw.rectangle([tx, ty, tx + 180, ty + 150], fill=(38, 46, 62), outline=(70, 85, 115), width=2)
    draw.polygon([(tx - 20, ty), (tx + 90, ty - 50), (tx + 200, ty)], fill=(48, 58, 78), outline=(70, 85, 115))
    draw.text((tx + 30, ty + 60), "神殿の入口 (Temple)", fill=(180, 200, 230), font=get_font(14))

    # Trigger Sphere / Circle (Gizmo style)
    trig_x, trig_y = 570, 280
    draw.ellipse([trig_x - 120, trig_y - 45, trig_x + 120, trig_y + 45], outline=(50, 220, 100), width=3)
    draw.ellipse([trig_x - 100, trig_y - 35, trig_x + 100, trig_y + 35], fill=(30, 80, 50, 60))
    draw.text((trig_x - 70, trig_y - 10), "Trigger Collider Area", fill=(100, 255, 150), font=get_font(13))

    # Player inside the area
    px, py = trig_x - 20, trig_y - 10
    draw.ellipse([px - 15, py - 30, px + 15, py], fill=(70, 150, 240))
    draw.text((px - 25, py + 5), "Player", fill=(255, 255, 255), font=get_font(12))

    # Flowchart / Interpretation Box on Left
    bx, by = 40, 60
    draw.rectangle([bx, by, bx + 360, by + 340], fill=(18, 22, 32), outline=(80, 100, 130), width=1)

    steps = [
        ("1. Observation (Simulation)", "Transform.position = (127.3, 2.0, -83.5)", (160, 180, 200)),
        ("2. Spatial Check (Simulation)", "IsInsideArea(TempleEntrance) == true", (100, 220, 140)),
        ("3. Meaningful Event (Model)", "ReachedLocation(TempleEntrance)", (255, 215, 0)),
        ("4. Quest State Update (Model)", "QuestCondition: Cleared! → Next Step", (255, 130, 100))
    ]
    cur_y = by + 20
    for title, desc, col in steps:
        draw.text((bx + 15, cur_y), title, fill=col, font=get_font(13))
        draw.rectangle([bx + 15, cur_y + 22, bx + 345, cur_y + 55], fill=(26, 32, 46))
        draw.text((bx + 25, cur_y + 28), desc, fill=(230, 240, 255), font=get_font(12))
        cur_y += 75

    # Quest Notification popup UI at top right
    draw.rectangle([w - 280, 60, w - 30, 115], fill=(35, 60, 45), outline=(60, 200, 100), width=2)
    draw.text((w - 265, 68), "🔔 QUEST UPDATED", fill=(100, 255, 140), font=get_font(13))
    draw.text((w - 265, 88), "古代の神殿に到達した！", fill=(255, 255, 255), font=get_font(14))

    img.save("public/images/quest_area_trigger.png")
    print("Created quest_area_trigger.png")

# ==========================================
# 5. limit_break_demo.mp4 & .gif (640x360, 30fps, 4s = 120 frames)
# ==========================================
def create_limit_break_video():
    w, h = 640, 360
    fps = 30
    total_frames = 120  # 4 seconds

    frames = []

    for f in range(total_frames):
        img = Image.new("RGB", (w, h), (20, 24, 34))
        draw = ImageDraw.Draw(img)

        draw_header_badge(draw, "【動画置換予定】 限界突破演出（Model即時 vs 演出後のreveal）", w, (200, 80, 160))

        # Time phase
        # 0 - 30: Ready (2凸) -> Click
        # 31 - 70: API OK -> Animation Playing (Still 2凸 on screen!)
        # 71 - 100: REVEAL! Flash -> Apply VM -> 3凸!
        # 101 - 120: Finished (3凸)

        t_sec = f / fps

        # Timeline indicator at bottom
        draw.rectangle([30, h - 50, w - 30, h - 35], fill=(35, 42, 58))
        progress = (f / total_frames) * (w - 60)
        draw.rectangle([30, h - 50, 30 + progress, h - 35], fill=(220, 100, 180))

        # Phase description bar
        if f < 30:
            phase_name = "0.0s: ユーザーが「限界突破」ボタンを押す"
            phase_col = (180, 200, 220)
        elif f < 70:
            phase_name = "1.0s: API成功(Modelは3凸確定) だが画面は演出中！まだ2凸表示"
            phase_col = (255, 200, 80)
        elif f < 95:
            phase_name = "2.5s: ★★★ REVEAL! ここで初めてViewModelを3凸に更新！ ★★★"
            phase_col = (100, 255, 160)
        else:
            phase_name = "3.5s: 演出完了（表示上の現在 = 3凸）"
            phase_col = (150, 220, 255)

        draw.text((35, h - 30), phase_name, fill=phase_col, font=get_font(12))

        # Main character card / display
        cx, cy = w // 2, 170

        if f >= 71:
            # Star 3
            card_border = (255, 215, 0)
            stars_text = "★ ★ ★  (3凸)"
            stars_col = (255, 220, 50)
            lv_text = "Lv. 70 / 70"
            status_tag = "ViewModel: 3凸に更新完了"
            status_tag_col = (100, 255, 140)
        else:
            # Star 2
            card_border = (100, 140, 200)
            stars_text = "★ ★ ☆  (2凸)"
            stars_col = (180, 200, 240)
            lv_text = "Lv. 60 / 60"
            status_tag = "ViewModel: 2凸を表示中"
            status_tag_col = (180, 200, 220)

        # Card frame
        draw.rectangle([cx - 150, cy - 80, cx + 150, cy + 80], fill=(28, 34, 48), outline=card_border, width=2)
        draw.text((cx - 70, cy - 65), stars_text, fill=stars_col, font=get_font(20))
        draw.text((cx - 45, cy - 25), lv_text, fill=(255, 255, 255), font=get_font(18))

        # Status badge under card
        draw.rectangle([cx - 130, cy + 30, cx + 130, cy + 65], fill=(18, 22, 32))
        draw.text((cx - 110, cy + 38), status_tag, fill=status_tag_col, font=get_font(13))

        # Animation visual effect
        if 31 <= f < 71:
            # Pulsing circles (charging energy)
            pulse_radius = int(50 + (f - 31) * 3) % 90 + 30
            draw.ellipse([cx - pulse_radius, cy - pulse_radius, cx + pulse_radius, cy + pulse_radius], outline=(255, 180, 50), width=2)
            draw.text((cx - 60, cy - 115), "⚡ 演出中: 暗転 & 昇格待機 ⚡", fill=(255, 180, 50), font=get_font(13))
        elif 71 <= f < 85:
            # Flash burst
            burst_r = int((f - 71) * 20) + 40
            draw.ellipse([cx - burst_r, cy - burst_r, cx + burst_r, cy + burst_r], outline=(255, 255, 255), width=4)
            draw.text((cx - 50, cy - 115), "💥 REVEAL!! 💥", fill=(255, 255, 100), font=get_font(18))

        # Model vs Presentation state display
        draw.rectangle([30, 55, 230, 115], fill=(22, 26, 36), outline=(60, 70, 90))
        m_val = "★3 (確定)" if f >= 30 else "★2"
        p_val = "★3 (表示)" if f >= 71 else "★2 (演出待機)"
        draw.text((40, 62), f"Model側の現在:       {m_val}", fill=(255, 180, 100) if f>=30 else (180, 190, 210), font=get_font(11))
        draw.text((40, 85), f"Presentationの現在:  {p_val}", fill=(100, 255, 160) if f>=71 else (180, 190, 210), font=get_font(11))

        frames.append(np.array(img))

    # Save MP4
    mp4_path = "public/videos/limit_break_demo.mp4"
    imageio.mimwrite(mp4_path, frames, fps=fps, codec='libx264', quality=8)
    print("Created limit_break_demo.mp4")

    # Save GIF (subsample every 2 frames for lightweight preview)
    gif_frames = [Image.fromarray(frm) for frm in frames[::2]]
    gif_path = "public/images/limit_break_demo.gif"
    gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:], duration=int(1000/(fps/2)), loop=0)
    print("Created limit_break_demo.gif")

if __name__ == "__main__":
    create_party_status_tabs()
    create_player_exploration()
    create_battle_presentation()
    create_quest_area_trigger()
    create_limit_break_video()
    print("All placeholders generated successfully!")
