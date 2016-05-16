from os import path
import traceback

from growler import App
from growler.middleware import Logger, Static

# Apparently MakoRenderer is broken
# from growler_mako.mako_renderer import MakoRenderer
from mako.template import Template
from mako.lookup import TemplateLookup

import version
from vox_reddi_cli import parse_votes_for_post

app = App('VoxReddi')
app.use(Static(path='public'))
app.use(Logger())


def render_mako_template(filename, data):
    views_path = path.join(path.dirname(__file__), "views")
    templ_lookup = TemplateLookup(directories=[views_path])
    tmpl = Template(filename=path.join(views_path, "%s.mako" % filename), lookup=templ_lookup)
    return tmpl.render(**data)


@app.get('/')
def index(req, res):
    res.send_html(render_mako_template("home",
                                       {'version': version.version}))


@app.get('/poll')
def hello_world(req, res):
    try:
        post_id = req.param('poll')[0]
        (voters, vote_results, log) = parse_votes_for_post(post_id)
    except:
        exc_lines = traceback.format_exc().splitlines()
        res.send_html(render_mako_template("error",
                                           {'lines': exc_lines}))
    else:
        res.send_html(render_mako_template("result",
                                           {'voters': [v.name for v in voters],
                                            'vote_results': vote_results,
                                            'log': log,
                                            'post_id': post_id}))

app.create_server_and_run_forever(port=8080, host='0.0.0.0')
