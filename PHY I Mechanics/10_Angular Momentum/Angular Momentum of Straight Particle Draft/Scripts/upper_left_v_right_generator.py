import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow

# Coordinates for a 3x3 grid (x: 0..2, y: 0..2)
points = {
    "A": (0, 2), "B": (1, 2), "C": (2, 2),
    "D": (0, 1), "E": (1, 1), "F": (2, 1),
    "G": (0, 0), "H": (1, 0), "I": (2, 0),
}

def draw_and_save(observer_label: str):
    fig, ax = plt.subplots(figsize=(6, 6))

    # Plot the 9 grid points with bigger markers
    xs = [coord[0] for coord in points.values()]
    ys = [coord[1] for coord in points.values()]
    ax.scatter(xs, ys, s=100, color='black', zorder=3)

    # Labels (slightly larger)
    for label, (x, y) in points.items():
        ax.text(x + 0.06, y + 0.06, label, fontsize=13, zorder=4)

    # Particle: solid green filled small circle
    particle_x, particle_y = 0.5, 1.5
    particle = Circle((particle_x, particle_y), radius=0.07, color="green", zorder=5)
    ax.add_patch(particle)

    # Velocity arrow pointing to the right with label v
    arrow_len = 0.6
    arrow = FancyArrow(particle_x, particle_y, arrow_len, 0.0, width=0.02,
                       head_width=0.10, head_length=0.10, length_includes_head=True, zorder=6)
    ax.add_patch(arrow)
    ax.text(particle_x + arrow_len + 0.08, particle_y - 0.02, "v", fontsize=14, zorder=7)

    # Small circle on the selected observer
    Ox, Oy = points[observer_label]
    observer_circle = Circle((Ox, Oy), radius=0.08, fill=False, linewidth=2, zorder=6)
    ax.add_patch(observer_circle)

    # Thinner dashed horizontal line passing through the particle
    ax.plot([-0.5, 2.5], [particle_y, particle_y], linestyle='--', color='gray', linewidth=1.0, zorder=2)

    # Formatting: grid background, equal aspect, limits, hide axes
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 1, 2])
    ax.grid(True, which='both', linewidth=0.8, alpha=0.6)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    filename = f"upper_left_v_right_{observer_label}.png"
    plt.savefig(filename, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"Saved {filename}")

if __name__ == "__main__":
    for lbl in ["A","B","C","D","E","F","G","H","I"]:
        draw_and_save(lbl)
