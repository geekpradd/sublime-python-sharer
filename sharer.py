import sublime, sublime_plugin,json
import urllib.parse,threading
import urllib.request

class ShareCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    self.content=self.FetchText()

    x=str(self.view.file_name())
    self.locationParams=self.getFileInfo(x)

    if self.check(self.locationParams):
      t= threading.Thread(target=self.rest)
      t.start()
  def rest(self):
    link=self.contactAPI(self.locationParams,self.content)

    sublime.set_clipboard(link)
    self.displayOutput(link)

  def check(self,param):
    values=['py','pyc','pyo','pyw']
    if param[3] in values:
      return True
    else:
      return False

  def FetchText(self):
    allCont=sublime.Region(0,self.view.size())
    content=self.view.substr(allCont)
    return content

  def getFileInfo(self,name):
    location  =       name
    name      =       location.split('\\')[-1]
    folder    =       location.replace(name,'')
    extension =       name.split('.')[-1]
    n         =       name.replace(extension,'')

    return [location,name,folder,extension,n]

  def contactAPI(self,params,con):
    url = 'http://www.sourcesharer.hol.es/create/save-api.php'

    values= {'language' : 'python',
          'code' : con,
          'name' : params[-1][:-1:] }
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)

    val=str(response.read())[4:-5:]

    return val

  def displayOutput(self,argv):
    msg="Your Python Source has been saved online for sharing at {0}. \n\nThis link has been copied to your clipboard\n\nPress Esc to Exit".format(argv)
    window=sublime.active_window()
    self.output_view = window.get_output_panel("textarea")
    window.run_command("show_panel", {"panel": "output.textarea"})
    self.output_view.set_read_only(False)
    self.output_view.run_command("append", {"characters": msg})
    self.output_view.set_read_only(True)
