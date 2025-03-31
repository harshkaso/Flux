import dearcygui as dcg
from flowfield_library import flowfield_registry
from mask_library import mask_registry
from config import Defaults, UIDimensions, UITypes, Properties

class Flowfield:
    def __init__(self, context):
        self.context = context
        self.width  = context.flowfield_window.width
        self.height = context.flowfield_window.height
        self.mask_list = mask_registry
        self.function_list = flowfield_registry
        self.mask_fade = Properties.mask_fade
        self._set_mask(Defaults.mask)
        self._set_function(Defaults.flowfield_function)

    def setup_controls(self):
        self.function_combo = dcg.Combo(self.context, 
                                        width=UIDimensions.side_panel_width/2 ,
                                        items=list(self.function_list.keys()),
                                        label='Function',
                                        value=Defaults.flowfield_function,
                                        callback=lambda _0, _1, function_name: self._set_function(function_name))
        with dcg.VerticalLayout(self.context) as self.function_controls:
            self._setup_function_controls(self.function.args)

    def _setup_function_controls(self, args):
        if not hasattr(self, 'function_controls'):
            # Raise a exception
            return

        self.function_controls.children = [] # Remove previous controls
        for arg in list(args.__dict__):
            property = getattr(args,arg)
            if not hasattr(property, 'type'):
                continue
            if property.type == UITypes.SLIDER_FLOAT:
                dcg.Slider(self.context,
                            parent=self.function_controls,
                            width=UIDimensions.side_panel_width/2,
                            format='float',
                            label=property.label,
                            value=property.value,
                            min_value=property.min_value,
                            max_value=property.max_value,
                            user_data=property,
                            callback=lambda _, target, value: getattr(target.user_data, 'callback')(value) if hasattr(target.user_data, 'callback') else setattr(target.user_data, 'value', value))
            elif property.type == UITypes.SLIDER_INT:
                dcg.Slider(self.context,
                            parent=self.function_controls,
                            width=UIDimensions.side_panel_width/2,
                            format='int',
                            label=property.label,
                            value=property.value,
                            min_value=property.min_value,
                            max_value=property.max_value,
                            user_data=property,
                            callback=lambda _, target, value: getattr(target.user_data, 'callback')(value) if hasattr(target.user_data, 'callback') else setattr(target.user_data, 'value', value))
            elif property.type == UITypes.INPUT_TEXT:
                dcg.InputText(self.context,
                            parent=self.function_controls,
                            width=UIDimensions.side_panel_width/2,
                            label=property.label,
                            value=property.value,
                            user_data=property,
                            callback=lambda _, target, value: getattr(target.user_data, 'callback')(value) if hasattr(target.user_data, 'callback') else setattr(target.user_data, 'value', value))

    def _set_function(self, function_name):
        self.function = self.function_list[function_name]
        self._setup_function_controls(self.function.args)
        self.function.init_flowfield()

    def setup_mask_controls(self):
        self.fade_slider = dcg.Slider(self.context,
                                      width=UIDimensions.side_panel_width/2,
                                      format="int",
                                      label='Fade',
                                      value=self.mask_fade.value,
                                      min_value=self.mask_fade.min_value,
                                      max_value=self.mask_fade.max_value,
                                      callback=lambda _0,_1, fade_value: self._set_mask_fade(fade_value))
        self.mask_combo = dcg.Combo(self.context, 
                                        width=UIDimensions.side_panel_width/2 ,
                                        items=list(self.mask_list.keys()),
                                        label='Function',
                                        value=Defaults.mask,
                                        callback=lambda _0, _1, mask_name: self._set_mask(mask_name))
        with dcg.VerticalLayout(self.context) as self.mask_controls:
            self._setup_mask_function_controls(self.mask.args)

    def _setup_mask_function_controls(self, args):
        if not hasattr(self, 'mask_controls') or not args:
            # Raise a exception
            return
        
        self.mask_controls.children = [] # Remove previous controls
        for arg in list(args.__dict__):
            property = getattr(args,arg)
            if not hasattr(property, 'type'):
                continue
            if property.type == UITypes.SLIDER_FLOAT:
                dcg.Slider(self.context,
                            parent=self.mask_controls,
                            width=UIDimensions.side_panel_width/2,
                            format='float',
                            label=property.label,
                            value=property.value,
                            min_value=property.min_value,
                            max_value=property.max_value,
                            user_data=property,
                            callback=lambda _, target, value: getattr(target.user_data, 'callback')(value) if hasattr(target.user_data, 'callback') else setattr(target.user_data, 'value', value))
            elif property.type == UITypes.SLIDER_INT:
                dcg.Slider(self.context,
                            parent=self.mask_controls,
                            width=UIDimensions.side_panel_width/2,
                            format='int',
                            label=property.label,
                            value=property.value,
                            min_value=property.min_value,
                            max_value=property.max_value,
                            user_data=property,
                            callback=lambda _, target, value: getattr(target.user_data, 'callback')(value) if hasattr(target.user_data, 'callback') else setattr(target.user_data, 'value', value))
            elif property.type == UITypes.INPUT_TEXT:
                dcg.InputText(self.context,
                            parent=self.mask_controls,
                            width=UIDimensions.side_panel_width/2,
                            label=property.label,
                            value=property.value,
                            user_data=property,
                            callback=lambda _, target, value: getattr(target.user_data, 'callback')(value) if hasattr(target.user_data, 'callback') else setattr(target.user_data, 'value', value))

    
    def _set_mask_fade(self, fade_value):
        self.mask_fade.value = fade_value

    def _set_mask(self, mask_name):
        self.mask = self.mask_list[mask_name]
        self._setup_mask_function_controls(self.mask.args)
        self.mask.init_mask()

    def handle_window_resize(self):
        self.function.init_flowfield()
        self.mask.init_mask()
        