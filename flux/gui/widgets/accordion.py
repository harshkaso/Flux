from flux.gui.widgets.collapsible_panel import CollapsiblePanel


class Accordion:
    def __init__(self) -> None:
        self._panels: list[CollapsiblePanel] = []

    def add_panel(
        self,
        label: str,
        default_open: bool = False,
    ) -> CollapsiblePanel:
        panel = CollapsiblePanel(
            label=label,
            default_open=default_open,
            on_toggle=self._on_panel_toggle,
        )

        self._panels.append(panel)
        return panel

    def _on_panel_toggle(self, opened: CollapsiblePanel) -> None:
        if not opened.is_open:
            return

        for panel in self._panels:
            if panel is not opened:
                panel.close()
