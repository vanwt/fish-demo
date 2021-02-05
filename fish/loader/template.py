import os


class TemplateLoader:
    def __init__(self, template_dir_name: str = "template"):
        self.cwd = os.getcwd()
        self._template_dir_name = template_dir_name
        self.template_path = os.path.join(self.cwd, self.template_path_name)
        self.suffix = ".html"

    def make_tmp_path(self, path):
        if "/" in path:
            path = path.split("/")
        else:
            path = [path]
        return path

    @property
    def template_path_name(self):
        return self._template_dir_name

    @template_path_name.setter
    def template_path_name(self, name):
        self._template_dir_name = name
        self.template_path = os.path.join(self.cwd, name)

    def __call__(self, html_file_name: str = None):
        if not html_file_name:
            raise AttributeError("Please fill in the Html file name!")
        if not html_file_name.endswith(self.suffix):
            html_file_name += self.suffix
        return os.path.join(self.template_path, *self.make_tmp_path(html_file_name))
