<%inherit file="/base.mako"/>
<p><a href='http://redd.it/${post_id}'>Original post</a></p>
<h3>Results</h3>
<p>
    <% max_vote = vote_results[0][1] %>
    % for option, number in vote_results:
      <%
      vote_percent = int(number) / int(max_vote) * 100
      progress_bar_style = ''
      if number == max_vote:
          progress_bar_style = 'progress-bar-success'
      %>
      <div class="progress">
        <div class="progress-bar ${progress_bar_style}" role="progressbar" style="width: ${vote_percent}%">
          ${option}: <b>${number}</b>
        </div>
      </div>
    % endfor
  </ol>
</p>

<h4>Voting log</h4>
<pre>
  <code>
  % for line in log:
    ${line}
  % endfor
  </code>
</pre>

<h4>Voters</h4>
<ul>
% for voter in voters:
  <li><a href="http://www.reddit.com/user/${voter}">${voter}</a></li>
% endfor
</ul>
