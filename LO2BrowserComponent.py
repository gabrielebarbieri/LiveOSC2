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
        self.add_callback('/live/browser/instruments/load', self.browser_instruments_load)
        self.add_callback('/live/browser/audiofx/load', self.browser_audiofx_load)
        self.add_callback('/live/browser/midifx/load', self.browser_midifx_load)
        self.add_callback('/live/browser/m4l/load', self.browser_m4l_load)
        self.add_callback('/live/browser/plugins/load', self.browser_plugins_load)
        self.add_callback('/live/browser/clips/load', self.browser_clips_load)
        self.add_callback('/live/browser/samples/load', self.browser_samples_load)
        self.add_callback('/live/browser/sounds/load', self.browser_sounds_load)
        self.add_callback('/live/browser/packs/load', self.browser_packs_load)
        self.add_callback('/live/browser/userlib/load', self.browser_userlib_load)
        self.add_callback('/live/browser/currentprj/load', self.browser_currentprj_load)
        self.add_callback('/live/browser/userfolders/load', self.browser_userfolders_load)

        self.add_callback('/live/browser/list', self.browser_list)


    def _recursive_browse(self, item):
        item_list = []
        if hasattr(item, 'children'):
            for it in item.children:
                if it.is_loadable and not it.is_folder:
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

    def _find_items_by_category(self, category):
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

        if category in categories.keys():
            return categories.get(category)()
        else:
            return categories.keys()

    def _find_item_by_name(self, category, name):
        item = None
        item_list = self._find_items_by_category(category)
        if item_list:
            item = filter(lambda i: i.name == name, item_list)
            if len(item):
                item = item[0]

        return item

    def _browser_load_item(self, category, name):
        item = self._find_item_by_name(category, name)
        self.browser.load_item(item)

    # Callbacks
    def browser_list(self, msg, src):
        if len(msg) == 3:
            path, type_tag, category = msg
        else:
            path, type_tag = msg
            category = None

        item_list = self._find_items_by_category(category)
        item_list = list(map(lambda i: i if isinstance(i, str) else i.name, item_list))

        self.send('/live/browser/list', item_list)

    def browser_drums_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('drums', name)

    def browser_instruments_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('instruments', name)

    def browser_audiofx_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('audiofx', name)

    def browser_midifx_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('midifx', name)

    def browser_m4l_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('m4l', name)

    def browser_plugins_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('plugins', name)

    def browser_clips_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('clips', name)

    def browser_samples_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('samples', name)

    def browser_sounds_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('sounds', name)

    def browser_packs_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('packs', name)

    def browser_userlib_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('userlib', name)

    def browser_currentprj_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('currentprj', name)

    def browser_userfolders_load(self, msg, src):
        path, type_tag, name = msg
        self._browser_load_item('userfolders', name)
