import Live

from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.SubjectSlot import subject_slot

from LO2Mixin import LO2Mixin, wrap_init


class LO2ClipSlotComponent(ClipSlotComponent, LO2Mixin):

    def with_clip(fn):
        def wrap(self, *a, **kw):
            if self._clip_slot is not None:
                if self._clip_slot.has_clip:
                    fn(self, *a, **kw)

        return wrap


    @wrap_init
    def __init__(self, tid, sid, *a, **k):
        self._track_id = tid
        self._scene_id = sid
        self._has_clip = 0

        super(LO2ClipSlotComponent, self).__init__(*a, **k)

        self.set_default('_track_id', '_scene_id')

        callbacks = {
            'color': 'color',
            'name': 'name',
            'warping': 'warping',
            'looping': 'looping',
            'loopstart': 'loop_start',
            'loopend': 'loop_end',
            'start': 'start_marker',
            'end': 'end_marker',
            'loopjump': 'loop_jump',
            'muted': 'muted'
        }

        for n,p in callbacks.iteritems():
            self.add_simple_callback('/live/clip/'+n, '_clip_slot.clip', p, self._is_clip, getattr(self, '_on_clip_'+n+'_changed'))

        self.add_callback('/live/clip/play', self._fire)
        self.add_callback('/live/clip/stop', self._stop)
        self.add_callback('/live/clip/pitch', self._pitch)
        self.add_callback('/live/clip/select', self._view)
        self.add_callback('/live/clip/notes', self._notes)
        self.add_callback('/live/clip/notes/add', self._notes_add)
        self.add_callback('/live/clip/notes/remove', self._notes_remove)



    def _lo2__update_clip_property_slots(self):
        clip = self._clip_slot.clip if self._clip_slot else None

        self._on_clip_name_changed.subject = clip
        self._on_clip_warping_changed.subject = clip
        self._on_clip_looping_changed.subject = clip
        self._on_clip_loopjump_changed.subject = clip
        self._on_clip_loopstart_changed.subject = clip
        self._on_clip_loopend_changed.subject = clip
        self._on_clip_start_changed.subject = clip
        self._on_clip_end_changed.subject = clip
        self._on_clip_gain_changed.subject = clip
        self._on_clip_muted_changed.subject = clip


    def _is_clip(self, msg):
        if len(msg) >= 4:
            return msg[2] == self._track_id and msg[3] == self._scene_id


    # Properties
    @property
    def id(self):
        return (self._track_id, self._scene_id)

    def _get_name(self):
        if self._clip_slot is not None:
            if self._clip_slot.has_clip:
                return self._clip_slot.clip.name
            else:
                return ''
        else:
            return ''

    #@with_clip
    def _set_name(self, name):
        if self._clip_slot is not None:
            if self._clip_slot.has_clip:
                self._clip_slot.clip.name = name

    clip_name = property(_get_name, _set_name)


    def _get_color(self):
        if self._clip_slot is not None:
            if self._clip_slot.has_clip:
                return self._clip_slot.clip.color
            else:
                return 0
        else:
            return 0

    #@with_clip
    def _set_color(self, color):
            self._clip_slot.clip.name = color

    color = property(_get_color, _set_color)



    # Listeners
    def _lo2__on_clip_state_changed(self):
        self._send_state()

    def _lo2__on_clip_playing_state_changed(self):
        self._send_state()

    def _send_state(self):
        if self._scene_id == -1:
            return

        state = LO2ClipSlotComponent.compute_state(self._clip_slot)
        name = ''

        if self._clip_slot.has_clip:
            name = self._clip_slot.clip.name

        self.send('/live/clip/state', self._track_id, self._scene_id, state)

        if self._clip_slot.has_clip != self._has_clip:
            self._has_clip = self._clip_slot.has_clip
            self.send_default('/live/clip/name', name)

    @staticmethod
    def compute_state(clip_slot):
        state = int(clip_slot.has_clip) if clip_slot is not None else 0

        if clip_slot.has_clip:
            c = clip_slot.clip
            if c.is_playing:
                state = 2
            if c.is_triggered:
                state = 3

        return state


    def _lo2__on_clip_color_changed(self):
        self.send_default('/live/clip/color', self._clip_slot.clip.color)


    @subject_slot('name')
    def _on_clip_name_changed(self):
        self.send_default('/live/clip/name', self._clip_slot.clip.name)


    @subject_slot('warping')
    def _on_clip_warping_changed(self):
        self.send_default('/live/clip/warping', self._clip_slot.clip.warping)

    @subject_slot('loop_jump')
    def _on_clip_loopjump_changed(self):
        self.send_default('/live/clip/loopjump')

    @subject_slot('looping')
    def _on_clip_looping_changed(self):
        self.send_default('/live/clip/loopstate', self._clip_slot.clip.looping)

    @subject_slot('loop_start')
    def _on_clip_loopstart_changed(self):
        self.send_default('/live/clip/loopstart', self._clip_slot.clip.loop_start)

    @subject_slot('loop_end')
    def _on_clip_loopend_changed(self):
        self.send_default('/live/clip/loopend', self._clip_slot.clip.loop_end)

    @subject_slot('start_marker')
    def _on_clip_start_changed(self):
        self.send_default('/live/clip/start', self._clip_slot.clip.start_marker)

    @subject_slot('end_marker')
    def _on_clip_end_changed(self):
        self.send_default('/live/clip/end', self._clip_slot.clip.end_marker)

    @subject_slot('gain')
    def _on_clip_gain_changed(self):
        self.send_default('/live/clip/gain', self._clip_slot.clip.gain)

    @subject_slot('muted')
    def _on_clip_muted_changed(self):
        self.send_default('/live/clip/muted', self._clip_slot.clip.muted)



    # Callbacks
    def _fire(self, msg, src):
        if self._clip_slot is not None and self._is_clip(msg):
            if self._clip_slot.has_clip:
                self._clip_slot.clip.fire()
            else:
                self._clip_slot.fire()

    def _stop(self, msg, src):
        if self._clip_slot is not None and self._is_clip(msg):
            if self._clip_slot.has_clip:
                self._clip_slot.clip.stop()
            else:
                self._clip_slot.stop()

    @with_clip
    def _pitch(self, msg, src):
        if self._is_clip(msg):
            c = self._clip_slot.clip
            if len(msg) == 6:
                c.pitch_coarse = msg[4]
                c.pitch_fine = msg[5]
            else:
                self.send_default('/live/clip/pitch', c.pitch_coarse, c.pitch_fine)


    @with_clip
    def _view(self, msg, src):
        if self._is_clip(msg):
            tr = self._clip_slot.canonical_parent
            self.song().view.detail_clip = self._clip_slot.clip
            self.application().view.show_view('Detail/Clip')

            if 0:
                self.song().view.selected_track = self._clip_slot.canonical_parent
                self.song().view.selected_scene = self.song().scenes[self._scene_id]


    def _notes(self, msg, src):
        if self._is_clip(msg):
            c = self._clip_slot.clip

            if c.is_midi_clip and len(msg) == 8:
                notes = c.get_notes(msg[4], msg[5], msg[6], msg[7])
                data = []
                data.append(self._track_id)
                data.append(self._scene_id)

                for n in notes:
                    for p in n:
                        data.append(p)
                self.send('/live/clip/notes', data)


    def _notes_add(self, msg, src):
        if self._is_clip(msg):
            c = self._clip_slot.clip
            if c.is_midi_clip and len(msg) >= 9:
                param_count = len(msg) - 4
                if param_count % 5 != 0:
                    return # bad param count/format

                note_count = param_count / 5

                notes_to_add = []
                for x in range(note_count):
                    notes_to_add.append(
                            (msg[x * 5 + 4], msg[x * 5 + 5], msg[x * 5 + 6], msg[x * 5 + 7], msg[x * 5 + 8])
                        )

                c.set_notes(tuple(notes_to_add))


    def _notes_remove(self, msg, src):
        if self._is_clip(msg):
            c = self._clip_slot.clip
            if c.is_midi_clip and len(msg) == 8:
                c.remove_notes(msg[4], msg[5], msg[6], msg[7])



