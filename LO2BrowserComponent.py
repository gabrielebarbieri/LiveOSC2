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

        self.add_callback('/live/browser/load', self.browser_load)

    # Ableton Callbacks
    def _browser_list_drum(self):
        drum_kits = filter(lambda k:
                           k.is_loadable,
                           [k for k in self.browser.drums.children])
        drum_kits = [dk for dk in drum_kits]

        return drum_kits

    def _find_drum_by_name(self, name):
        drum_kits = self._browser_list_drum()
        kit = filter(lambda k: k.name == name, drum_kits)
        if len(kit) > 0:
            kit = kit[0]
        else:
            kit = None

        return kit

    def _browser_load_item(self, name):
        kit = self._find_drum_by_name(name)
        self.browser.load_item(kit)

    def _list_tracks(self):
        self.log_message(self.tracks)

    # Callbacks
    def browser_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item(name)
