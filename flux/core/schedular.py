from __future__ import annotations

from collections.abc import Callable
from typing import Any

import dearpygui.dearpygui as dpg  # type: ignore


class Scheduler:
    """Schedules callbacks relative to DearPyGui's render loop."""

    @staticmethod
    def next_frame(callback: Callable[[], None]) -> None:
        """Execute the callback on the next frame."""
        dpg.set_frame_callback(
            dpg.get_frame_count() + 1,
            callback,
        )

    @staticmethod
    def after_frames(
        frames: int,
        callback: Callable[[], None],
    ) -> None:
        """Execute the callback after `frames` render frames."""
        dpg.set_frame_callback(
            dpg.get_frame_count() + max(frames, 0),
            callback,
        )

    @staticmethod
    def defer_until(
        predicate: Callable[[], bool],
        callback: Callable[[], None],
        *,
        max_frames: int = 60,
    ) -> None:
        """
        Poll `predicate` every frame until it returns True,
        then execute `callback`.

        If `predicate` never becomes True, `callback` is still
        executed after `max_frames` frames.
        """

        attempts = 0

        def check() -> None:
            nonlocal attempts

            if predicate():
                callback()
                return

            attempts += 1

            if attempts >= max_frames:
                callback()
                return

            Scheduler.next_frame(check)

        check()

    @staticmethod
    def defer_until_stable(
        state: Callable[[], Any],
        callback: Callable[[], None],
        *,
        stable_frames: int = 2,
        max_frames: int = 60,
    ) -> None:
        """
        Polls `state()` once per frame until its value has remained
        unchanged for `stable_frames` consecutive frames.

        Useful for waiting for DearPyGui layout to settle.
        """
        previous = object()
        stable = 0
        attempts = 0

        def check() -> None:
            nonlocal previous, stable, attempts

            current = state()
            if current == previous:
                stable += 1
            else:
                previous = current
                stable = 0

            if stable >= stable_frames:
                callback()
                return

            attempts += 1

            if attempts >= max_frames:
                callback()
                return

            Scheduler.next_frame(check)

        Scheduler.next_frame(check)

    @staticmethod
    def every_frame(
        callback: Callable[[], bool | None],
    ) -> None:
        """
        Execute `callback` every frame.

        If callback returns False, scheduling stops.
        """

        def tick() -> None:
            if callback() is False:
                return

            Scheduler.next_frame(tick)

        tick()
