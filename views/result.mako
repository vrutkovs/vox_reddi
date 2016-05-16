<%inherit file="/base.mako"/>
<p>
  <ol>
    % for option, number in vote_results:
    <li>${option}: <b>${number}</b></li>
    % endfor
  </ol>
</p>

<h3>Voters</h3>
<ul>
% for voter in voters:
  <li><a href="http://www.reddit.com/user/${voter}">${voter}</a></li>
% endfor
</ul>
<p><a href='http://redd.it/${post_id}'>Original post</a></p>

<h3>Voting log</h3>
<pre>
  <code>
  % for line in log:
    ${line}
  % endfor
  </code>
</pre>
