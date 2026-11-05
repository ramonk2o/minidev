// Hidden acceptance tests for the list refactor: the behavior SPEC.md states
// (patch.sh) must survive it. The agent never sees this file.
import { test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { addNote, listNotes, reset } from '../src/notes.js';

beforeEach(() => reset());

test('notes are listed newest first', () => {
  addNote('one'); addNote('two'); addNote('three');
  assert.deepEqual(listNotes().map((n) => n.text), ['three', 'two', 'one']);
});

test('changing the returned list does not change the stored notes', () => {
  addNote('one'); addNote('two');
  const list = listNotes();
  list.push({ id: 99, text: 'intruder' });
  list.reverse();
  list.length = 0;
  assert.deepEqual(listNotes().map((n) => n.text), ['two', 'one']);
});

test('each call returns a new list', () => {
  addNote('one');
  assert.notEqual(listNotes(), listNotes());
});

test('ids are unique and follow the order notes were added', () => {
  addNote('one'); addNote('two'); addNote('three');
  assert.deepEqual(listNotes().map((n) => n.id), [3, 2, 1]);
});

test('addNote returns the note that listNotes shows', () => {
  const note = addNote('one');
  assert.equal(listNotes()[0].id, note.id);
  assert.equal(listNotes()[0].text, 'one');
});

test('reset empties the list', () => {
  addNote('one');
  reset();
  assert.deepEqual(listNotes(), []);
  addNote('again');
  assert.equal(listNotes()[0].id, 1);
});

test('notes with no text are still rejected', () => {
  assert.throws(() => addNote('   '));
  assert.throws(() => addNote(42));
  assert.deepEqual(listNotes(), []);
});

test('many notes keep their order', () => {
  for (let i = 0; i < 1000; i++) addNote(`n${i}`);
  const list = listNotes();
  assert.equal(list.length, 1000);
  assert.equal(list[0].text, 'n999');
  assert.equal(list[999].text, 'n0');
});
