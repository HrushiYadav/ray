"""APIs-tab sidebar (Pattern B): scope the isolated apis sidebar to apis/ pages.

Overrides context["sidebars"] for apis/ pages instead of using
html_sidebars["apis/**"] (which double-matches "**" and emits a fatal "matches
two patterns" warning). The template name needs ".html" because the theme
includes it as-is (`{% include sidebartemplate %}`).

A render-once cache of this sidebar was prototyped and measured NET-NEGATIVE at
this sidebar size (the per-page bs4 rewrite of the large collapse=False tree costs
more than re-rendering, ~18% slower full build, no artifact-size change). So the
sidebar is rendered directly. A proper scoped cache belongs with the DOC-937
preload_sidebar_nav rework.
"""
APIS_PREFIX = "apis"


def _on_html_page_context(app, pagename, templatename, context, doctree):
    if not (pagename == APIS_PREFIX or pagename.startswith(APIS_PREFIX + "/")):
        return
    # Orphan pages (e.g. a library's deprecated-API ref) are deliberately not in
    # any toctree, so they have no ancestry for generate_toctree_html(startdepth=1)
    # to root a fragment at ("no suitable ancestor found to act as root node").
    # Leave those on the global sidebar; every other apis page gets the scoped one.
    if "orphan" in app.env.metadata.get(pagename, {}):
        return
    context["sidebars"] = ["api-sidebar.html"]


def setup(app):
    # priority > 500 so the theme has set context["sidebars"] before we override it.
    app.connect("html-page-context", _on_html_page_context, priority=900)
    return {"version": "0.5", "parallel_read_safe": True, "parallel_write_safe": True}
