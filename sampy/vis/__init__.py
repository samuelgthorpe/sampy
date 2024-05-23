"""
This module houses common sampy visuaization methods.

# NOTES
# ----------------------------------------------------------------------------|


written March 2024
by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import numpy as np
from matplotlib.colors import ListedColormap


# # Globals
# -----------------------------------------------------|
HOTNCOLD_ARRAY = np.zeros([256, 3])
HOTNCOLD_ARRAY[:128, 2] = np.linspace(0, 1, 128)[::-1]
HOTNCOLD_ARRAY[128:, 0] = np.linspace(0, 1, 128)
HOTNCOLD = ListedColormap(HOTNCOLD_ARRAY)


# # Vis Exception Class
# -----------------------------------------------------|
VisException = type('VisException', (Exception,), {})


# # Common Visualization Tools
# -----------------------------------------------------|
def prettify(axi, grid_ax='y', grid_alpha=0.25):  # pragma: no cover
    """Make axes pretty."""
    color_lines_neutral = '#858585'  # dark grey
    axi.spines['left'].set_color(color_lines_neutral)
    axi.spines['bottom'].set_color(color_lines_neutral)
    axi.spines['top'].set_visible(False)
    axi.spines['right'].set_visible(False)
    axi.spines['left'].set_position(('outward', 10))
    axi.tick_params(right=False, left=False, top=False, bottom=False)
    axi.grid(b=True, which='both', axis=grid_ax, alpha=grid_alpha, ls='solid')


def label_subplot(axi, tag, ptag=None, fontsiz=17, xbuff=(-0.1, 0.4)):
    """Label the subplot."""
    axi.text(xbuff[0], 1.04, tag, transform=axi.transAxes,
             ha='center', fontsize=fontsiz)
    if ptag:
        axi.text(xbuff[1], 1.04, ptag, transform=axi.transAxes,
                 ha='center', fontsize=fontsiz, fontstyle='italic')


def add_scalebar(axi, dx, dy, tagx=None, tagy=None, fontsiz=15):
    """Add scalebar at origin of axis."""
    x, y = axi.get_xlim(), axi.get_ylim()
    xmax, ymax = x[0] + dx, y[0] + dy
    xb, yb = 0.25*xmax, 0.1*ymax
    tagx = tagx if tagx else '{}s'.format(dx)
    tagy = tagy if tagy else '{} \ncm/s'.format(dy)
    clr = [0.2]*3
    axi.plot([x[0]-xb, xmax-xb], [y[0]-yb, y[0]-yb], c=clr, lw=3)
    axi.plot([x[0]-xb, x[0]-xb], [y[0]-yb, ymax-yb], c=clr, lw=3)
    axi.text(xmax-xb, y[0]-1.5*yb, tagx, ha='center', va='top',
             fontsize=fontsiz, fontstyle='italic')
    axi.text(x[0]-1.5*xb, ymax-yb, tagy, ha='right', va='top',
             fontsize=fontsiz, fontstyle='italic')
    axi.set_xlim([x[0] - 2*xb, x[1]])
    axi.set_ylim([y[0] - 2*yb, y[1]])


def shift_axi(axi, x0_shift, y0_shift, x_scale, y_scale):
    """Shift axis."""
    pos = axi.get_position()
    shifted = [pos.x0 + x0_shift, pos.y0 + y0_shift,
               x_scale*pos.width, y_scale*pos.height]
    axi.set_position(shifted)


# # Main Entry
# -----------------------------------------------------|
if __name__ == "__main__":
    pass
