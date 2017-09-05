from pinotebetter.pinote import *
import markdown
import clipboard
import console
import ui
import dialogs
pb = Pinote('user','pass')


class ListingsView(object):
	def __init__(self, notes):
		self.notes = notes.get('notes')
		self.count = notes.get('count')
		self.selected_item = None
		import ui
		self.view = ui.TableView()
		self.view.name = '{} Notes'.format(notes.get('count'))
		ds = ui.ListDataSource(notes.get('notes'))
		self.view.right_button_items=[ui.ButtonItem(title='Add Note',action=self.add_note)]
		self.view.left_button_items=[ui.ButtonItem(image=ui.Image.named('iob:ios7_refresh_empty_32'),action=self.refresh)]
		ds.delete_enabled = False
		ds.action = self.row_selected
		self.view.data_source = ds
		self.view.delegate = ds
		self.view.frame = (0, 0, 500, 500)
		self.view.present('sheet')
	
	@ui.in_background
	def add_note(self, btn):
		title = dialogs.input_alert('Title')
		text = dialogs.text_dialog(title=title,autocorrection=True,done_button_title='Save')
		pb.add_note(title, text, 'qtey uenr')
	
	@ui.in_background
	def refresh(self, btn):
		self.view.close()
		self.__init__(pb.get_all_notes())
		
	@ui.in_background
	def row_selected(self, ds):
		note = self.notes[ds.selected_row]
		#print note
		console.show_activity('Getting note...')
		note_detail = pb.get_note_details(note.get('id'))
		console.hide_activity()
		note_view = NoteView(note_detail)

class NoteView(object):
	def __init__(self, note):
		self.note = note
		import ui
		self.view = ui.WebView()
		
		self.view.load_html(self.get_html())
		edit_btn = ui.ButtonItem(title='Edit',action=self.edit_action)
		delete_btn = ui.ButtonItem(title='Delete',action=self.delete_action,tint_color='#ff0000')
		self.view.right_button_items = [edit_btn, delete_btn]
		self.view.present()
		self.view.wait_modal()
		

	def edit_action(self, btn):
		edit_view = ui.load_view('pinote_edit')
		edit_view['title'].text = self.note.get('title')
		edit_view['note'].text = self.note.get('text')
		edit_view.present() 
		edit_view.wait_modal()
		
		self.note['text'] = edit_view['note'].text
		self.note['title'] = edit_view['title'].text
		pb.edit_note(self.note['title'], self.note['text'],self.note['id'] )
		
	def delete_action(self, btn):
		result = dialogs.alert('Are you sure you want to delete?', button1='Delete')
		if result:
			pb.delete_note(self.note['id'])
		self.view.close()
	
	def get_html(self):
		html_fmt='''
			<html style="font-size: 3em; word-wrap: break-word;">
			<h4>{title}</h4>
			<p>{body}</p>
			</html>
			'''
		md = markdown.Markdown(extensions=['markdown.extensions.nl2br'])
		title = self.note.get('title')
		body = md.convert(self.note.get('text'))
		return html_fmt.format(title=title, body=body)


notes =  pb.get_all_notes()
notes.get('notes').sort(key=lambda note: note.get('updated_at'), reverse=True)
v = ListingsView(notes)
#v.view.present('sheet')
#details = pb.get_note_details(note.get('id'))
#note_view = NoteView(note=details)
#note_view.present('sheet')
#print stuff
#dialogs.text_dialog(title=stuff.get('title'),text=stuff.get('text'),autocorrection=True)
html_fmt='''
<html style="font-size: 3em; word-wrap: break-word;">
<h4>{title}</h4>
<p>{body}</p>
</html>
'''
#print stuff
#md = markdown.Markdown(extensions=['markdown.extensions.nl2br'])
#htnl = md.convert(stuff.get('text'))
#htnl = foo.get_note_html(note.get('id'))


#TODO:
#	tags,
#	preview markdown
#	save button
#	delete ui
# fix pinote parser - html