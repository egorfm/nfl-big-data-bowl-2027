#!/usr/bin/env python3
"""
Generates illustrative, publication-quality formula graphics for NFL Big Data Bowl 2027 READMEs (EN and RU).
Theme: Modern dark sports-analytics card matching GitHub and NextGenStats aesthetic.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

# Set global styles
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

OUTPUT_DIR = "/Users/egor/.gemini/antigravity/scratch/nfl-big-data-bowl-2027/reports/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BG_COLOR = "#0e1117"
CARD_COLOR = "#161b22"
BORDER_COLOR = "#30363d"
PANEL_COLOR = "#0d1117"
TEXT_COLOR = "#c9d1d9"
WHITE = "#ffffff"
CYAN = "#58a6ff"
CRIMSON = "#f85149"
GOLD = "#e3b341"
GREEN = "#3fb950"
GRAY = "#8b949e"
PURPLE = "#bc8cff"


def create_tangential_card(lang='en'):
    fig = plt.figure(figsize=(12, 4.8), facecolor=BG_COLOR, dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.8)
    ax.axis('off')

    # Background card
    card = FancyBboxPatch((0.2, 0.2), 11.6, 4.4, boxstyle="round,pad=0.1,rounding_size=0.25",
                          facecolor=CARD_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5)
    ax.add_patch(card)

    if lang == 'en':
        title = "1. TANGENTIAL ACCELERATION (a_t) & BRAKING ISOLATION"
        subtitle = "Isolates longitudinal braking force along route path from centripetal turning forces"
        formula_main = r"$a_t = \frac{\mathbf{v} \cdot \mathbf{a}}{\|\mathbf{v}\|} = \frac{v_x a_x + v_y a_y}{\sqrt{v_x^2 + v_y^2}}$"
        label_v = r"Velocity $\mathbf{v}$"
        label_at = r"Tangential $a_t < 0$"
        label_at_sub = "(Braking Force)"
        label_an = r"Normal $a_n$ (Turning)"
        label_a = r"Net Accel $\mathbf{a}$"
        box1_title = r"$a_t > 0$ : Acceleration"
        box1_sub = "Propulsive push phase"
        box2_title = r"$a_t < -1.5\ \mathrm{yd/s^2}$ : Braking"
        box2_sub = "Active deceleration trigger"
        vector_panel_title = "Kinematic Vector Decomposition"
        route_label = "Route Direction"
    else:
        title = "1. ТАНГЕНЦИАЛЬНОЕ УСКОРЕНИЕ (a_t) И ИЗОЛЯЦИЯ ТОРМОЖЕНИЯ"
        subtitle = "Изолирует продольное торможение вдоль траектории от центростремительного поворота"
        formula_main = r"$a_t = \frac{\mathbf{v} \cdot \mathbf{a}}{\|\mathbf{v}\|} = \frac{v_x a_x + v_y a_y}{\sqrt{v_x^2 + v_y^2}}$"
        label_v = r"Скорость $\mathbf{v}$"
        label_at = r"Тангенциальное $a_t < 0$"
        label_at_sub = "(Тормозное усилие)"
        label_an = r"Нормальное $a_n$ (Поворот)"
        label_a = r"Полное ускорение $\mathbf{a}$"
        box1_title = r"$a_t > 0$ : Разгон"
        box1_sub = "Тяговая фаза движения"
        box2_title = r"$a_t < -1.5\ \mathrm{yd/s^2}$ : Торможение"
        box2_sub = "Порог активного сброса скорости"
        vector_panel_title = "Векторная декомпозиция сил"
        route_label = "Направление маршрута"

    # Header
    ax.text(0.6, 4.25, title, fontsize=13.5, fontweight='bold', color=WHITE)
    ax.text(0.6, 3.88, subtitle, fontsize=9.5, color=GRAY)

    # Left Panel: Formula Display Card
    form_box = FancyBboxPatch((0.5, 2.05), 5.5, 1.5, boxstyle="round,pad=0.08,rounding_size=0.15",
                              facecolor=PANEL_COLOR, edgecolor=BORDER_COLOR, linewidth=1.2)
    ax.add_patch(form_box)
    ax.text(3.25, 2.80, formula_main, fontsize=15.5, color=CYAN, ha='center', va='center')

    # Interpretation badges below formula
    # Badge 1: Acceleration
    b1 = FancyBboxPatch((0.5, 0.55), 2.65, 1.25, boxstyle="round,pad=0.06,rounding_size=0.12",
                        facecolor="#122619", edgecolor="#238636", linewidth=1.0)
    ax.add_patch(b1)
    ax.text(0.65, 1.45, box1_title, fontsize=9.5, fontweight='bold', color=GREEN)
    ax.text(0.65, 0.95, box1_sub, fontsize=8.5, color="#85e89d")

    # Badge 2: Braking
    b2 = FancyBboxPatch((3.35, 0.55), 2.65, 1.25, boxstyle="round,pad=0.06,rounding_size=0.12",
                        facecolor="#2b1419", edgecolor="#da3633", linewidth=1.0)
    ax.add_patch(b2)
    ax.text(3.5, 1.45, box2_title, fontsize=9.5, fontweight='bold', color=CRIMSON)
    ax.text(3.5, 0.95, box2_sub, fontsize=8.5, color="#ff7b72")

    # Right Panel: Vector Diagram
    diag_box = FancyBboxPatch((6.3, 0.55), 5.2, 3.0, boxstyle="round,pad=0.08,rounding_size=0.15",
                              facecolor=PANEL_COLOR, edgecolor=BORDER_COLOR, linewidth=1.2)
    ax.add_patch(diag_box)
    ax.text(8.9, 3.25, vector_panel_title, fontsize=10.5, fontweight='bold', color=WHITE, ha='center')

    # Origin point (WR position)
    px, py = 8.8, 1.85
    ax.scatter([px], [py], s=120, color=WHITE, edgecolors=CYAN, linewidth=2.5, zorder=10)
    ax.text(px + 0.1, py - 0.3, "WR (Player)", fontsize=8.5, fontweight='bold', color=WHITE, ha='left')

    # Velocity vector v (pointing along path)
    vx, vy = 1.6, 0.50
    arrow_v = FancyArrowPatch((px, py), (px + vx, py + vy),
                              arrowstyle="simple,head_width=6,head_length=8",
                              color=CYAN, linewidth=2.5, zorder=8)
    ax.add_patch(arrow_v)
    ax.text(px + vx/2 + 0.05, py + vy/2 + 0.25, label_v, fontsize=8.5, fontweight='bold', color=CYAN, ha='center')

    # Deceleration tangential component a_t (pointing backwards opposite to v!)
    at_x, at_y = -1.3, -0.40
    arrow_at = FancyArrowPatch((px, py), (px + at_x, py + at_y),
                               arrowstyle="simple,head_width=6,head_length=8",
                               color=CRIMSON, linewidth=2.5, zorder=9)
    ax.add_patch(arrow_at)
    ax.text(px + at_x - 0.15, py + at_y + 0.18, label_at, fontsize=8, fontweight='bold', color=CRIMSON, ha='right')
    ax.text(px + at_x - 0.15, py + at_y - 0.06, label_at_sub, fontsize=7.5, color="#ff7b72", ha='right')

    # Normal component a_n (perpendicular to v)
    an_x, an_y = -0.35, 1.1
    arrow_an = FancyArrowPatch((px, py), (px + an_x, py + an_y),
                               arrowstyle="simple,head_width=5,head_length=7",
                               color=PURPLE, linewidth=2.0, zorder=8)
    ax.add_patch(arrow_an)
    ax.text(px + an_x, py + an_y + 0.15, label_an, fontsize=8, color=PURPLE, ha='center')

    # Net acceleration vector a = a_t + a_n
    net_x, net_y = at_x + an_x, at_y + an_y
    arrow_a = FancyArrowPatch((px, py), (px + net_x, py + net_y),
                              arrowstyle="simple,head_width=6,head_length=8",
                              color=GOLD, linewidth=2.2, zorder=8)
    ax.add_patch(arrow_a)
    ax.text(px + net_x - 0.15, py + net_y + 0.05, label_a, fontsize=8, fontweight='bold', color=GOLD, ha='right', va='center')

    # Dashed parallelogram for vector sum
    ax.plot([px + at_x, px + net_x], [py + at_y, py + net_y], color=GOLD, linestyle="--", linewidth=0.9, alpha=0.4)
    ax.plot([px + an_x, px + net_x], [py + an_y, py + net_y], color=GOLD, linestyle="--", linewidth=0.9, alpha=0.4)
    ax.text(11.2, 0.75, route_label, fontsize=7.5, color=GRAY, ha='right', style='italic')

    filename = f"formula_tangential_acceleration_{lang}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=200, facecolor=BG_COLOR, edgecolor='none')
    plt.close()
    print(f"Generated {filepath}")


def create_centripetal_card(lang='en'):
    fig = plt.figure(figsize=(12, 4.8), facecolor=BG_COLOR, dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.8)
    ax.axis('off')

    # Background card
    card = FancyBboxPatch((0.2, 0.2), 11.6, 4.4, boxstyle="round,pad=0.1,rounding_size=0.25",
                          facecolor=CARD_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5)
    ax.add_patch(card)

    if lang == 'en':
        title = "2. CENTRIPETAL ACCELERATION (a_n) & ROUTE CURVATURE (κ)"
        subtitle = "Measures cornering sharpness and lateral G-force at the route inflection stem"
        form1 = r"$a_n = \frac{|v_x a_y - v_y a_x|}{\sqrt{v_x^2 + v_y^2}} = \kappa \cdot \|\mathbf{v}\|^2$"
        form2 = r"$\kappa = \frac{|v_x a_y - v_y a_x|}{(v_x^2 + v_y^2)^{3/2}} = \frac{1}{R_{\mathrm{cut}}}$"
        panel_diag_title = "Route Break Curvature Dynamics"
        lbl_r = r"Turn Radius $R = 1/\kappa$"
        lbl_an = r"Lateral Force $a_n$"
        lbl_v = r"Speed $\mathbf{v}$"
        pt_break = "Break Point (Cut)"
        box_desc = "Decouples directional redirection (turning) from deceleration (stopping)."
    else:
        title = "2. ЦЕНТРОСТРЕМИТЕЛЬНОЕ УСКОРЕНИЕ (a_n) И КРИВИЗНА МАРШРУТА (κ)"
        subtitle = "Оценивает резкость угла среза и боковую перегрузку в точке перелома маршрута"
        form1 = r"$a_n = \frac{|v_x a_y - v_y a_x|}{\sqrt{v_x^2 + v_y^2}} = \kappa \cdot \|\mathbf{v}\|^2$"
        form2 = r"$\kappa = \frac{|v_x a_y - v_y a_x|}{(v_x^2 + v_y^2)^{3/2}} = \frac{1}{R_{\mathrm{cut}}}$"
        panel_diag_title = "Динамика искривления траектории"
        lbl_r = r"Радиус срезки $R = 1/\kappa$"
        lbl_an = r"Боковая сила $a_n$"
        lbl_v = r"Скорость $\mathbf{v}$"
        pt_break = "Точка срезки (Cut)"
        box_desc = "Разделяет смену направления (поворот) и сброс скорости (торможение)."

    # Header
    ax.text(0.6, 4.25, title, fontsize=13.5, fontweight='bold', color=WHITE)
    ax.text(0.6, 3.88, subtitle, fontsize=9.5, color=GRAY)

    # Left Panel: Formulations Box
    box_left = FancyBboxPatch((0.5, 0.55), 5.5, 3.0, boxstyle="round,pad=0.08,rounding_size=0.15",
                              facecolor=PANEL_COLOR, edgecolor=BORDER_COLOR, linewidth=1.2)
    ax.add_patch(box_left)

    ax.text(0.8, 2.85, form1, fontsize=14, color=PURPLE, va='center')
    ax.plot([0.8, 5.7], [2.2, 2.2], color="#21262d", linewidth=1.2)
    ax.text(0.8, 1.65, form2, fontsize=14, color=CYAN, va='center')

    # Note footer inside left box
    ax.text(0.8, 0.9, box_desc, fontsize=8.5, color="#8b949e", style='italic')

    # Right Panel: Trajectory & Curvature Arc Diagram
    box_right = FancyBboxPatch((6.3, 0.55), 5.2, 3.0, boxstyle="round,pad=0.08,rounding_size=0.15",
                               facecolor=PANEL_COLOR, edgecolor=BORDER_COLOR, linewidth=1.2)
    ax.add_patch(box_right)
    ax.text(8.9, 3.25, panel_diag_title, fontsize=10.5, fontweight='bold', color=WHITE, ha='center')

    # Route trajectory: vertical stem then sharp 90-degree cut to right, shifted down
    stem_x = np.linspace(7.4, 7.4, 25)
    stem_y = np.linspace(0.65, 1.45, 25)
    # Arc turn
    theta = np.linspace(np.pi, np.pi/2, 40)
    arc_r = 1.05
    arc_cx, arc_cy = 8.45, 1.45
    cut_x = arc_cx + arc_r * np.cos(theta)
    cut_y = arc_cy + arc_r * np.sin(theta)
    # Out stem
    out_x = np.linspace(8.45, 11.0, 25)
    out_y = np.linspace(2.5, 2.5, 25)

    traj_x = np.concatenate([stem_x, cut_x, out_x])
    traj_y = np.concatenate([stem_y, cut_y, out_y])
    ax.plot(traj_x, traj_y, color=CYAN, linewidth=3.0, alpha=0.9, zorder=6)

    # Osculating circle at the cut apex
    circle_apex = Circle((arc_cx, arc_cy), arc_r, fill=False, edgecolor=GOLD, linestyle="--", linewidth=1.3, alpha=0.6)
    ax.add_patch(circle_apex)
    ax.scatter([arc_cx], [arc_cy], s=35, color=GOLD, zorder=8)
    
    # Radius line R drawn toward upper right (e.g. angle 35 deg)
    ang_r = np.pi / 5.5
    rx_end = arc_cx + arc_r * np.cos(ang_r)
    ry_end = arc_cy + arc_r * np.sin(ang_r)
    ax.plot([arc_cx, rx_end], [arc_cy, ry_end], color=GOLD, linewidth=1.5, linestyle="-")
    ax.text(arc_cx + 0.25, arc_cy + 0.35, lbl_r, fontsize=7.5, color=GOLD, fontweight='bold', ha='left')

    # Player position at cut point (angle 135 deg)
    px = arc_cx + arc_r * np.cos(3*np.pi/4)
    py = arc_cy + arc_r * np.sin(3*np.pi/4)
    ax.scatter([px], [py], s=120, color=WHITE, edgecolors=PURPLE, linewidth=2.5, zorder=10)
    ax.text(px - 0.18, py - 0.28, pt_break, fontsize=8, color=WHITE, fontweight='bold', ha='right')

    # a_n arrow pointing to circle center (arc_cx, arc_cy)
    arrow_an = FancyArrowPatch((px, py), (px + 0.52*(arc_cx - px), py + 0.52*(arc_cy - py)),
                               arrowstyle="simple,head_width=6,head_length=7",
                               color=PURPLE, linewidth=2.2, zorder=9)
    ax.add_patch(arrow_an)
    ax.text(px + 0.25*(arc_cx - px) - 0.12, py + 0.25*(arc_cy - py) - 0.22, lbl_an, fontsize=7.5, color="#d2a8ff", fontweight='bold', ha='center')

    # Tangent velocity arrow
    tv_dx = -np.sin(3*np.pi/4) * 0.70
    tv_dy = np.cos(3*np.pi/4) * 0.70
    arrow_v = FancyArrowPatch((px, py), (px + tv_dx, py - tv_dy),
                              arrowstyle="simple,head_width=5,head_length=7",
                              color=GREEN, linewidth=2.0, zorder=9)
    ax.add_patch(arrow_v)
    ax.text(px + tv_dx - 0.08, py - tv_dy + 0.12, lbl_v, fontsize=8, color=GREEN, fontweight='bold', ha='right')

    filename = f"formula_centripetal_curvature_{lang}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=200, facecolor=BG_COLOR, edgecolor='none')
    plt.close()
    print(f"Generated {filepath}")


def create_brk_plus_card(lang='en'):
    fig = plt.figure(figsize=(12, 4.8), facecolor=BG_COLOR, dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.8)
    ax.axis('off')

    # Background card
    card = FancyBboxPatch((0.2, 0.2), 11.6, 4.4, boxstyle="round,pad=0.1,rounding_size=0.25",
                          facecolor=CARD_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5)
    ax.add_patch(card)

    if lang == 'en':
        title = "3. STANDARDIZED METRIC: BRK+ (BRAKING RATE PLUS)"
        subtitle = "League-adjusted kinematic index (Mean = 100, SD = 15). Higher = sharper deceleration & separation"
        formula_str = r"$\mathrm{BRK+} = 100 + 15 \times \left( \frac{\mu_{\mathrm{league}} - a_{t,\mathrm{player}}}{\sigma_{\mathrm{league}}} \right)$"
        panel_dist_title = "NFL Wide Receiver Distribution"
        tier_elite = "ELITE TIER (BRK+ ≥ 115) • Top 10% separation creators"
        tier_avg = "LEAGUE AVERAGE (85 - 114) • Standard NFL baseline"
        tier_poor = "SLUGGISH CUTTER (< 85) • Heavy press-coverage risk"
        callout_bryant = "Pat Bryant (130.7)\nSeparation: 3.19 yds"
    else:
        title = "3. СТАНДАРТИЗИРОВАННАЯ МЕТРИКА: BRK+ (BRAKING RATE PLUS)"
        subtitle = "Индекс торможения с поправкой на лигу (Среднее = 100, SD = 15). Выше = резче торможение и больше отрыв"
        formula_str = r"$\mathrm{BRK+} = 100 + 15 \times \left( \frac{\mu_{\mathrm{лига}} - a_{t,\mathrm{игрок}}}{\sigma_{\mathrm{лига}}} \right)$"
        panel_dist_title = "Распределение ресиверов НФЛ по BRK+"
        tier_elite = "ЭЛИТНЫЙ УРОВЕНЬ (BRK+ ≥ 115) • Топ-10% создателей отрыва"
        tier_avg = "СРЕДНИЙ УРОВЕНЬ (85 - 114) • Базовый уровень лиги"
        tier_poor = "МЕДЛЕННЫЙ СРЕЗ (< 85) • Трудности против плотной опеки"
        callout_bryant = "Пэт Брайант (130.7)\nОтрыв: 3.19 ярда"

    # Header
    ax.text(0.6, 4.25, title, fontsize=13.5, fontweight='bold', color=WHITE)
    ax.text(0.6, 3.88, subtitle, fontsize=9.5, color=GRAY)

    # Left Panel: Formula & Tiers Box
    box_left = FancyBboxPatch((0.5, 0.55), 5.5, 3.0, boxstyle="round,pad=0.08,rounding_size=0.15",
                              facecolor=PANEL_COLOR, edgecolor=BORDER_COLOR, linewidth=1.2)
    ax.add_patch(box_left)

    ax.text(3.25, 2.95, formula_str, fontsize=15.5, color=GOLD, ha='center', va='center')

    # 3 Tier Badges inside left panel
    # 1. Elite tier
    e_box = FancyBboxPatch((0.7, 2.05), 5.1, 0.55, boxstyle="round,pad=0.04,rounding_size=0.08",
                           facecolor="#122619", edgecolor="#238636", linewidth=0.9)
    ax.add_patch(e_box)
    ax.text(0.9, 2.32, tier_elite, fontsize=8, fontweight='bold', color="#85e89d", va='center')

    # 2. League avg
    a_box = FancyBboxPatch((0.7, 1.35), 5.1, 0.55, boxstyle="round,pad=0.04,rounding_size=0.08",
                           facecolor="#161b22", edgecolor="#388bfd", linewidth=0.9)
    ax.add_patch(a_box)
    ax.text(0.9, 1.62, tier_avg, fontsize=8, fontweight='bold', color="#79c0ff", va='center')

    # 3. Sluggish tier
    p_box = FancyBboxPatch((0.7, 0.65), 5.1, 0.55, boxstyle="round,pad=0.04,rounding_size=0.08",
                           facecolor="#2b1419", edgecolor="#da3633", linewidth=0.9)
    ax.add_patch(p_box)
    ax.text(0.9, 0.92, tier_poor, fontsize=8, fontweight='bold', color="#ff7b72", va='center')

    # Right Panel: Bell Curve Distribution
    box_right = FancyBboxPatch((6.3, 0.55), 5.2, 3.0, boxstyle="round,pad=0.08,rounding_size=0.15",
                               facecolor=PANEL_COLOR, edgecolor=BORDER_COLOR, linewidth=1.2)
    ax.add_patch(box_right)
    ax.text(8.9, 3.25, panel_dist_title, fontsize=10.5, fontweight='bold', color=WHITE, ha='center')

    # Generate Bell Curve in local coords (x: 6.6 to 11.2, y: 0.85 to 2.8)
    x_vals = np.linspace(55, 145, 200)
    mu, sigma = 100, 15
    y_vals = np.exp(-0.5 * ((x_vals - mu) / sigma) ** 2)

    def x_to_cx(val):
        return 6.6 + (val - 55) / (145 - 55) * 4.3

    cx = x_to_cx(x_vals)
    cy = 0.85 + y_vals * 1.8

    # Draw shaded areas
    mask_poor = x_vals < 85
    ax.fill_between(cx[mask_poor], 0.85, cy[mask_poor], color=CRIMSON, alpha=0.35)

    mask_avg = (x_vals >= 85) & (x_vals < 115)
    ax.fill_between(cx[mask_avg], 0.85, cy[mask_avg], color=CYAN, alpha=0.25)

    mask_elite = x_vals >= 115
    ax.fill_between(cx[mask_elite], 0.85, cy[mask_elite], color=GREEN, alpha=0.45)

    # Main curve line
    ax.plot(cx, cy, color=WHITE, linewidth=1.8)

    # Baseline axis line
    ax.plot([6.6, 10.9], [0.85, 0.85], color="#30363d", linewidth=1.2)

    # Mean line (100)
    ax.plot([x_to_cx(100), x_to_cx(100)], [0.85, 0.85 + 1.8], color=CYAN, linestyle="--", linewidth=1.2)
    ax.text(x_to_cx(100), 0.70, "100", fontsize=8, color=CYAN, ha='center', fontweight='bold')

    # 85 line
    ax.plot([x_to_cx(85), x_to_cx(85)], [0.85, 0.85 + np.exp(-0.5)*1.8], color=CRIMSON, linestyle=":", linewidth=1.0)
    ax.text(x_to_cx(85), 0.70, "85", fontsize=7.5, color=CRIMSON, ha='center')

    # 115 line
    ax.plot([x_to_cx(115), x_to_cx(115)], [0.85, 0.85 + np.exp(-0.5)*1.8], color=GREEN, linestyle=":", linewidth=1.0)
    ax.text(x_to_cx(115), 0.70, "115", fontsize=7.5, color=GREEN, ha='center')

    # Pat Bryant Callout (130.7)
    bryant_cx = x_to_cx(130.7)
    bryant_cy = 0.85 + np.exp(-0.5 * ((130.7 - mu)/sigma)**2) * 1.8
    ax.scatter([bryant_cx], [bryant_cy], s=65, color=GOLD, edgecolors=WHITE, linewidth=1.5, zorder=12)

    arrow_b = FancyArrowPatch((bryant_cx - 0.2, 2.5), (bryant_cx, bryant_cy + 0.08),
                              arrowstyle="simple,head_width=4,head_length=5",
                              color=GOLD, linewidth=1.2, zorder=11)
    ax.add_patch(arrow_b)
    ax.text(bryant_cx - 0.25, 2.65, callout_bryant, fontsize=7.5, color=GOLD, fontweight='bold', ha='right', va='center')

    filename = f"formula_brk_plus_{lang}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=200, facecolor=BG_COLOR, edgecolor='none')
    plt.close()
    print(f"Generated {filepath}")


if __name__ == '__main__':
    for lang in ['en', 'ru']:
        create_tangential_card(lang)
        create_centripetal_card(lang)
        create_brk_plus_card(lang)
    print("All formula card graphics successfully generated!")
