#!/usr/bin/env python

import os
import sys

from .scorelib.rttm import load_rttm
from .scorelib.turn import merge_turns, trim_turns
from .scorelib.uem import gen_uem, load_uem
from .scorelib.score import score
from .scorelib.six import iterkeys
from .scorelib.utils import error, warn


def load_rttms(rttm_fns):
    """Load speaker turns from RTTM files.

    Parameters
    ----------
    rttm_fns : list of str
        Paths to RTTM files.

    Returns
    -------
    turns : list of Turn
        Speaker turns.

    file_ids : set
        File ids found in ``rttm_fns``.
    """
    turns = []
    file_ids = set()
    for rttm_fn in rttm_fns:
        if not os.path.exists(rttm_fn):
            error('Unable to open RTTM file: %s' % rttm_fn)
            sys.exit(1)
        try:
            turns_, _, file_ids_ = load_rttm(rttm_fn)
            turns.extend(turns_)
            file_ids.update(file_ids_)
        except IOError as e:
            error('Invalid RTTM file: %s. %s' % (rttm_fn, e))
            sys.exit(1)
    return turns, file_ids


def check_for_empty_files(ref_turns, sys_turns, uem):
    """Warn on files in UEM without reference or speaker turns."""
    ref_file_ids = {turn.file_id for turn in ref_turns}
    sys_file_ids = {turn.file_id for turn in sys_turns}
    for file_id in sorted(iterkeys(uem)):
        if file_id not in ref_file_ids:
            warn('File "%s" missing in reference RTTMs.' % file_id)
        if file_id not in sys_file_ids:
            warn('File "%s" missing in system RTTMs.' % file_id)
    # TODO: Clarify below warnings; this indicates that there are no
    #       ELIGIBLE reference/system turns.
    if not ref_turns:
        warn('No reference speaker turns found within UEM scoring regions.')
    if not sys_turns:
        warn('No system speaker turns found within UEM scoring regions.')


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
