import sys
from os.path import dirname, join

from PyQt6.QtCore import QLocale, QSettings, Qt, QTranslator
from PyQt6.QtGui import QActionGroup, QIcon
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox
from sympy import E, Rational, cos, exp, log, pi, sin, sqrt, sympify, tan
from sympy.physics import units

from .ui import Ui_MainWindow


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.sum()

    def sum(self):
        buttons = [
            self.ui.btn_0,
            self.ui.btn_1,
            self.ui.btn_2,
            self.ui.btn_3,
            self.ui.btn_4,
            self.ui.btn_5,
            self.ui.btn_6,
            self.ui.btn_7,
            self.ui.btn_8,
            self.ui.btn_9,
            self.ui.btn_dot,
            self.ui.btn_plus,
            self.ui.btn_minus,
            self.ui.btn_multiple,
            self.ui.btn_divide,
            self.ui.btn_leftbracket,
            self.ui.btn_rightbracket,
            self.ui.btn_0_2,
            self.ui.btn_1_2,
            self.ui.btn_2_2,
            self.ui.btn_3_2,
            self.ui.btn_4_2,
            self.ui.btn_5_2,
            self.ui.btn_6_2,
            self.ui.btn_7_2,
            self.ui.btn_8_2,
            self.ui.btn_9_2,
            self.ui.btn_dot_2,
            self.ui.btn_plus_2,
            self.ui.btn_minus_2,
            self.ui.btn_multiple_2,
            self.ui.btn_divide_2,
            self.ui.btn_leftbracket_2,
            self.ui.btn_rightbracket_2,
        ]

        for button in buttons:
            button.clicked.connect(lambda checked, btn=button: self.write_symbol(btn.text()))

        equal_buttons = [self.ui.btn_equal, self.ui.btn_equal_2, self.ui.btn_equal_3]
        for btn_equal in equal_buttons:
            btn_equal.clicked.connect(self.calculate)
        clear_buttons = [self.ui.btn_clear, self.ui.btn_clear_2]
        for btn_clear in clear_buttons:
            btn_clear.clicked.connect(self.clear_line_result)
        del_buttons = [self.ui.btn_del, self.ui.btn_del_2]
        for btn_del in del_buttons:
            btn_del.clicked.connect(self.del_text)
        self.ui.clear_journal_btn.clicked.connect(self.clear_journal)
        self.ui.save_journal_btn.clicked.connect(self.save_journal)

        self.ui.btn_log.clicked.connect(self.log)
        self.ui.btn_sin.clicked.connect(self.sin)
        self.ui.btn_cos.clicked.connect(self.cos)
        self.ui.btn_tan.clicked.connect(self.tan)
        self.ui.btn_exp.clicked.connect(self.exp)
        self.ui.btn_pi.clicked.connect(self.pi)
        self.ui.btn_e.clicked.connect(self.e)
        self.ui.btn_procent.clicked.connect(self.procent)
        self.ui.btn_square.clicked.connect(self.square)
        self.ui.btn_radical.clicked.connect(self.radical)

        self.ui.length_convert_btn.clicked.connect(self.convert_length)
        self.ui.weight_convert_btn.clicked.connect(self.convert_weight)
        self.ui.time_convert_btn.clicked.connect(self.convert_time)
        self.ui.volume_convert_btn.clicked.connect(self.convert_volume)
        self.ui.information_convert_btn.clicked.connect(self.convert_information)
        self.ui.pressure_convert_btn.clicked.connect(self.convert_pressure)

        self.ui.action_standard.triggered.connect(self.switch_to_standard)
        self.ui.action_engineer.triggered.connect(self.switch_to_engineer)
        self.ui.action_paper.triggered.connect(self.switch_to_paper)
        self.ui.action_unit_converter.triggered.connect(self.switch_to_unit_converter)

        self.ui.action_copy.triggered.connect(self.line_result_copy)
        self.ui.action_cut.triggered.connect(self.line_result_cut)
        self.ui.action_paste.triggered.connect(self.line_result_paste)

        self.ui.action_line_top.triggered.connect(self.line_top)
        self.ui.action_line_down.triggered.connect(self.line_down)

        self.ui.action_about_program.triggered.connect(self.show_about_program)
        self.ui.action_about_qt.triggered.connect(self.show_about_qt)

        mode_group = QActionGroup(self)
        mode_group_actions = [
            self.ui.action_standard,
            self.ui.action_engineer,
            self.ui.action_paper,
            self.ui.action_unit_converter,
        ]
        for action in mode_group_actions:
            mode_group.addAction(action)
            action.setCheckable(True)

        # Load settings
        settings = QSettings("pyqulator")
        mode = settings.value("mode", "standard")
        paper_mode_line = settings.value("paper_mode_line", "down")
        window_state = settings.value("window_state")

        if mode == "standard":
            self.ui.action_standard.setChecked(True)
            self.switch_to_standard()
        elif mode == "engineer":
            self.ui.action_engineer.setChecked(True)
            self.switch_to_engineer()
        elif mode == "paper":
            self.ui.action_paper.setChecked(True)
            self.switch_to_paper()
        else:
            self.ui.action_unit_converter.setChecked(True)
            self.switch_to_unit_converter()

        if paper_mode_line == "down":
            self.line_down()
        if paper_mode_line == "top":
            self.line_top()

        if window_state == "maximized":
            self.showMaximized()
        elif window_state:
            self.resize(window_state)

    # Save window state
    def closeEvent(self, event):  # noqa
        settings = QSettings("pyqulator")
        if self.isMaximized():
            settings.setValue("window_state", "maximized")
        else:
            settings.setValue("window_state", self.size())
        event.accept()

    # Keyboard key handling
    def keyPressEvent(self, event):  # noqa
        if self.ui.stackedwidget.currentIndex() in {0, 1}:
            self.current_line_result.clearFocus()
            if (
                event.key() in range(Qt.Key.Key_0, Qt.Key.Key_9 + 1)
                or event.key()
                in (Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Slash, Qt.Key.Key_Asterisk, Qt.Key.Key_Period)
                or event.key() == Qt.Key.Key_ParenLeft
                or event.key() == Qt.Key.Key_ParenRight
            ):
                symbol = event.text()
                self.write_symbol(symbol)
            elif event.key() == Qt.Key.Key_Backspace:
                self.del_text()
            elif event.key() == Qt.Key.Key_Delete:
                self.clear_line_result()
            elif event.key() == Qt.Key.Key_C:
                self.line_result_copy()
            elif event.key() == Qt.Key.Key_X:
                self.line_result_cut()
            elif event.key() == Qt.Key.Key_V:
                self.line_result_paste()
            elif event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                self.calculate()

    # Input of symbols on standard and engineer modes
    def write_symbol(self, symbol):
        if self.current_line_result.text() == "0" and symbol not in ["+", "-", "*", "/", "."]:
            self.current_line_result.setText(symbol)
        elif self.current_line_result.text().endswith((".", "(", ")")) and symbol in [".", "(", ")"]:
            pass
        elif self.current_line_result.text().endswith(("+", "-", "*", "/")) and symbol in [
            ".",
            "+",
            "-",
            "*",
            "/",
            ")",
        ]:
            pass
        elif self.current_line_result.text().endswith(tuple("0123456789")) and symbol in ["("]:
            pass
        else:
            self.current_line_result.setText(self.current_line_result.text() + symbol)

    # Calculate
    def calculate(self):
        try:
            expression = self.current_line_result.text()
            res = str(sympify(expression).evalf()).rstrip("0").rstrip(".")  # Remove zeros and dots from the end
            self.current_line_result.setText(res)
            self.ui.journal.addItem(f"{expression} = {res}")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # Clear result line
    def clear_line_result(self):
        self.ui.line_result.setText("0")
        self.ui.line_result_2.setText("0")
        self.ui.line_result_3.setText("")
        self.ui.input_line_unit.setText("")
        self.ui.output_line_unit.setText("")

    # Delete last symbol
    def del_text(self):
        if len(self.current_line_result.text()) > 1 and self.current_line_result.text() != "0":
            self.current_line_result.setText(self.current_line_result.text()[:-1])
        elif len(self.current_line_result.text()) <= 1 and self.current_line_result.text() != "0":
            self.current_line_result.setText("0")

    # Engineer mode operations
    def log(self):
        try:
            res = log(sympify(self.current_line_result.text()).evalf())
            self.current_line_result.setText(str(res).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def sin(self):
        try:
            res = sin(sympify(self.current_line_result.text()).evalf())
            self.current_line_result.setText(str(res).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def cos(self):
        try:
            res = cos(sympify(self.current_line_result.text()).evalf())
            self.current_line_result.setText(str(res).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def tan(self):
        try:
            res = tan(sympify(self.current_line_result.text()).evalf())
            self.current_line_result.setText(str(res).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def exp(self):
        try:
            res = exp(sympify(self.current_line_result.text()).evalf())
            self.current_line_result.setText(str(res).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def pi(self):
        try:
            if self.current_line_result.text() == "" or self.current_line_result.text() == "0":
                self.current_line_result.setText(str(pi.evalf()))
            else:
                res = (pi * sympify(self.current_line_result.text())).evalf()
                self.current_line_result.setText(str(res).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def e(self):
        try:
            if self.current_line_result.text() == "" or self.current_line_result.text() == "0":
                self.current_line_result.setText(str(E.evalf()))
            else:
                res = (E * sympify(self.current_line_result.text())).evalf()
                self.current_line_result.setText(str(res).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def procent(self):
        try:
            res = (sympify(self.current_line_result.text()) / Rational(100)).evalf()
            self.current_line_result.setText(str(res).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def radical(self):
        try:
            res = (sympify(self.current_line_result.text())).evalf()
            self.current_line_result.setText(str(sqrt(res)).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def square(self):
        try:
            res = (sympify(self.current_line_result.text()) * sympify(self.current_line_result.text())).evalf()
            self.current_line_result.setText(str(res).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # Journal functions
    def clear_journal(self):
        self.ui.journal.clear()

    def save_journal(self):
        file_path = QFileDialog.getSaveFileName(self)[0]
        if file_path:
            if not file_path.endswith(".txt"):
                file_path += ".txt"
            with open(file_path, "w") as file:
                for i in range(self.ui.journal.count()):
                    item = self.ui.journal.item(i).text()
                    file.write(item + "\n")

    # Unit converter functions
    def convert_length(self):
        try:
            input_value = Rational(self.ui.input_line_unit.text())
            input_index = self.ui.input_length_combobox.currentIndex()
            output_index = self.ui.output_length_combobox.currentIndex()
            conversion_factors = [
                units.planck_length,
                units.angstrom,
                units.picometer,
                units.nanometer,
                units.micrometer,
                units.millimeter,
                units.centimeter,
                units.decimeter,
                units.meter,
                units.kilometer,
                units.inch,
                units.foot,
                units.yard,
                units.mile,
                units.nautical_mile,
                units.astronomical_unit,
                units.lightyear,
            ]
            converted_value = units.convert_to(
                input_value * conversion_factors[input_index], conversion_factors[output_index]
            ).evalf()
            numeric_value = converted_value.args[0]  # Convert to numeric
            self.ui.output_line_unit.setText(str(numeric_value).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def convert_weight(self):
        try:
            input_value = Rational(self.ui.input_line_unit.text())
            input_index = self.ui.input_weight_combobox.currentIndex()
            output_index = self.ui.output_weight_combobox.currentIndex()
            conversion_factors = [
                units.amu,
                units.planck_mass,
                units.milli_mass_unit,
                units.dalton,
                units.microgram,
                units.milligram,
                units.gram,
                units.pound,
                units.kilogram,
                units.metric_ton,
            ]
            converted_value = units.convert_to(
                input_value * conversion_factors[input_index], conversion_factors[output_index]
            ).evalf()
            numeric_value = converted_value.args[0]
            self.ui.output_line_unit.setText(str(numeric_value).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def convert_time(self):
        try:
            input_value = Rational(self.ui.input_line_unit.text())
            input_index = self.ui.input_time_combobox.currentIndex()
            output_index = self.ui.output_time_combobox.currentIndex()
            conversion_factors = [
                units.planck_time,
                units.picosecond,
                units.nanosecond,
                units.microsecond,
                units.millisecond,
                units.second,
                units.minute,
                units.hour,
                units.day,
                units.full_moon_cycle,
                units.common_year,
                units.year,
                units.julian_year,
                units.draconic_year,
                units.tropical_year,
                units.sidereal_year,
                units.gaussian_year,
                units.anomalistic_year,
            ]
            converted_value = units.convert_to(
                input_value * conversion_factors[input_index], conversion_factors[output_index]
            ).evalf()
            numeric_value = converted_value.args[0]
            self.ui.output_line_unit.setText(str(numeric_value).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def convert_volume(self):
        try:
            input_value = Rational(self.ui.input_line_unit.text())
            input_index = self.ui.input_volume_combobox.currentIndex()
            output_index = self.ui.output_volume_combobox.currentIndex()
            conversion_factors = [
                units.planck_volume,
                units.milliliter,
                units.centiliter,
                units.deciliter,
                units.liter,
                units.quart,
            ]
            converted_value = units.convert_to(
                input_value * conversion_factors[input_index], conversion_factors[output_index]
            ).evalf()
            numeric_value = converted_value.args[0]
            self.ui.output_line_unit.setText(str(numeric_value).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def convert_information(self):
        try:
            input_value = Rational(self.ui.input_line_unit.text())
            input_index = self.ui.input_information_combobox.currentIndex()
            output_index = self.ui.output_information_combobox.currentIndex()
            conversion_factors = [
                units.bit,
                units.byte,
                units.kibibyte,
                units.mebibyte,
                units.gibibyte,
                units.tebibyte,
                units.pebibyte,
                units.exbibyte,
            ]
            converted_value = units.convert_to(
                input_value * conversion_factors[input_index], conversion_factors[output_index]
            ).evalf()
            numeric_value = converted_value.args[0]
            self.ui.output_line_unit.setText(str(numeric_value).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def convert_pressure(self):
        try:
            input_value = Rational(self.ui.input_line_unit.text())
            input_index = self.ui.input_pressure_combobox.currentIndex()
            output_index = self.ui.output_pressure_combobox.currentIndex()
            conversion_factors = [
                units.planck_pressure,
                units.atmosphere,
                units.bar,
                units.pascal,
                units.torr,
                units.psi,
            ]
            converted_value = units.convert_to(
                input_value * conversion_factors[input_index], conversion_factors[output_index]
            ).evalf()
            numeric_value = converted_value.args[0]
            self.ui.output_line_unit.setText(str(numeric_value).rstrip("0").rstrip("."))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # Change mode
    def switch_to_standard(self):
        self.ui.stackedwidget.setCurrentWidget(self.ui.standard_page)
        self.current_line_result = self.ui.line_result
        self.clear_journal()
        settings = QSettings("pyqulator")
        settings.setValue("mode", "standard")

    def switch_to_engineer(self):
        self.ui.stackedwidget.setCurrentWidget(self.ui.engineer_page)
        self.current_line_result = self.ui.line_result_2
        self.ui.line_result_2.setText(self.ui.line_result.text())
        self.clear_journal()
        settings = QSettings("pyqulator")
        settings.setValue("mode", "engineer")

    def switch_to_paper(self):
        self.ui.stackedwidget.setCurrentWidget(self.ui.paper_page)
        self.current_line_result = self.ui.line_result_3
        self.ui.line_result.setText(self.ui.line_result_2.text())
        self.clear_journal()
        self.clear_line_result()
        self.current_line_result.returnPressed.connect(self.calculate)
        settings = QSettings("pyqulator")
        settings.setValue("mode", "paper")

    def switch_to_unit_converter(self):
        self.ui.stackedwidget.setCurrentWidget(self.ui.unit_converter_page)
        self.current_line_result = self.ui.input_line_unit
        self.clear_line_result()
        settings = QSettings("pyqulator")
        settings.setValue("mode", "unit_converter")

    # Edit functions
    def line_result_copy(self):
        self.current_line_result.selectAll()
        self.current_line_result.copy()

    def line_result_cut(self):
        self.current_line_result.selectAll()
        self.current_line_result.cut()
        if self.ui.stackedwidget.currentIndex() in {0, 1}:
            self.clear_line_result()

    def line_result_paste(self):
        if self.ui.stackedwidget.currentIndex() in {0, 1}:
            self.current_line_result.clear()
        self.current_line_result.paste()
        text = self.current_line_result.text()
        filtered_text = ""
        for char in text:
            if self.ui.stackedwidget.currentIndex() in {0, 1, 2}:
                if char.isdigit() or char in ".+-*/()":
                    filtered_text += char
            else:
                if char.isdigit() or char in ".":
                    filtered_text += char
        self.current_line_result.setText(filtered_text)
        if self.current_line_result.text() == "":
            self.clear_line_result()

    def line_top(self):
        while self.ui.horizontalLayout.count():
            widget = self.ui.horizontalLayout.takeAt(0).widget()
            self.ui.horizontalLayout.removeWidget(widget)
        self.ui.verticalLayout.removeItem(self.ui.horizontalLayout)
        self.ui.verticalLayout.insertLayout(0, self.ui.horizontalLayout)
        self.ui.horizontalLayout.addWidget(self.ui.line_result_3)
        self.ui.horizontalLayout.addWidget(self.ui.btn_equal_3)
        settings = QSettings("pyqulator")
        settings.setValue("paper_mode_line", "top")

    def line_down(self):
        while self.ui.horizontalLayout.count():
            widget = self.ui.horizontalLayout.takeAt(0).widget()
            self.ui.horizontalLayout.removeWidget(widget)
        self.ui.verticalLayout.removeItem(self.ui.horizontalLayout)
        self.ui.verticalLayout.addLayout(self.ui.horizontalLayout)
        self.ui.horizontalLayout.addWidget(self.ui.line_result_3)
        self.ui.horizontalLayout.addWidget(self.ui.btn_equal_3)
        settings = QSettings("pyqulator")
        settings.setValue("paper_mode_line", "down")

    # Show windows with info about program and Qt
    def show_about_program(self):
        self.about_msg = QMessageBox()
        self.about_msg.setWindowTitle("About Pyqulator")
        msg_text = """
        <p>Pyqulator is a calculator written<br>
        in Python and PyQt 6.<br>
        Uses library: sympy.<br>
        Licensed under GNU GPL v3.<br>
        (c) limafresh, 2024</p>
        <p><a href="https://github.com/limafresh/pyqulator">Visit repository</a></p>
        """
        self.about_msg.setText(msg_text)
        icon = QIcon.fromTheme("accessories-calculator")
        self.about_msg.setIconPixmap(icon.pixmap(32, 32))
        self.about_msg.exec()

    def show_about_qt(self):
        QMessageBox.aboutQt(self)


def main():
    app = QApplication([])

    # Translate app
    locale = QLocale.system().name()
    translator = QTranslator()

    if translator.load(join(dirname(__file__), "locales", f"ui_{locale}.qm")):
        app.installTranslator(translator)

    application = Calculator()
    application.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
