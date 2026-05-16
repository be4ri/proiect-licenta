import re
import pandas as pd
from .add_snp_command import AddSNPCommand
from .remove_snp_command import RemoveSNPCommand

class SNPCommandInvoker:
    def __init__(self, patients_repository):
        self.repository = patients_repository
        self._undo_stack = []
        self._redo_stack = []
        self.rsid_pattern = r"rs\d+"

    def _validate(self, rsid, excg):
        if not rsid.strip() and not excg.strip():
            raise ValueError("GRPM_RSID and EXCG46 cannot be empty. For EXCG46 type '--'.")
        if not re.fullmatch(self.rsid_pattern, rsid.strip()):
            raise ValueError("Invalid GRPM_RSID format. It should start with 'rs' followed by digits.")

    def execute_add(self, rsid, chr_val, pos, excg):
        self._validate(rsid, excg)
        command = AddSNPCommand(self.repository, rsid, chr_val, pos, excg)
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def execute_remove(self, rsid, chr_val, pos, excg):
        self._validate(rsid, excg)
        command = RemoveSNPCommand(self.repository, rsid, chr_val, pos, excg)
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self):
        if self._undo_stack:
            command = self._undo_stack.pop()
            command.undo()
            self._redo_stack.append(command)
            print("Action undone.")
        else:
            print("Nothing to undo.")

    def redo(self):
        if self._redo_stack:
            command = self._redo_stack.pop()
            command.execute()
            self._undo_stack.append(command)
            print("Action redone.")
        else:
            print("Nothing to redo.")