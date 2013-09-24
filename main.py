import wx
import random

class Mondrian(object):
    def __init__(self):
        self.set_client_size(1600, 1200)
    def set_client_size(self, w, h):
        self.client_size = (w, h)
        self.reset()
    def reset(self):
        cw, ch = self.client_size
        self.size = max(cw, ch) / 100
        self.bounds = (cw / self.size, ch / self.size)
        w, h = self.bounds
        self.bounds = (w + 2, h + 2)
        w, h = self.bounds
        self.grid = grid = [[0] * w for _ in range(h)]
        # walled perimeter
        for y in range(h):
            grid[y][0] = 1
            grid[y][w - 1] = 1
        for x in range(w):
            grid[0][x] = 2
            grid[h - 1][x] = 2
        # split
        split_count = random.randint(4, 16)
        _split_count = split_count
        splits = set([(1, 0), (1, w - 1), (2, 0), (2, h - 1)])
        while split_count:
            split = self.split(grid, splits)
            if split is not None:
                splits.add(split)
                split_count -= 1
        # locate all regions
        regions = []
        for y in range(h):
            for x in range(w):
                if grid[y][x] != 0:
                    continue
                regions.append((x, y))
                self.fill(grid, x, y, -1)
        random.shuffle(regions)
        # fill colors
        fill_count = random.randint(2, min(_split_count, 6))
        while fill_count:
            x, y = regions.pop()
            c = random.randint(3, 5)
            self.fill(grid, x, y, c)
            fill_count -= 1
        # fill white
        while regions:
            x, y = regions.pop()
            self.fill(grid, x, y, 0)
    def split(self, grid, splits):
        w, h = self.bounds
        p = 4
        d = random.randint(1, 2)
        if d == 1:
            x = random.randint(0, w - 1)
            for dx in range(-p, p + 1):
                if (1, x + dx) in splits:
                    return None
            p = []
            for y in range(0, h):
                if grid[y][x] == 2:
                    p.append(y)
            if len(p) < 2:
                return None
            a, b = sorted(random.sample(p, 2))
            for y in range(a, b + 1):
                grid[y][x] = 1
            return (1, x)
        else:
            y = random.randint(0, h - 1)
            for dy in range(-p, p + 1):
                if (2, y + dy) in splits:
                    return None
            p = []
            for x in range(0, w):
                if grid[y][x] == 1:
                    p.append(x)
            if len(p) < 2:
                return None
            a, b = sorted(random.sample(p, 2))
            for x in range(a, b + 1):
                grid[y][x] = 2
            return (2, y)
    def fill(self, grid, x, y, c):
        color = grid[y][x]
        queue = set([(x, y)])
        while queue:
            x, y = queue.pop()
            if grid[y][x] != color:
                continue
            grid[y][x] = c
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    queue.add((x + dx, y + dy))
    def render(self, dc):
        colors = [
            wx.WHITE,
            wx.BLACK,
            wx.BLACK,
            wx.Colour(204, 0, 11),
            wx.Colour(1, 102, 186),
            wx.Colour(249, 213, 26),
        ]
        n = self.size
        w, h = self.bounds
        dc.SetPen(wx.TRANSPARENT_PEN)
        for y in xrange(h - 2):
            for x in xrange(w - 2):
                i, j = x * n, y * n
                color = colors[self.grid[y + 1][x + 1]]
                dc.SetBrush(wx.Brush(color))
                dc.DrawRectangle(i, j, n + 1, n + 1)

class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None, -1, 'Mondrian')
        self.page = Mondrian()
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.update()
    def update(self):
        self.reset()
        wx.CallLater(5000, self.update)
    def reset(self):
        self.page.reset()
        self.Refresh()
    def on_key_down(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
    def on_left_down(self, event):
        self.reset()
    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.BLACK_BRUSH)
        dc.Clear()
        self.page.render(dc)
    def on_size(self, event):
        event.Skip()
        w, h = self.GetClientSize()
        self.page.set_client_size(w, h)
        self.Refresh()

def main():
    app = wx.App(False)
    frame = Frame()
    frame.SetClientSize((800, 600))
    frame.Center()
    frame.Show()
    #frame.ShowFullScreen(True)
    app.MainLoop()

if __name__ == '__main__':
    main()
