class stylesheet():
    def style(self):
        self.style = """
                    * {
                        background-color: #272822;
                        color: #f8f8f2;
                        font-family: Verdana;
                    }

                    QLabel#title {
                        text-align: center;
                        font-size: 20pt;
                        border: 3px solid #2cde85;
                        border-radius: 20px;
                    }
                    
                    QLineEdit#input_box {
                        border: 3px solid #2cde85;
                        border-radius: 10px;
                    }

                    QPushButton#reset_button {
                        border: 1px solid #2cde85;
                        border-radius: 3px;
                    }
                    
                    QPushButton#reset_button:hover {
                        background-color: #2cde85;
                        border: 3px solid white;
                    }
                """
        return self.style