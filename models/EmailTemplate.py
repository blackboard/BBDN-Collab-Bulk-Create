class EmailTemplate():

    def __init__(self, template_name='', values={}, html=True):
        self.template_name = template_name + '.template'
        self.values = values
        self.html = html

        self.TEMPLATE_DIR = 'emailtemplates/'

    def render(self):
        content = open(self.TEMPLATE_DIR + self.template_name).read()

        for k in self.values.keys():
            content = content.replace('[%s]' % k,self.values[k])

        return content