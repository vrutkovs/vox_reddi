<%inherit file="/base.mako"/>
<h3>Results</h3>
<p>
  <ol>
    % for option, number in vote_results:
    <li>${option}: <b>${number}</b></li>
    % endfor
  </ol>
</p>

<h4>Voters</h4>
<ul>
% for voter in voters:
  <li><a href="http://www.reddit.com/user/${voter}">${voter}</a></li>
% endfor
</ul>
<p><a href='http://redd.it/${post_id}'>Original post</a></p>

<h4>Voting log</h4>
<pre>
  <code>
  % for line in log:
    ${line}
  % endfor
  </code>
</pre>
