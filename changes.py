"""Changelog."""
import sublime
import sublime_plugin
import webbrowser

CSS = '''
html { {{'.background'|css}} }
div.apply-syntax { padding: 0; margin: 0; {{'.background'|css}} }
.apply-syntax h1, .apply-syntax h2, .apply-syntax h3,
.apply-syntax h4, .apply-syntax h5, .apply-syntax h6 {
    {{'.string'|css('color')}}
}
.apply-syntax blockquote { {{'.comment'|css('color')}} }
.apply-syntax a { text-decoration: none; }
'''

class ApplySyntaxChangesCommand(sublime_plugin.WindowCommand):
    """Changelog command."""

    def run(self):
        """Show the changelog in a new view."""
        try:
            import mdpopups
            has_phantom_support = (mdpopups.version() >= (1, 7, 3)) and (int(sublime.version()) >= 3118)
        except Exception:
            has_phantom_support = False

        text = sublime.load_resource('Packages/ApplySyntax/CHANGES.md')
        view = self.window.new_file()
        view.set_name('ApplySyntax - Changelog')
        view.settings().set('gutter', False)
        if has_phantom_support:
            html = '<div class="apply-syntax">%s</div>' % mdpopups.md2html(view, text)
            mdpopups.add_phantom(
                view, 'changelog', sublime.Region(0), html, sublime.LAYOUT_INLINE, css=CSS, on_navigate=self.on_navigate
            )
        else:
            view.run_command('insert', {"characters": text})
        view.set_read_only(True)
        view.set_scratch(True)

    def on_navigate(self, href):
        """Open links."""
        webbrowser.open_new_tab(href)
