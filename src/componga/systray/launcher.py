import wx
import wx.adv
from threading import Thread


def async_componga_run(launcher):
    from componga.__main__ import main as componga_main

    componga_main(launcher=launcher)


class ImageFrame(wx.Frame):
    def __init__(self, callback, parent=None):
        super(ImageFrame, self).__init__(parent, title="Images", size=(500, 200))

        self._callback = callback
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        labels = ['Image 1', 'Image 2', 'Image 3']
        for idx, label in enumerate(labels):
            vbox = wx.BoxSizer(wx.VERTICAL)
            static_text = wx.StaticText(panel, label=label)
            bitmap = wx.Bitmap(f'/home/captain/workspace-gpt/componga/src/componga/resources/arrow-path.png', wx.BITMAP_TYPE_ANY)
            image = wx.StaticBitmap(panel, wx.ID_ANY, bitmap)

            image.Bind(wx.EVT_LEFT_DOWN, self.on_image_click)
            image.name = label

            vbox.Add(static_text, flag=wx.ALIGN_CENTER)
            vbox.Add(image, flag=wx.TOP | wx.ALIGN_CENTER, border=10)
            hbox.Add(vbox, flag=wx.ALL, border=10)

        panel.SetSizer(hbox)

    def on_image_click(self, event):
        source = event.GetEventObject()
        print(source.name)
        self.Close()
        self._callback(source.name)


class ConfigFrame(wx.Frame):
    def __init__(self, parent=None):
        super(ConfigFrame, self).__init__(
            parent,
            title="Configuration",
            size=(300, 200),
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX),
        )

        self.scrolled = wx.ScrolledWindow(self, -1)
        self.scrolled.SetScrollbars(1, 1, 600, 800)
        vbox = wx.BoxSizer(wx.VERTICAL)

        alphabet = [chr(i) for i in range(97, 123)]
        options = ["Option {}".format(i + 1) for i in range(10)]

        self.freeze_combo = wx.ComboBox(
            self.scrolled, choices=alphabet, style=wx.CB_READONLY
        )
        self.arrow_combo = wx.ComboBox(
            self.scrolled, choices=alphabet, style=wx.CB_READONLY
        )

        freeze_sizer = wx.BoxSizer(wx.HORIZONTAL)
        freeze_sizer.Add(
            wx.StaticText(self.scrolled, label="Freeze Shortcut: "),
            1,
            wx.EXPAND | wx.ALL,
            5,
        )
        freeze_sizer.Add(self.freeze_combo, 1, wx.EXPAND | wx.ALL, 5)

        arrow_sizer = wx.BoxSizer(wx.HORIZONTAL)
        arrow_sizer.Add(
            wx.StaticText(self.scrolled, label="Arrow Shortcut: "),
            1,
            wx.EXPAND | wx.ALL,
            5,
        )
        arrow_sizer.Add(self.arrow_combo, 1, wx.EXPAND | wx.ALL, 5)

        vbox.Add(freeze_sizer, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(arrow_sizer, 0, wx.EXPAND | wx.ALL, 5)

        for option in options:
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(
                wx.StaticText(self.scrolled, label=option), 1, wx.EXPAND | wx.ALL, 5
            )
            combo = wx.ComboBox(self.scrolled, choices=alphabet, style=wx.CB_READONLY)
            sizer.Add(combo, 1, wx.EXPAND | wx.ALL, 5)
            vbox.Add(sizer, 0, wx.EXPAND | wx.ALL, 5)

        self.scrolled.SetSizer(vbox)


class TrayIcon(wx.adv.TaskBarIcon):
    def __init__(self):
        super(TrayIcon, self).__init__()
        self.set_icon("/home/captain/workspace-gpt/componga/src/componga/resources/arrow-path.png")
        self._componga_app = None
        self._menu = None
        self._build_menu()
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.on_right_click)

    def _build_menu(self):
        self._menu = wx.Menu()
        show_item = self._menu.Append(wx.ID_ANY, "Show", "Show Image Frame")
        hide_item = self._menu.Append(wx.ID_ANY, "Hide", "Hide Componga Window")
        config_item = self._menu.Append(wx.ID_ANY, "Config", "Configure Shortcuts")
        exit_item = self._menu.Append(wx.ID_EXIT, "Exit", "Exit the application")

        self.Bind(wx.EVT_MENU, self.on_show, show_item)
        self.Bind(wx.EVT_MENU, self.on_hide, hide_item)
        self.Bind(wx.EVT_MENU, self.on_config, config_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        return self._menu

    def _launch_componga(self):
        Thread(target=async_componga_run, args=(self,)).start()

    def register_componga_app(self, componga_app):
        self._componga_app = componga_app

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, "Tray App")

    def on_right_click(self, event):
        self.PopupMenu(self._menu)

    def on_show(self, event):
        frame = ImageFrame(self._on_desktop_selected)
        frame.Show()

    def _on_desktop_selected(self, selection):
        print(f"on_desktop_selected: {selection}")
        if self._componga_app:
            self._componga_app.run_launcher_cmd("show")
        else:
            wx.CallAfter(self._launch_componga)

    def on_hide(self, event):
        print("on_hide")
        if self._componga_app:
            self._componga_app.run_launcher_cmd("hide")

    def on_config(self, event):
        frame = ConfigFrame()
        frame.Show()

    def on_exit(self, event):
        print("on_exit")
        if self._componga_app:
            self._componga_app.run_launcher_cmd("stop")

        wx.CallAfter(self.Destroy)
        wx.CallAfter(wx.GetApp().ExitMainLoop)


class WxApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.tray_icon = TrayIcon()
        return True


if __name__ == "__main__":
    app = WxApp(False)
    app.MainLoop()
