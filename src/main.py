import sys
import os
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),"interface_graphique"))

from interface_graphique import main_interface_graphique as ig
import share


def main():
    share.clear_tmp()
    share.replace_20_first_img_in_directory()
    app = ig.QApplication(sys.argv)
    window = ig.WelcomeScreen()
    window.show()
    sys.exit(app.exec())

if __name__=='__main__':
    main()

