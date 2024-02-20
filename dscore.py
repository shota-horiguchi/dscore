#!/usr/bin/env python

from score import check_for_empty_files
from score import load_rttms
from scorelib.turn import merge_turns, trim_turns
from scorelib.uem import gen_uem, load_uem
from scorelib.score import score


def calc_der(ref_rttm, sys_rttm, uem=None,
             collar=0.0, ignore_overlaps=False):
    ref_turns, _ = load_rttms(ref_rttm)
    sys_turns, _ = load_rttms(sys_rttm)

    args.ref_rttm_fns = load_script_file(ref_rttm)
    args.sys_rttm_fns = load_script_file(sys_rttm)

    if uem is not None:
        uem = load_uem(uems)
    else:
        uem = gen_uem(ref_turns, sys_turns)

    ref_turns = trim_turns(ref_turns, uem)
    sys_turns = trim_turns(sys_turns, uem)
    ref_turns = merge_turns(ref_turns)
    sys_turns = merge_turns(sys_turns)

    # Score.
    check_for_empty_files(ref_turns, sys_turns, uem)
    file_scores, global_scores = score(
        ref_turns, sys_turns, uem, step=args.step,
        jer_min_ref_dur=args.jer_min_ref_dur, collar=args.collar,
        ignore_overlaps=args.ignore_overlaps)

    return {
        'der': global_scores['der'],
        'miss': global_scores['miss'],
        'falarm': global_scores['falarm'],
        'confusion': global_scores['confusion'],
    }
