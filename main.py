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

import praw
import re
import argparse
from datetime import datetime
from collections import Counter

USER_AGENT = "Vox Reddi 0.1"
VOTE_REGEXP = re.compile('\s*\+(\w+)')
MINIMUM_REGISTERED_TIME_IN_DAYS = 30

parser = argparse.ArgumentParser()
parser.add_argument("--submission")
args = parser.parse_args()
submission = args.submission
print("Counting votes in %s" % submission)

options = []
voters = []

r = praw.Reddit(user_agent=(USER_AGENT))
submission = r.get_submission(submission_id=submission)
top_level_comments = submission.comments
for comment in top_level_comments:
    if comment.edited:
        print("Discarding %s - edited" % comment.id)
        continue

    comment_body = comment.body
    match = re.match(VOTE_REGEXP, comment_body)
    if match:
        option = match.group(1)
        voter = comment.author

        voter_created_date = datetime.fromtimestamp(voter.created_utc)
        datediff = datetime.utcnow() - voter_created_date
        if datediff.days < MINIMUM_REGISTERED_TIME_IN_DAYS:
            print('Ignoring vote by %s for %s - registered %s days ago' % (
                (option, voter, datediff.days)))
            continue

        if voter in voters:
            print('Ignoring vote by %s for %s - has already voted' % ((option, voter)))
            continue
        options.append(option)
        voters.append(voter)
        print("Recorded vote for '%s', by %s" % (option, voter))
    else:
        stripped_comment = comment_body[:50]
        print("Cannot parse comment id %s, contents:\n'%s'" % (comment.id, stripped_comment))

vote_results = Counter(options)

print('Voters:\n%s' % voters)
print('Vote results:\n%s' % vote_results)
