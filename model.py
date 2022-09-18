from controller import miningDb


class mainModel:
    def runModel(self):
        file_type = ['png', 'jpg', 'JPG', 'PNG']
        players = ['player1', 'player2']

        newMiningDb = miningDb(file_type, players)
        # uexcorpReviewMinerals() curl uexcorp web page and updates minerals.json every time it runs
        newMiningDb.uexcorpReviewMinerals()
        # addOrder() appends an order id to db.json for all images contained in the img/ folder
        newMiningDb.addOrder()


if __name__ == '__main__':
    newMainModel = mainModel()
    newMainModel.runModel()