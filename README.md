## Pinote Better
<hr>

Pinote Better enables programmatic access to Pinboard Notes. This is very much a workaround, as currently there isn't an official API for Notes. (Hence the requirement of username/password instead of API token.)


### Usage
```python
>>> from pinote import Pinote
>>> pn = Pinote('your_username', 'your_password')
```

Once you've done this, you can now use the `pn` object to access Notes. Here are some examples:

##### Get All Notes
```python
>>> pn.get_all_notes()
{
    u'count': 1,
    u'notes': [{
        u'hash': u'47cd8b82d59beby67',
        u'title': u'my cool note',
        u'created_at': u'2017-03-03 21:00:41',
        u'updated_at': u'2017-03-03 21:00:41',
        u'length': u'293',
        u'id': u'1ebd124daf1y82nd0'
    }]
}
```

##### Get a Full Note
```python
>>> pn.get_note_html('1ebd124daf1y82nd0')
<blockquote class="note">
    <p><b>my cool note</b></p>
    <p><em>note body</em> more note body</p>
</blockquote>
```

##### Add a Note
```python
>>> pn.add_note('my cool note', '*note body* more note body', 'space separated tags', True, False)
```

##### Edit a Note
```python
>>> pn.edit_note('my title', 'my note body', '1ebd124daf1y82nd0', False)
```

##### Delete a Note
```python
>>> pn.delete_note('1ebd124daf1y82nd0')
```

<hr>

#### TODO:

- [x] Add exception handling
- [ ] Add a Pythonista GUI (i.e. iOS app)


### License
MIT License. See [License](<LICENSE>) for details.
