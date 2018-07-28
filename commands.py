"""
Commands for graphical interface.

Created on 25.05.2017

@author: Ruslan Dolovanyuk

"""

from dialogs import About
from dialogs import Message
from dialogs import RetCode
from dialogs import TextEntryDialog


class Commands:
    """Helper class, contains command for bind events, menu and buttons."""

    def __init__(self, drawer, conn, cursor):
        """Initilizing commands class."""
        self.drawer = drawer
        self.conn = conn
        self.cursor = cursor
        self.message = Message(self.drawer)

    def update(self):
        """Update all data from database."""
        script = 'SELECT * FROM category'
        self.categories = self.cursor.execute(script).fetchall()
        script = 'SELECT * FROM main'
        self.notes = self.cursor.execute(script).fetchall()

        self.category_names = [category[1] for category in self.categories]
        self.titles = [note[1] for note in self.notes]

        self.category_names.insert(0, 'Все')
        self.titles.insert(0, '{ Пусто }')

    def get_all(self):
        """Get information from all components."""
        title = self.drawer.title.GetValue()
        date = self.drawer.date.GetDate().Format('%d.%m.%Y')
        company = self.drawer.company.GetValue()
        model = self.drawer.model.GetValue()
        serial = self.drawer.serial.GetValue()
        data = self.drawer.data.GetValue()
        return (title, date, company, model, serial, data)

    def index_l2g(self, index):
        """Converted local index category in global index all notes."""
        category_index = self.drawer.category.GetSelection()
        if 0 == category_index:
            return self.notes[index-1][0]

        sub_notes = []
        for note in self.notes:
            if note[7] == category_index:
                sub_notes.append(note)

        return sub_notes[index-1][0]

    def add_category(self, event):
        """Add new category in database."""
        dlg = TextEntryDialog(self.drawer, 'Добавление категории',
                              'Введите название новой категории:')
        if RetCode.OK == dlg.ShowModal():
            name = dlg.GetValue()
            index = 1
            if self.categories:
                index = self.categories[-1][0]+1
            if name in self.category_names:
                self.message.exclamation('Внимание!',
                                         'Данная категория уже существует')
            else:
                script = '''INSERT INTO category (id, name) VALUES (%d, "%s")
                         ''' % (index, name)
                self.cursor.execute(script)
                self.conn.commit()
                self.update()
                self.drawer.update()
                self.drawer.category.SetSelection(0)
                self.select_category(event)
        dlg.Destroy()

    def select_category(self, event):
        """Change selected category."""
        category_index = self.drawer.category.GetSelection()
        if 0 == category_index:
            self.titles = [note[1] for note in self.notes]
        else:
            self.titles = []
            for note in self.notes:
                if note[7] == category_index:
                    self.titles.append(note[1])

        self.titles.insert(0, '{ Пусто }')
        self.drawer.listbox.Set(self.titles)
        self.drawer.empty()

    def selection(self, event):
        """Change selection listbox."""
        old_index = self.drawer.listbox.GetSelection()
        index = self.index_l2g(old_index)-1
        if 0 == old_index:
            self.drawer.empty()
        else:
            self.drawer.title.SetValue(self.notes[index][1])
            self.drawer.set_date(index)
            self.drawer.company.SetValue(self.notes[index][3])
            self.drawer.model.SetValue(self.notes[index][4])
            self.drawer.serial.SetValue(self.notes[index][5])
            self.drawer.data.SetValue(self.notes[index][6])
            self.drawer.change.Enable()
            self.drawer.delete.Enable()
            self.drawer.Layout()

    def select_date(self, event):
        """Changed select date in calendar."""
        date = self.drawer.date.GetDate().Format('%d.%m.%Y')
        self.drawer.set_date_str(date)
        self.drawer.Layout()

    def add(self, event):
        """Add note in database."""
        category_index = self.drawer.category.GetSelection()
        note = self.get_all()
        if '' != note[0]:
            id_db = 1
            script = 'SELECT * FROM main ORDER BY id DESC LIMIT 1'
            last_note = self.cursor.execute(script).fetchall()
            if last_note:
                id_db = last_note[0][0]+1
            script = '''INSERT INTO main (id, title, date, company, model, serial, data, category)
                        VALUES (%d, "%s", "%s", "%s", "%s", "%s", "%s", %d)
                     ''' % (id_db, note[0], note[1], note[2], note[3],
                            note[4], note[5], category_index)
            self.cursor.execute(script)
            self.conn.commit()
            self.update()
            self.drawer.update()
            self.drawer.category.SetSelection(category_index)
            self.select_category(event)
        else:
            self.message.exclamation('Внимание!',
                                     'Поле "Заголовок" необходимо заполнить')

    def change(self, event):
        """Change note in database."""
        old_index = self.drawer.listbox.GetSelection()
        index = self.index_l2g(old_index)
        category_index = self.drawer.category.GetSelection()
        note = self.get_all()
        script = '''UPDATE main SET title="%s", date="%s",
                                    company="%s", model="%s", serial="%s",
                                    data="%s" WHERE id=%d
                 ''' % (note[0], note[1], note[2],
                        note[3], note[4], note[5], index)
        self.cursor.execute(script)
        self.conn.commit()
        self.update()
        self.drawer.update()
        self.drawer.category.SetSelection(category_index)
        self.select_category(event)
        self.drawer.listbox.SetSelection(old_index)
        self.selection(event)

    def delete(self, event):
        """Delete note in database."""
        index = self.index_l2g(self.drawer.listbox.GetSelection())
        category_index = self.drawer.category.GetSelection()
        if self.notes:
            find = False
            for note in self.notes:
                if index == note[0]:
                    script = 'DELETE FROM main WHERE id=%d' % note[0]
                    self.cursor.execute(script)
                    find = True
                    continue

                if find:
                    script = '''UPDATE main SET id=%d WHERE id=%d
                             ''' % (note[0]-1, note[0])
                    self.cursor.execute(script)
            self.conn.commit()
            self.update()
            self.drawer.update()
            self.drawer.category.SetSelection(category_index)
            self.select_category(event)

    def set_window(self):
        """Set size and position window from saving data."""
        script = 'SELECT * FROM window'
        data = self.cursor.execute(script).fetchone()

        self.drawer.SetPosition((data[1], data[2]))
        self.drawer.SetSize((data[3], data[4]))
        self.drawer.Layout()

    def about(self, event):
        """Run about dialog."""
        About(self.drawer, 'О программе...', 'База Ремонтных Работ', '1.0',
              'Руслан Долованюк').ShowModal()

    def close(self, event):
        """Close event for button close."""
        self.drawer.Close(True)

    def close_window(self, event):
        """Close window event."""
        pos = self.drawer.GetScreenPosition()
        size = self.drawer.GetSize()

        script = 'UPDATE window SET px=%d, py=%d WHERE id=1' % tuple(pos)
        self.cursor.execute(script)
        script = 'UPDATE window SET sx=%d, sy=%d WHERE id=1' % tuple(size)
        self.cursor.execute(script)
        self.conn.commit()

        self.drawer.Destroy()
