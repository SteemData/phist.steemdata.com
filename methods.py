from contextlib import suppress

import diff_match_patch
import ghdiff
from funcy.seqs import first, rest
from steem.utils import resolve_identifier


def comment_history(db, uri_or_identifier):
    with suppress(TypeError, ValueError):
        identifier = parse_identifier(uri_or_identifier)
        return get_comment_history(db, *resolve_identifier(identifier))


def parse_identifier(uri):
    return '@%s' % uri.split('@')[-1]


def get_comment_history(db, author, permlink):
    conditions = {
        # 'account': author,
        'author': author,
        'type': 'comment',
        'permlink': permlink,
    }
    return list(db['Operations'].find(conditions).sort('timestamp', 1))


def reverse_patch(body_diffs):
    """ Take a diff_match_patch C++ library diffs, and re-create original full-body texts."""
    p = diff_match_patch.diff_match_patch()

    original, *diffs = body_diffs
    full_versions = [original]
    for diff in diffs:
        try:
            reverse = p.patch_apply(p.patch_fromText(diff), full_versions[-1])
            full_versions.append(reverse[0])
        except ValueError:
            # some comments have their bodies overwritten completely, rather than diffed
            full_versions.append(diff)

    return full_versions


def recreate_body_diffs(comments):
    """
    Take a list of comments, extract their bodies, re-create full text from diffs and generate pretty html diffs.
    Returns: (OriginalText, [diffs])
    """
    body_diffs = [x['body'] for x in comments]

    full_versions = reverse_patch(body_diffs)

    results = [full_versions[0]]
    for i, diff in enumerate(full_versions[1:]):
        results.append(ghdiff.diff(full_versions[i], diff).replace('\n', ''))

    return first(results), list(rest(results))
