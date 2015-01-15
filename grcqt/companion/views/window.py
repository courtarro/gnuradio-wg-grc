import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from .. import base


class MainWindow(QtWidgets.QMainWindow, base.View):
    """
    GRC.Views.MainWindow
    ---------------------------
    Class that handles the main view definition for the main grc window
    """

    def __init__(self):
        super().__init__()  # REQUIRED for both QMainWindow and base.View
        self.log.debug("__init__")

        # Main window properties
        self.log.debug("Setting window properties")
        self.setWindowTitle(_('window-title'))
        self.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks |
                            QtWidgets.QMainWindow.AllowTabbedDocks |
                            QtWidgets.QMainWindow.AnimatedDocks)

        # Setup the window icon
        self.log.debug("Setting window icon ({0})".format(self.gp.path.ICON))
        icon = QtGui.QIcon(self.gp.path.ICON)
        self.setWindowIcon(icon)

        self.log.debug("Setting window size")
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        self.resize(screen.width() * 0.40, screen.height())

        self.menuBar().setNativeMenuBar(self.gp.window.NATIVE_MENUBAR)

        # TODO: Not sure about document mode
        #self.setDocumentMode(True)

        # Generate the rest of the window
        self.menus = {}
        self.toolbars = {}
        self.createMenus()
        self.createToolbars()
        self.createStatusBar()

        #actions['Quit.triggered.connect(self.close)
        #actions['Report.triggered.connect(self.reportDock.show)
        #QtCore.QMetaObject.connectSlotsByName(self)

    def createActions(self, actions):
        """
        Defines all actions for this view.
        Controller uses the QT to connect actions to handlers
        """
        self.log.debug("Creating actions")
        Action = QtWidgets.QAction
        Icons = QtGui.QIcon.fromTheme
        Keys = QtGui.QKeySequence

        # File Actions
        actions['new'] = Action(Icons("document-new"), _("new"), self,
                                shortcut=Keys.New, statusTip=_("new-tooltip"))

        actions['open'] = Action(Icons("document-open"), _("open"), self,
                                 shortcut=Keys.Open, statusTip=_("open-tooltip"))

        actions['close'] = Action(Icons("window-close"), _("close"), self,
                                  shortcut=Keys.Close, statusTip=_("close-tooltip"))

        actions['close_all'] = Action(Icons("window-close"), _("close_all"), self,
                                      shortcut=Keys.Close, statusTip=_("close_all-tooltip"))

        actions['save'] = Action(Icons("document-save"), _("save"), self,
                                 shortcut=Keys.Save, statusTip=_("save-tooltip"))

        actions['save_as'] = Action(Icons("document-save-as"), _("save_as"), self,
                                    shortcut=Keys.SaveAs, statusTip=_("save_as-tooltip"))

        actions['print'] = Action(Icons('document-print'), _("print"), self,
                                  shortcut=Keys.Print, statusTip=_("print-tooltip"))

        actions['screen_capture'] = Action(Icons('camera-photo'), _("screen_capture"), self,
                                           statusTip=_("screen_capture-tooltip"))

        actions['exit'] = Action(Icons("application-exit"), _("exit"), self,
                                 shortcut=Keys.Quit, statusTip=_("exit-tooltip"))

        # Edit Actions
        actions['undo'] = Action(Icons('edit-undo'), _("undo"), self,
                                 shortcut=Keys.Undo, statusTip=_("undo-tooltip"))

        actions['redo'] = Action(Icons('edit-redo'), _("redo"), self,
                                 shortcut=Keys.Redo, statusTip=_("redo-tooltip"))

        actions['cut'] = Action(Icons('edit-cut'), _("cut"), self,
                                shortcut=Keys.Cut, statusTip=_("cut-tooltip"))

        actions['copy'] = Action(Icons('edit-copy'), _("copy"), self,
                                 shortcut=Keys.Copy, statusTip=_("copy-tooltip"))

        actions['paste'] = Action(Icons('edit-paste'), _("paste"), self,
                                  shortcut=Keys.Paste, statusTip=_("paste-tooltip"))

        actions['delete'] = Action(Icons('edit-delete'), _("delete"), self,
                                   shortcut=Keys.Delete, statusTip=_("delete-tooltip"))

        actions['rotate_ccw'] = Action(Icons('object-rotate-left'), _("rotate_ccw"), self,
                                       shortcut=Keys.MoveToPreviousChar,
                                       statusTip=_("rotate_ccw-tooltip"))

        actions['rotate_cw'] = Action(Icons('object-rotate-right'), _("rotate_cw"), self,
                                      shortcut=Keys.MoveToNextChar,
                                      statusTip=_("rotate_cw-tooltip"))

        # View Actions
        actions['errors'] = Action(Icons('dialog-error'), _("errors"), self, shortcut='E',
                                   statusTip=_("errors-tooltip"))

        actions['find'] = Action(Icons('edit-find'), _("find"), self,
                                 shortcut=Keys.Find,
                                 statusTip=_("find-tooltip"))

        # Help Actions
        actions['about'] = Action(Icons('help-about'), _("about"), self,
                                  statusTip=_("about-tooltip"))

        actions['about_qt'] = Action(Icons('help-about'), _("about-qt"), self,
                                     statusTip=_("about-tooltip"))

        actions['generate'] = Action(Icons('system-run'), _("process-generate"), self,
                                     shortcut='F5', statusTip=_("process-generate-tooltip"))

        actions['execute'] = Action(Icons('media-playback-start'), _("process-execute"),
                                    self, shortcut='F6',
                                    statusTip=_("process-execute-tooltip"))

        actions['kill'] = Action(Icons('process-stop'), _("process-kill"), self,
                                 shortcut='F7', statusTip=_("process-kill-tooltip"))

        actions['help'] = Action(Icons('help-browser'), _("help"), self,
                                 shortcut=Keys.HelpContents, statusTip=_("help-tooltip"))

        actions['types'] = Action("Types", self)

        actions['library'] = Action("Library", self, shortcut="Ctrl+L",
                                    statusTip=_("block-library-tooltip"), checkable=True)

        actions['report'] = Action("Reports", self, checkable=True)
        actions['enable'] = Action("Enable", self)
        actions['disable'] = Action("Disable", self)

        actions['properties'] = Action(Icons('document-properties'), _("flowgraph-properties"),
                                       self, statusTip=_("flowgraph-properties-tooltip"))

        actions['preferences'] = Action(Icons('preferences-system'), _("preferences"), self,
                                        statusTip=_("preferences-tooltip"))

        # Disable some actions, by default
        actions['save'].setEnabled(False)
        actions['undo'].setEnabled(False)
        actions['redo'].setEnabled(False)
        actions['cut'].setEnabled(False)
        actions['copy'].setEnabled(False)
        actions['paste'].setEnabled(False)
        actions['delete'].setEnabled(False)
        actions['rotate_ccw'].setEnabled(False)
        actions['rotate_cw'].setEnabled(False)
        actions['errors'].setEnabled(False)

    def createMenus(self):
        """ Setup the main menubar for the application """

        self.log.debug("Creating menus")
        actions = self.actions
        menus = self.menus

        # Global menu options
        self.menuBar().setNativeMenuBar(True)

        # Setup the file menu
        file = self.menuBar().addMenu("&File")
        file.addAction(actions['new'])
        file.addAction(actions['open'])
        file.addAction(actions['close'])
        file.addAction(actions['close_all'])
        file.addSeparator()
        file.addAction(actions['save'])
        file.addAction(actions['save_as'])
        file.addSeparator()
        file.addAction(actions['screen_capture'])
        file.addAction(actions['print'])
        file.addSeparator()
        file.addAction(actions['exit'])
        menus['file'] = file

        # Setup the edit menu
        edit = self.menuBar().addMenu("&Edit")
        edit.addAction(actions['undo'])
        edit.addAction(actions['redo'])
        edit.addSeparator()
        edit.addAction(actions['cut'])
        edit.addAction(actions['copy'])
        edit.addAction(actions['paste'])
        edit.addAction(actions['delete'])
        edit.addSeparator()
        edit.addAction(actions['rotate_ccw'])
        edit.addAction(actions['rotate_cw'])
        edit.addSeparator()
        edit.addAction(actions['enable'])
        edit.addAction(actions['disable'])
        edit.addAction(actions['properties'])
        menus['edit'] = edit

        # Setup the view menu
        view = self.menuBar().addMenu("&View")
        view.addAction(actions['errors'])
        view.addAction(actions['find'])
        view.addSeparator()
        view.addAction(actions['library'])
        view.addAction(actions['report'])
        menus['view'] = view

        # Setup the build menu
        build = self.menuBar().addMenu("&Build")
        build.addAction(actions['generate'])
        build.addAction(actions['execute'])
        build.addAction(actions['kill'])
        menus['build'] = build

        # Setup the help menu
        help = self.menuBar().addMenu("&Help")
        help.addAction(actions['help'])
        help.addAction(actions['types'])
        help.addSeparator()
        help.addAction(actions['about'])
        help.addAction(actions['about_qt'])
        menus['help'] = help

    def createToolbars(self):
        self.log.debug("Creating toolbars")
        toolbars = self.toolbars
        actions = self.actions

        # Main toolbar
        file = self.addToolBar("file")
        file.addAction(actions['new'])
        file.addAction(actions['open'])
        file.addAction(actions['save'])
        file.addAction(actions['close'])
        file.addAction(actions['print'])
        toolbars['file'] = file

        # Edit toolbar
        edit = self.addToolBar("edit")
        edit.addAction(actions['cut'])
        edit.addAction(actions['copy'])
        edit.addAction(actions['paste'])
        edit.addAction(actions['delete'])
        edit.addSeparator()
        edit.addAction(actions['rotate_ccw'])
        edit.addAction(actions['rotate_cw'])
        toolbars['edit'] = edit

        # Run Toolbar
        run = self.addToolBar("run")
        run.addAction(actions['generate'])
        run.addAction(actions['execute'])
        run.addAction(actions['kill'])
        toolbars['run'] = run

    def createStatusBar(self):
        self.log.debug("Creating status bar")
        self.statusBar().showMessage(_("ready-message"))

    def new_tab(self, flowgraph):
        self.setCentralWidget(flowgraph)

    def open(self):
        Open = QtWidgets.QFileDialog.getOpenFileName
        filename, filtr = Open(self, self.actions['open'].statusTip(),
                               filter='Flow Graph Files (*.grc);;All files (*.*)')
        return filename

