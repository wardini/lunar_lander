from base import BaseState
from storage import Storage

class LoadScores(BaseState):
    def __init__(self,glbls):
        super(LoadScores, self).__init__(glbls)

    def startup(self):
        super(LoadScores,self).startup()

        self.storage = Storage(self.glbls["GAME_PREFIX"])
        self.glbls["STORAGE"]=self.storage

        s = self.storage.storage
        N = len(self.glbls['STATES']["GAMEPLAY"].levels)
        self.glbls["scores"]={'Level_'+str(i+1):None for i in range(N)}
        stored_version = s.get("version")
        if stored_version == self.glbls['VERSION'] or \
           stored_version in self.glbls['COMPATABLE_VERSIONS']:

            for i in range(N):
                self.glbls["scores"]["Level_"+str(i+1)]=s.get("Level_"+str(i+1),None)

        if stored_version != self.glbls['VERSION']:
            self.save_scores_and_version()

        self.next_state = "MENU"
        self.done = True

    def save_scores_and_version(self):
        save_dict = {'version':self.glbls['VERSION']}

        for k in self.glbls["scores"].keys():
            save_dict[k] = self.glbls["scores"][k]
        self.storage.clear_and_store_dict(save_dict)




