import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from LO2Mixin import LO2Mixin, wrap_init

class LO2BrowserComponent(ControlSurfaceComponent, LO2Mixin):

    @wrap_init
    def __init__(self, *a, **kw):
        super(LO2BrowserComponent, self).__init__(*a, **kw)

        # Ableton
        self.view = self.application().view
        self.song = self.song()
        self.tracks = self.song.visible_tracks
        self.browser = self.application().browser

        self.add_callback('/live/browser/drums/load', self.browser_drums_load)
        self.add_callback('/live/browser/instruments/load', self.browser_not_implemented)
        self.add_callback('/live/browser/audiofx/load', self.browser_not_implemented)
        self.add_callback('/live/browser/midifx/load', self.browser_not_implemented)
        self.add_callback('/live/browser/m4l/load', self.browser_not_implemented)
        self.add_callback('/live/browser/plugins/load', self.browser_not_implemented)
        self.add_callback('/live/browser/clips/load', self.browser_not_implemented)
        self.add_callback('/live/browser/samples/load', self.browser_not_implemented)
        self.add_callback('/live/browser/sounds/load', self.browser_not_implemented)
        self.add_callback('/live/browser/packs/load', self.browser_not_implemented)
        self.add_callback('/live/browser/userlib/load', self.browser_not_implemented)
        self.add_callback('/live/browser/currentprj/load', self.browser_not_implemented)
        self.add_callback('/live/browser/userfolders/load', self.browser_not_implemented)

    def browser_not_implemented(self):
        self.show_message("call not implemented!")

    # Ableton Callbacks
    def _browser_drums_list(self):
        drum_kits = filter(lambda k:
                           k.is_loadable,
                           [k for k in self.browser.drums.children])
        drum_kits = [dk for dk in drum_kits]

        return drum_kits

    def _find_drum_by_name(self, name):
        drum_kits = self._browser_drums_list()
        kit = filter(lambda k: k.name == name, drum_kits)
        if len(kit) > 0:
            kit = kit[0]
        else:
            kit = None

        return kit

    def _browser_load_item(self, item):
        self.browser.load_item(item)

    # Callbacks
    def browser_drums_load(self, msg, src):
        path, type_tag, name = msg
        kit = self._find_drum_by_name(name)
        self._browser_load_item(kit)
