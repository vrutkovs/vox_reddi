# The MIT License (MIT)
# Copyright (c) 2016 roignac@gmail.com
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
import argparse
import sys
import asyncio
import json
from datetime import datetime
from collections import Counter
from version import version

PY_VERSION = 3
if sys.version_info[0] < 3:
    PY_VERSION = 2

USER_AGENT = "Vox Reddi %s" % version
VOTE_REGEXP = re.compile('^\s*\+(\w+)', re.UNICODE | re.IGNORECASE)
MINIMUM_REGISTERED_TIME_IN_DAYS = 30


class UnparsableComment(Exception):
    def __init__(self, comment):
        self.comment_id = comment.id
        self.author = comment.author

    def __repr__(self):
        return u"Cannot parse comment id %s by %s" % (self.comment_id, self.author)


class VoteException(Exception):
    def __init__(self, option, voter, commentid, message):
        self.option = option
        self.voter = voter
        self.message = message
        self.commentid = commentid

    def __repr__(self):
        message = u"Ignoring vote by {} for '{}' in '{}' - {}".format(
                  self.voter, self.option, self.commentid, self.message)
        if PY_VERSION == 2:
            message = message.encode("utf-8")
        return message


async def parse_comment(comment, voters):
    commentid = comment.id
    comment_body = comment.body
    match = re.match(VOTE_REGEXP, comment_body)

    if not match:
        raise UnparsableComment(comment)

    option = match.group(1).title()
    voter = comment.author
    if voter is None:
        raise VoteException(option, voter, commentid, "account was removed")

    voter_created_date = datetime.fromtimestamp(voter.created_utc)
    datediff = datetime.utcnow() - voter_created_date
    if datediff.days < MINIMUM_REGISTERED_TIME_IN_DAYS:
        raise VoteException(option, voter, commentid, "registered %s days ago" % datediff.days)

    if voter in voters:
        raise VoteException(option, voter, commentid, "has already voted")

    if comment.edited:
        raise VoteException(option, voter, commentid, "comment has been edited")

    return (option, voter)


def ws_send_msg(ws, message):
    return ws.send_str(json.dumps(message))


async def start_parsing_votes_for_post(submission_id, ws):
    # import praw as late as possible
    import praw

    options = []
    voters = []

    r = praw.Reddit(user_agent=(USER_AGENT))
    submission = r.get_submission(submission_id=submission_id)
    announcement_date = datetime.fromtimestamp(submission.created_utc)
    date_diff = datetime.utcnow() - announcement_date
    ws_send_msg(ws, {"log": "%s since submission date" % date_diff})
    ws_send_msg(ws, {"log": "Counting votes in %s" % submission.id})
    top_level_comments = submission.comments
    for comment in top_level_comments:
        try:
            (option, voter) = await parse_comment(comment, voters)
            options.append(option)
            voters.append(voter)
            ws_send_msg(ws, {"log": "Recorded vote for '%s' by %s, commentid %s" % (option, voter, comment.id)})
        except (VoteException, UnparsableComment) as e:
            ws_send_msg(ws, {"log": repr(e)})

    ws_send_msg(ws, {"voters": [v.name for v in voters]})
    ws_send_msg(ws, {"results": Counter(options).most_common()})
