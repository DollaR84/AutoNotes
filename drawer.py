"""
Graphical form for AutoNotes.

Created on 25.05.2017

@author: Ruslan Dolovanyuk

"""

from commands import Commands

import wx
import wx.adv


class Drawer:
    """Graphical form for auto notes."""

    def __init__(self, conn, cursor):
        """Initilizing drawer form."""
        self.app = wx.App()
        self.wnd = AutoNotesFrame(conn, cursor)
        self.wnd.Show(True)
        self.app.SetTopWindow(self.wnd)

    def mainloop(self):
        """Graphical main loop running."""
        self.app.MainLoop()


class AutoNotesFrame(wx.Frame):
    """Create user interface."""

    def __init__(self, conn, cursor):
        """Initializing interface."""
        super().__init__(None, wx.ID_ANY, 'База ремонтных работ')
        self.command = Commands(self, conn, cursor)
        self.month = (
                      'января', 'февраля', 'марта',
                      'апреля', 'мая', 'июня',
                      'июля', 'августа', 'сентября',
                      'октября', 'ноября', 'декабря',
                     )

        self.panel = wx.Panel(self, wx.ID_ANY)
        sizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel.Add(self.panel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer_panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        bottom_sizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.left_but_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.right_but_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.create_left_panel()
        self.create_right_panel()
        self.create_buttons_panel()

        top_sizer.Add(self.left_sizer, 1, wx.EXPAND | wx.ALL)
        top_sizer.Add(self.right_sizer, 1, wx.EXPAND | wx.ALL)
        bottom_sizer.Add(self.left_but_sizer, 0, wx.ALIGN_LEFT)
        bottom_sizer.Add(self.right_but_sizer, 0, wx.ALIGN_RIGHT)
        sizer.Add(top_sizer, 1, wx.EXPAND | wx.ALL)
        sizer.Add(bottom_sizer, 0, wx.EXPAND | wx.ALL)
        self.panel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, getattr(self.command, 'close_window'))

        self.command.set_window()
        self.update()
        self.category.SetSelection(0)

    def create_left_panel(self):
        """Create all components on left panel."""
        self.command.update()
        box_category = wx.StaticBox(self.panel, wx.ID_ANY, 'Категория')
        category_box_sizer = wx.StaticBoxSizer(box_category, wx.VERTICAL)
        category_sizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)

        self.category = wx.Choice(box_category, wx.ID_ANY,
                                  choices=self.command.category_names)
        add_category_but = wx.Button(box_category, wx.ID_ANY, 'Создать')
        self.listbox = wx.ListBox(self.panel, wx.ID_ANY,
                                  choices=self.command.titles,
                                  style=wx.LB_SINGLE | wx.LB_HSCROLL)

        category_sizer.Add(self.category, 0, wx.EXPAND | wx.ALL)
        category_sizer.Add(add_category_but, 0, wx.ALIGN_RIGHT)
        category_box_sizer.Add(category_sizer, 0, wx.EXPAND | wx.ALL)
        self.left_sizer.Add(category_box_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.left_sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 5)

        self.Bind(wx.EVT_CHOICE, getattr(self.command, 'select_category'))
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'add_category'),
                  add_category_but)
        self.Bind(wx.EVT_LISTBOX, getattr(self.command, 'selection'))

    def create_right_panel(self):
        """Create all components on right panel."""
        box_title = wx.StaticBox(self.panel, wx.ID_ANY, 'Заголовок')
        box_date = wx.StaticBox(self.panel, wx.ID_ANY, 'Дата')
        box_company = wx.StaticBox(self.panel, wx.ID_ANY, 'Производитель')
        box_model = wx.StaticBox(self.panel, wx.ID_ANY, 'Модель')
        box_serial = wx.StaticBox(self.panel, wx.ID_ANY, 'Серийный номер')
        box_data = wx.StaticBox(self.panel, wx.ID_ANY, 'Описание')

        self.title = wx.TextCtrl(box_title, wx.ID_ANY)
        self.date_str = wx.StaticText(box_date, wx.ID_ANY,
                                      style=wx.EXPAND | wx.ALIGN_LEFT)
        self.date = wx.adv.CalendarCtrl(box_date, wx.ID_ANY,
                                        wx.DateTime.Today(),
                                        style=wx.adv.CAL_MONDAY_FIRST |
                                        wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION)
        self.company = wx.TextCtrl(box_company, wx.ID_ANY)
        self.model = wx.TextCtrl(box_model, wx.ID_ANY)
        self.serial = wx.TextCtrl(box_serial, wx.ID_ANY)
        self.data = wx.TextCtrl(box_data, wx.ID_ANY,
                                style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)

        sizer_title = wx.StaticBoxSizer(box_title, wx.VERTICAL)
        sizer_date = wx.StaticBoxSizer(box_date, wx.VERTICAL)
        sizer_company = wx.StaticBoxSizer(box_company, wx.VERTICAL)
        sizer_model = wx.StaticBoxSizer(box_model, wx.VERTICAL)
        sizer_serial = wx.StaticBoxSizer(box_serial, wx.VERTICAL)
        sizer_data = wx.StaticBoxSizer(box_data, wx.VERTICAL)

        sizer_title.Add(self.title, 0, wx.EXPAND | wx.ALL, 5)
        sizer_date.Add(self.date_str, 0, wx.ALIGN_LEFT, 5)
        sizer_date.Add(self.date, 0, wx.EXPAND | wx.ALL, 5)
        sizer_company.Add(self.company, 0, wx.EXPAND | wx.ALL, 5)
        sizer_model.Add(self.model, 0, wx.EXPAND | wx.ALL, 5)
        sizer_serial.Add(self.serial, 0, wx.EXPAND | wx.ALL, 5)
        sizer_data.Add(self.data, 1, wx.EXPAND | wx.ALL, 5)

        self.right_sizer.Add(sizer_title, 0, wx.EXPAND | wx.ALL, 5)
        self.right_sizer.Add(sizer_date, 0, wx.EXPAND | wx.ALL, 5)
        self.right_sizer.Add(sizer_company, 0, wx.EXPAND | wx.ALL, 5)
        self.right_sizer.Add(sizer_model, 0, wx.EXPAND | wx.ALL, 5)
        self.right_sizer.Add(sizer_serial, 0, wx.EXPAND | wx.ALL, 5)
        self.right_sizer.Add(sizer_data, 1, wx.EXPAND | wx.ALL, 5)

        self.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED,
                  getattr(self.command, 'select_date'), self.date)

    def create_buttons_panel(self):
        """Create all buttons on bottom panel."""
        self.add = wx.Button(self.panel, wx.ID_ANY, 'Добавить')
        self.change = wx.Button(self.panel, wx.ID_ANY, 'Изменить')
        self.delete = wx.Button(self.panel, wx.ID_ANY, 'Удалить')
        self.about = wx.Button(self.panel, wx.ID_ANY, 'О программе...')
        self.close = wx.Button(self.panel, wx.ID_ANY, 'Выход')

        self.left_but_sizer.Add(self.add, 0, wx.ALIGN_LEFT)
        self.left_but_sizer.Add(self.change, 0, wx.ALIGN_LEFT)
        self.left_but_sizer.Add(self.delete, 0, wx.ALIGN_LEFT)
        self.right_but_sizer.Add(self.about, 0, wx.ALIGN_RIGHT)
        self.right_but_sizer.Add(self.close, 0, wx.ALIGN_RIGHT)

        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'add'), self.add)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'change'), self.change)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'delete'), self.delete)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'about'), self.about)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'close'), self.close)

    def update(self):
        """Redraw components."""
        self.category.Set(self.command.category_names)
        self.listbox.Set(self.command.titles)
        self.empty()

    def empty(self):
        """Clear components."""
        self.title.SetValue('')
        self.set_date_str(wx.DateTime.Today().Format('%d.%m.%Y'))
        self.date.SetDate(wx.DateTime.Today())
        self.company.SetValue('')
        self.model.SetValue('')
        self.serial.SetValue('')
        self.data.SetValue('')
        self.change.Disable()
        self.delete.Disable()
        self.Layout()

    def set_date(self, index):
        """Set date in calendar."""
        self.set_date_str(self.command.notes[index][2])
        date = self.command.notes[index][2].split('.')
        self.date.SetDate(wx.DateTime(int(date[0]), int(date[1])-1,
                                      int(date[2])))

    def set_date_str(self, date_str):
        """Set date in string label."""
        date = date_str.split('.')
        date_new = '%s %s %s' % (date[0], self.month[int(date[1])-1], date[2])
        self.date_str.SetLabel(date_new)
