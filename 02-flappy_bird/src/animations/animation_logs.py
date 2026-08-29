from gale.timer import Timer

import settings

def animate_log_gap(log_pair) -> None:
        min_gap = 1
        max_gap = 80
        duration_close = 0.75
        duration_open = 2

        def open_gap():
            if log_pair.is_out_of_game():
                return

            Timer.tween(
                duration_open,
                [(log_pair, {"gap": max_gap})],
                ease_function_name="in_out_sine",
                on_finish=close_gap
            )
            
        def close_gap():
            if log_pair.is_out_of_game():
                return

            def choke():
                if not log_pair.is_out_of_game():
                        settings.SOUNDS["choke"].play()
                        open_gap()

            Timer.tween(
                duration_close,
                [(log_pair, {"gap": min_gap})],
                ease_function_name="linear",
                on_finish=choke
            )

        close_gap()