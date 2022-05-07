bl_info = {
    "name": "Long Exposure Effect",
    "author": "aaron",
    "description": "Creates a long exposure effect for the selected script",
    "version": (0, 1),
    "blender": (3, 1, 0),
    "location": "Sequencer -> Strip",
    "warning": "Want's your RAM more than Chrome",
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
        self.layout.operator(
            "sequencer.long_exposure_effect",
            text="Long Exposure Effect",
            icon="OUTLINER_OB_CAMERA",
        )


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
        max=128,
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

    def execute(self, context):
        if bpy.context.area.type != "SEQUENCE_EDITOR":
            return {"CANCELLED"}

        original = bpy.context.scene.sequence_editor.active_strip
        # Make sure only the active strip is selected:
        bpy.ops.sequencer.select_all(action="DESELECT")
        original.select = True
        bpy.context.scene.sequence_editor.active_strip = original

        # List of created strips
        created_strips = []
        # Create and shift duplicates, set opacity
        for _ in range(self.levels):
            bpy.ops.sequencer.duplicate_move(
                SEQUENCER_OT_duplicate={}, TRANSFORM_OT_seq_slide={"value": (1, 1)}
            )
            current = bpy.context.active_sequence_strip
            current.blend_alpha = self.opacity
            created_strips.append(current)

            if current.channel == 128:
                # Max number of channels reached
                break

        # Select created strips
        bpy.ops.sequencer.select_all(action="DESELECT")
        for i in created_strips:
            i.select = True
        original.select = True
        bpy.context.scene.sequence_editor.active_strip = original

        # make meta strip
        bpy.ops.sequencer.meta_make()

        if not self.fade_in:
            # Re,pve the first frames as the effect fades in
            meta_strip = bpy.context.scene.sequence_editor.active_strip
            bpy.ops.sequencer.select_all(action="DESELECT")
            meta_strip.select = True
            meta_strip.select_left_handle = True
            bpy.ops.transform.seq_slide(value=(self.levels, 0))
            # Move the whole strip forward
            bpy.ops.sequencer.select_all(action="DESELECT")
            meta_strip.select = True
            bpy.ops.transform.seq_slide(value=(-self.levels, 0))

        if not self.fade_out:
            # Remove the last frames as the effect fades out
            meta_strip = bpy.context.scene.sequence_editor.active_strip
            bpy.ops.sequencer.select_all(action="DESELECT")
            meta_strip.select = True
            meta_strip.select_right_handle = True
            bpy.ops.transform.seq_slide(value=(-self.levels, 0))

        return {"FINISHED"}


def register():
    bpy.utils.register_class(SEQUENCER_OT_long_expo_effect)
    bpy.utils.register_class(SEQUENCER_PT_long_exposure)


def unregister():
    bpy.utils.unregister_class(SEQUENCER_OT_long_expo_effect)
    bpy.utils.unegister_class(SEQUENCER_PT_long_exposure)
