// Hidden acceptance tests for the Search entry in patch.sh. Every test checks a
// rule the entry states; the agent never sees this file.
import { test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { addNote, listNotes, searchNotes, reset } from '../src/notes.js';

beforeEach(() => reset());
const texts = (notes) => notes.map((n) => n.text);

test('matching ignores case', () => {
  addNote('Buy MILK');
  assert.deepEqual(texts(searchNotes('milk')), ['Buy MILK']);
  assert.deepEqual(texts(searchNotes('MiLk')), ['Buy MILK']);
});

test('matching ignores accents, both ways', () => {
  addNote('Café com leite');
  addNote('cafe sem acucar');
  assert.equal(searchNotes('cafe').length, 2);
  assert.equal(searchNotes('CAFÉ').length, 2);
});

test('accents written as combining marks match too', () => {
  addNote('Café da manhã');
  assert.equal(searchNotes('café').length, 1);
  assert.equal(searchNotes('manhã').length, 1);
});

test('several words must all appear, in any order', () => {
  addNote('buy milk today');
  addNote('buy bread');
  assert.deepEqual(texts(searchNotes('today buy')), ['buy milk today']);
  assert.deepEqual(texts(searchNotes('buy milk')), ['buy milk today']);
});

test('extra spaces between words do not matter', () => {
  addNote('buy milk');
  assert.equal(searchNotes('  buy    milk ').length, 1);
});

test('words can be on different lines of the text', () => {
  addNote('buy\nmilk');
  assert.equal(searchNotes('buy milk').length, 1);
});

test('words match inside other words', () => {
  addNote('a milkshake');
  assert.equal(searchNotes('milk').length, 1);
});

test('an empty or blank query returns no notes', () => {
  addNote('anything');
  assert.deepEqual(searchNotes(''), []);
  assert.deepEqual(searchNotes('   '), []);
});

test('no match returns an empty list', () => {
  addNote('buy milk');
  assert.deepEqual(searchNotes('bread'), []);
});

test('results come in the same order as listNotes', () => {
  addNote('milk one');
  addNote('bread');
  addNote('milk two');
  addNote('milk three');
  const expected = listNotes().filter((n) => n.text.includes('milk')).map((n) => n.id);
  assert.deepEqual(searchNotes('milk').map((n) => n.id), expected);
});
