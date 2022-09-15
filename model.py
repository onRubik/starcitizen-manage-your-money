from controller import miningDb


class mainModel:
    def runModel(self):
        file_type = ['png', 'jpg', 'JPG', 'PNG']
        players = ['viper', 'nj']

        newMiningDb = miningDb(file_type, players)
        # newMiningDb.uexcorpReviewMinerals()
        # newMiningDb.rewriteImage()
        # newMiningDb.cleanInput()
        newMiningDb.addOrder()


if __name__ == '__main__':
    newMainModel = mainModel()
    newMainModel.runModel()