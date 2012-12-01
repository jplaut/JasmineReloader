import sublime, sublime_plugin
import sys
from subprocess import call

s = sublime.load_settings('JasmineReloader.sublime-settings')

class JasmineReloader(sublime_plugin.EventListener):
  def on_post_save(self, view):
    if view.file_name().count("_spec.js") > 0:
      if s.get('browser') and s.get('jasmine_page_title'):
        if s.get('browser') == 'Google Chrome':
          command = """
            tell application "%s"
              set theTitle to "%s"

              set found to false
              repeat with theWindow in every window
                repeat with theTab in every tab of theWindow
                  if theTab's title = theTitle then
                    set found to true
                  exit repeat
                  end if
                end repeat
    
                if found then
                  tell theTab to reload
                  exit repeat
                end if
              end repeat
            end tell
              """ % (s.get('browser'), s.get('jasmine_page_title'))
        elif s.get('browser') == 'Safari':
          command = """
            tell application "Safari"
              set theTitle to "Jasmine Spec Runner"
              
              set found to false
              repeat with theWindow in every window
                repeat with theTab in every tab of theWindow
                  if theTab's name = theTitle then
                    set found to true
                    exit repeat
                  end if
                end repeat
                
                if found then
                  tell theTab
                    do JavaScript "document.location.reload()"
                  end tell
                  exit repeat
                end if
              end repeat
            end tell
          """

        elif s.get('browser') == 'Firefox':
          sublime.error_message("Currently, Firefox does not have great Applescript support. Please choose another browser.")

        call(['osascript', '-e', command])