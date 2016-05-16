<%inherit file="/base.mako"/>
<pre>
  <code>
    % for line in lines:
      > ${line}
    % endfor
  </code>
</pre>
