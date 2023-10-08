import wx
import wx.adv
from threading import Thread


def async_componga_run(launcher):
    from componga.__main__ import main as componga_main

    componga_main(launcher=launcher)


class TrayIcon(wx.adv.TaskBarIcon):
    def __init__(self):
        super(TrayIcon, self).__init__()
        self.set_icon(
            "/home/captain/workspace-gpt/componga/src/componga/resources/arrow-path.png"
        )
        self._componga_app = None
        self._menu = None

        self._build_menu()
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.on_right_click)

    def _build_menu(self):
        self._menu = wx.Menu()
        show_item = self._menu.Append(wx.ID_ANY, "Show", "Show Componga Window")
        hide_item = self._menu.Append(wx.ID_ANY, "Hide", "Hide Componga Window")
        exit_item = self._menu.Append(wx.ID_EXIT, "Exit", "Exit the application")

        self.Bind(wx.EVT_MENU, self.on_show, show_item)
        self.Bind(wx.EVT_MENU, self.on_hide, hide_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        return self._menu

    def _launch_componga(self):
        Thread(target=async_componga_run, args=(self,)).start()

    def register_componga_app(self, componga_app):
        self._componga_app = componga_app

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, "My Kivy App")

    def on_right_click(self, event):
        self.PopupMenu(self._menu)

    def on_show(self, event):
        print("on_show")
        if self._componga_app:
            self._componga_app.run_launcher_cmd("show")
        else:
            wx.CallAfter(self._launch_componga)

    def on_hide(self, event):
        print("on_hide")
        if self._componga_app:
            self._componga_app.run_launcher_cmd("hide")

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
