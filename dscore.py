#!/usr/bin/env python

from .score import check_for_empty_files
from .score import load_rttms
from dscore.scorelib.turn import merge_turns, trim_turns
from dscore.scorelib.uem import gen_uem, load_uem
from dscore.scorelib.score import score


def calc_der(ref_rttm, sys_rttm, uem=None,
             collar=0.0, ignore_overlaps=False):
    ref_turns, _ = load_rttms(ref_rttm)
    sys_turns, _ = load_rttms(sys_rttm)

    if uem is not None:
        uem = load_uem(uem)
    else:
        uem = gen_uem(ref_turns, sys_turns)

    ref_turns = trim_turns(ref_turns, uem)
    sys_turns = trim_turns(sys_turns, uem)
    ref_turns = merge_turns(ref_turns)
    sys_turns = merge_turns(sys_turns)

    # Score.
    check_for_empty_files(ref_turns, sys_turns, uem)
    file_scores, global_scores = score(
        ref_turns, sys_turns, uem, step=0.010,
        jer_min_ref_dur=0.0, collar=collar,
        ignore_overlaps=ignore_overlaps)

    return global_scores
