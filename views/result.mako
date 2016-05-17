<%inherit file="/base.mako"/>
<p><a href='http://redd.it/${post_id}'>Original post</a></p>

<div id="results-container" style="display: none">
  <h3>Results</h3>
  <p id="results"></p>
</div>

<div id="voters-container" style="display: none">
  <h4>Voters</h4>
  <p>Total: <span id="total-voted"></span></p>
  <ul id="voters"></ul>
</div>

<h4>Voting log</h4>
<pre id="log"></pre>

<script>
  $(document).ready(function () {
    var sock = new WebSocket('ws://' + window.location.host + '${ws_url}');
    sock.onmessage = function(event) {
        dta = $.parseJSON(event.data);
        if (Object.keys(dta)[0] == 'log'){
          $('#log').append(document.createTextNode(dta.log + '\n'));
        }
        if (Object.keys(dta)[0] == 'voters'){
          dta.voters.forEach(function(voter){
            $("#voters").append("<li><a href='http://reddit.com/u/"+voter+"/'>"+voter+"</a></li>");
          })
          $("#total-voted").append(document.createTextNode(dta.voters.length));
          $("#voters-container").show();
        }
        if (Object.keys(dta)[0] == 'results'){
          var first_result = dta.results[0][1];
          dta.results.forEach(function(result){
            var vote_percent = result[1] / first_result * 100;
            var progress_bar_style = '';
            if (result[1] == first_result) {
              progress_bar_style = 'progress-bar-success';
            }
            $("#results").append("<div class='progress'><div class='progress-bar " + progress_bar_style +"' role='progressbar' style='width: " + vote_percent + "%'><p class='text-left' style='margin-left: 10px'>" + result[0] + ": <b>"+ result[1] + "</b></p></div></div>");
          });
          $("#results-container").show();
        }
    };
    sock.onopen = function(){
      sock.send("ready");
    }
  });
</script>
