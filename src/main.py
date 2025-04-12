import sys

sys.path.append("./interface_graphique/")
from interface_graphique import interface_graphique as ig
import share
if __name__=='__main__':

    share.clear_tmp()
    share.replace_20_first_img_in_directory()
    app = ig.QApplication(sys.argv)
    window = ig.WelcomeScreen()
    window.show()
    sys.exit(app.exec())
