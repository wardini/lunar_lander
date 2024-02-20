import ast

class Storage():
    def __init__(self,prefix=""):
        self.prefix = prefix
        if __import__("sys").platform == "emscripten":
            self.use_platform = True
            import platform
            self.ls = platform.window.localStorage
        else:
            self.use_platform = False

        if self.use_platform:
            self.storage={}
            for i in range(self.ls.length):
                k = self.ls.key(i)
                if k == self.prefix+'version' or self.prefix+'Level' in k:
                    if self.ls.getItem(k) == 'null':
                        self.storage[k[len(self.prefix):]]=None
                    else:
                        if k == self.prefix+'version':
                            self.storage[k[len(self.prefix):]]=float(self.ls.getItem(k))
                        else:
                            self.storage[k[len(self.prefix):]]=str(self.ls.getItem(k))
        else:
            try:
                with open('local_storage.txt','r') as f:
                    self.storage = ast.literal_eval(f.readline())
            except:
                self.storage={'version':0}

        if 'version' not in self.storage.keys():
            self.storage={'version':0}

    def clear_and_store_dict(self,d):
        if self.use_platform:
            #self.ls.clear()
            for k in d.keys():
                print(k,d[k])
                self.ls.setItem(self.prefix+k,d[k])
        else:
            with open('local_storage.txt','w') as f:
                f.write(str(d))


