bl_info = {
    "name": "Long Exposure Video Effect",
    "author": "aaron",
    "description": "Creates a long exposure effect for the selected script",
    "version": (1, 1),
    "blender": (3, 1, 0),
    "location": "Sequencer -> Strip",
    "warning": "Can use a lot of RAM. Save your scene before using it!",
    "wiki_url": "",
    "category": "Sequencer",
}

import bpy


class SEQUENCER_PT_long_exposure(bpy.types.Panel):
    bl_label = "Long Exposure Effect"
    bl_category = "Strip"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):

        strip = context.active_sequence_strip
        if not strip:
            return False

        return strip.type != "SOUND"

    def draw(self, context):
        col = self.layout.column()
        default = col.operator(
            "sequencer.long_exposure_effect",
            text="Long Exposure Water",
            icon="OUTLINER_OB_FORCE_FIELD",
        )
        default.opacity = 0.05
        default.mode = "ALPHA_OVER"

        star_trails = col.operator(
            "sequencer.long_exposure_effect",
            text="Star Trails",
            icon="MOD_WAVE",
        )
        star_trails.opacity = 1
        star_trails.mode = "LIGHTEN"


class SEQUENCER_OT_long_expo_effect(bpy.types.Operator):
    """Create Long Exposure effect"""

    bl_idname = "sequencer.long_exposure_effect"
    bl_label = "Long Exposure Effect"
    bl_options = {"REGISTER", "UNDO"}

    levels: bpy.props.IntProperty(
        name="Levels",
        description="Number of duplicates of the selected strip.",
        default=10,
        min=1,
        max=127,
    )

    opacity: bpy.props.FloatProperty(
        name="Opacity",
        description="Opacity of the duplicated strips.",
        default=0.05,
        min=0,
        max=1,
    )

    fade_in: bpy.props.BoolProperty(
        name="Fade In",
        description="Effects starts gradually",
        default=True,
    )

    fade_out: bpy.props.BoolProperty(
        name="Fade Out",
        description="Effects stops gradually",
        default=True,
    )

    comet_mode: bpy.props.BoolProperty(
        name="Comet Mode",
        description="Opacity decreases gradually",
        default=False,
    )

    mode: bpy.props.StringProperty(
        name="Blend type",
        description="Blend mode of strips",
        default="ALPHA_OVER",
        options={"HIDDEN"},
    )

    def execute(self, context):
        if bpy.context.area.type != "SEQUENCE_EDITOR":
            return {"CANCELLED"}

        original = bpy.context.scene.sequence_editor.active_strip
        end_frame = original.frame_final_end
        # Make sure only the active strip is selected:
        bpy.ops.sequencer.select_all(action="DESELECT")
        original.select = True
        bpy.context.scene.sequence_editor.active_strip = original

        # Make meta strip
        bpy.ops.sequencer.meta_make()
        bpy.ops.sequencer.meta_toggle()
        original.select = True
        bpy.context.scene.sequence_editor.active_strip = original

        # Create and shift duplicates by 1 frame
        for i in range(1, self.levels):
            bpy.ops.sequencer.duplicate_move(
                SEQUENCER_OT_duplicate={}, TRANSFORM_OT_seq_slide={"value": (1, 1)}
            )
            current = bpy.context.active_sequence_strip
            current.blend_type = self.mode
            # Set opacity
            if self.comet_mode:
                opacity = self.opacity - i / self.levels
            else:
                opacity = self.opacity
            current.blend_alpha = opacity

            if current.channel == 128:
                self.levels = i
                # Max number of channels reached
                break

        # Exit from meta strip
        bpy.ops.sequencer.meta_toggle()

        meta_strip = bpy.context.scene.sequence_editor.active_strip
        if not self.fade_in:
            # Remove the first frames as the effect fades in
            meta_strip.frame_final_start += self.levels
            # Move the whole strip forward
            bpy.ops.sequencer.select_all(action="DESELECT")
            meta_strip.select = True
            bpy.ops.transform.seq_slide(value=(-self.levels, 0))

        if self.fade_out:
            # Increase the meta strip lenght
            meta_strip.frame_final_end += self.levels

        if end_frame < meta_strip.frame_final_end:
            """
            If there is another strip behind it's better to move upone channel.
            Otherwise it would move on x axis.
            Not elegant but it works.
            """
            meta_strip.channel += 1

        return {"FINISHED"}


def register():
    bpy.utils.register_class(SEQUENCER_OT_long_expo_effect)
    bpy.utils.register_class(SEQUENCER_PT_long_exposure)


def unregister():
    bpy.utils.unregister_class(SEQUENCER_OT_long_expo_effect)
    bpy.utils.unegister_class(SEQUENCER_PT_long_exposure)
