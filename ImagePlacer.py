import sublime, sublime_plugin, os, re

SETTINGS = sublime.load_settings("ImagePlacer.sublime-settings")
IMAGE_PATH = SETTINGS.get('imagefolder')
if IMAGE_PATH == None:
    IMAGE_PATH = "images"

def insert_image(selected_image):
    imagetag = '<img alt="" src="{0}" />'.format(selected_image)
    view = sublime.active_window().active_view()
    edit = view.begin_edit()
    for region in view.sel():
        view.replace(edit, region, imagetag)
    view.end_edit(edit) 

def get_current_path(self):
    current_file = self.view.file_name()
    index = current_file.rfind('/')
    current_dir = current_file[:index]
    return current_dir

class PlaceImageCommand(sublime_plugin.TextCommand):
    global IMAGE_PATH
    def run(self, edit):
        current_dir = get_current_path(self)

        imagefiles = [os.path.join(root, name)
            for root, dirs, files in os.walk(current_dir+"/"+IMAGE_PATH)
                for name in files
                    if name.endswith((".png", ".jpg", ".gif"))]

        imagefiles = [w.replace(current_dir+"/", '') for w in imagefiles]

        def on_enter(selected_image):
            if selected_image != -1:
                insert_image(imagefiles[selected_image])
        sublime.active_window().show_quick_panel(imagefiles, on_enter)
