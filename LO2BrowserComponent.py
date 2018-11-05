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
        self.add_callback('/live/browser/instruments/load', self._browser_not_implemented)
        self.add_callback('/live/browser/audiofx/load', self._browser_not_implemented)
        self.add_callback('/live/browser/midifx/load', self._browser_not_implemented)
        self.add_callback('/live/browser/m4l/load', self._browser_not_implemented)
        self.add_callback('/live/browser/plugins/load', self._browser_not_implemented)
        self.add_callback('/live/browser/clips/load', self._browser_not_implemented)
        self.add_callback('/live/browser/samples/load', self._browser_not_implemented)
        self.add_callback('/live/browser/sounds/load', self._browser_not_implemented)
        self.add_callback('/live/browser/packs/load', self._browser_not_implemented)
        self.add_callback('/live/browser/userlib/load', self._browser_not_implemented)
        self.add_callback('/live/browser/currentprj/load', self._browser_not_implemented)
        self.add_callback('/live/browser/userfolders/load', self._browser_not_implemented)


    def _recursive_browse(self, item):
        item_list = []
        if hasattr(item, 'children'):
            for it in item.children:
                item_list += [it]
                item_list += self._recursive_browse(it)

        return item_list

    def _browser_not_implemented(self):
        self.show_message("call not implemented!")

    def _browser_category_list(self, subcat):
        items = [i for i in self._recursive_browse(subcat)]
        return [i for i in filter(lambda i: i.is_loadable, items)]

    def _browser_drums_list(self):
        return self._browser_category_list(self.browser.drums)

    def _browser_instruments_list(self):
        return self._browser_category_list(self.browser.instruments)

    def _browser_audiofx_list(self):
        return self._browser_category_list(self.browser.audio_effects)

    def _browser_midifx_list(self):
        return self._browser_category_list(self.browser.midi_effects)

    def _browser_m4l_list(self):
        return self._browser_category_list(self.browser.max_for_live)

    def _browser_plugins_list(self):
        return self._browser_category_list(self.browser.plugins)

    def _browser_clips_list(self):
        return self._browser_category_list(self.browser.clips)

    def _browser_samples_list(self):
        return self._browser_category_list(self.browser.samples)

    def _browser_sounds_list(self):
        return self._browser_category_list(self.browser.sounds)

    def _browser_packs_list(self):
        return self._browser_category_list(self.browser.packs)

    def _browser_userlib_list(self):
        return self._browser_category_list(self.browser.user_library)

    def _browser_currentprj_list(self):
        return self._browser_category_list(self.browser.current_project)

    def _browser_userfolders_list(self):
        return self._browser_category_list(self.browser.user_folders)

    def _find_item_by_name(self, category, name):
        categories = {
            'drums': self._browser_drums_list,
            'instruments': self._browser_instruments_list,
            'audiofx': self._browser_audiofx_list,
            'midifx': self._browser_midifx_list,
            'm4l': self._browser_m4l_list,
            'plugins': self._browser_plugins_list,
            'clips': self._browser_clips_list,
            'samples': self._browser_samples_list,
            'sounds': self._browser_sounds_list,
            'packs': self._browser_packs_list,
            'userlib': self._browser_userlib_list,
            'currentprj': self._browser_currentprj_list,
            'userfolders': self._browser_userfolders_list,
        }
        item = None
        if category in categories.keys():
            item = filter(lambda i: i.name == name, categories.get(category)())
            if len(item):
                item = item[0]

        return item

    def _browser_load_item(self, item):
        self.browser.load_item(item)

    # Callbacks
    def browser_drums_load(self, msg, src):
        path, type_tag, name = msg
        kit = self._find_item_by_name('drums', name)
        self._browser_load_item(kit)
