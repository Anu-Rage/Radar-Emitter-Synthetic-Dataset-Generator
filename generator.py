import itertools
import random


def apply_tolerance(value, tolerance_percent):

    if value is None:
        return None

    if tolerance_percent == 0:
        return value

    delta = value * (tolerance_percent / 100)

    return round(
        random.uniform(
            value - delta,
            value + delta
        ),
        3
    )


def generate_tracks(
    freqs,
    pris,
    pws,
    scans,
    freq_tol,
    pri_tol,
    pw_tol,
    scan_tol,
    num_tracks,
    emitter
):

    rows = []

    # Handle optional scan
    if not scans:
        scans = [None]

    combinations = itertools.product(
        freqs,
        pris,
        pws,
        scans
    )

    for combo in combinations:

        freq, pri, pw, scan = combo

        for _ in range(num_tracks):

            row = {

                "frequency": apply_tolerance(
                    freq,
                    freq_tol
                ),

                "pri": apply_tolerance(
                    pri,
                    pri_tol
                ),

                "pw": apply_tolerance(
                    pw,
                    pw_tol
                ),

                "scan_rate": apply_tolerance(
                    scan,
                    scan_tol
                ),

                "emitter": emitter
            }

            rows.append(row)

    return rows