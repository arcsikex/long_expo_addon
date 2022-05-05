bl_info = {
    "name": "Long Exposure Effect",
    "author": "",  # NemAron <nemetharon95@gmail.com>
    "description": "Creates a long exposure effect for the selected script",
    "version": (0, 1),
    "blender": (3, 1, 0),
    "location": "Sequencer -> Strip",
    "warning": "Want's your RAM more than Chrome",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "Sequencer",
}

import bpy


class SEQUENCER_PT_long_exposure(bpy.types.Panel):
    bl_label = "Long Exposure"
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

    def execute(self, context):
        if bpy.context.area.type != "SEQUENCE_EDITOR":
            return {"CANCELLED"}

        bpy.ops.sequencer.lock()
        original = bpy.context.scene.sequence_editor.active_strip

        # Create and shift duplicates
        created_strips = []
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
        bpy.ops.object.select_all(action="DESELECT")
        for i in created_strips:
            i.select = True
        original.select = True
        bpy.context.scene.sequence_editor.active_strip = original

        # make meta strip
        bpy.ops.sequencer.meta_make()

        return {"FINISHED"}


def register():
    bpy.utils.register_class(SEQUENCER_OT_long_expo_effect)
    bpy.utils.register_class(SEQUENCER_PT_long_exposure)


def unregister():
    bpy.utils.unregister_class(SEQUENCER_OT_long_expo_effect)
    bpy.utils.register_class(SEQUENCER_PT_long_exposure)
