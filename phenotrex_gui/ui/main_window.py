"""Main module."""
from pathlib import Path

import pandas as pd
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from phenotrex_gui.prediction.prediction import predict
from phenotrex_gui.ui.table import TableWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(Path(__file__).parent/'main_window.ui', self)
        self.setWindowTitle('Phenotrex (GUI)')
        self.setContentsMargins(5, 5, 5, 5)
        self.select_files_button.clicked.connect(self.get_files)
        self.select_models_button.clicked.connect(self.get_models)
        self.calculate_button.clicked.connect(self.calculate)
        self.input_files_display.setReadOnly(True)
        self.input_models_display.setReadOnly(True)
        self.input_files_display.setVisible(False)
        self.input_files_display_label.setVisible(False)
        self.input_models_display.setVisible(False)
        self.input_models_display_label.setVisible(False)
        self.console_log.setReadOnly(True)
        self.console_log_label.setVisible(False)
        self.console_log.setVisible(False)
        self._input_files = []
        self._input_models = []

    def __del__(self):
        self.table.destroy()

    def get_files(self):
        home_dir = str(Path.home())
        fnames = QFileDialog.getOpenFileNames(
            self,
            'Open file',
            home_dir,
            filter='Genome files (*.fna *.faa *.fna.gz *.faa.gz *.fasta *.fasta.gz *.genotype)'
        )[0]
        self._input_files = fnames
        self.input_files_display.clear()
        self.input_files_display.textCursor().insertText('\n'.join(
            Path(x).name for x in self._input_files
        ))
        self.input_files_display.setVisible(True)
        self.input_files_display_label.setVisible(True)

    def get_models(self):
        home_dir = str(Path.home())
        fnames = QFileDialog.getOpenFileNames(self, 'Open file', home_dir, filter='*.pkl')[0]
        self._input_models = fnames
        self.input_models_display.clear()
        self.input_models_display.textCursor().insertText('\n'.join(
            Path(x).name for x in self._input_models
        ))
        self.input_models_display.setVisible(True)
        self.input_models_display_label.setVisible(True)

    def write_log_output(self, s: str):
        self.console_log_label.setVisible(True)
        self.console_log.setVisible(True)
        self.console_log.clear()
        self.console_log.textCursor().insertText(s)
        self.console_log.textCursor().insertText('\n')

    def set_table_data(self, df: pd.DataFrame):
        self.table = TableWindow(df)
        self.table.show()

    def calculate(self):
        do_calc = True
        if not len(self._input_files):
            self.write_log_output('No files selected!')
            do_calc = False
        if not len(self._input_models):
            self.write_log_output('No Phenotrex models selected!')
            do_calc = False

        if do_calc:
            all_df = []
            n_tot = len(self._input_files) * len(self._input_models)
            n_curr = 0
            for i, m in enumerate(self._input_models):
                for j, f in enumerate(self._input_files):
                    n_curr += 1
                    df = predict(input_files=[f], classifier=m, verb=False)
                    self.progressBar.setValue(int((n_curr / n_tot) * 100))
                    all_df.append(df)
            final_df = pd.concat(all_df, axis=0).reset_index(drop=True)
            self.set_table_data(final_df)
