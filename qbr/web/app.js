'use strict';

const $ = id => document.getElementById(id);
const token = document.querySelector('meta[name="stockfisher-token"]').content;
const state = {
  result: null,
  context: null,
  selected: new Set(),
  busy: false,
  connected: false,
  sourceRequest: 0
};
const count = value => Number(value || 0).toLocaleString();
// What each Anki state means. Only a studied card is coverage you have learned; the rest say how far from it you are.
const ankiStates = {
  'studied': ['studied', '● Studied', 'A note named this has a card you have reviewed.'],
  'card': ['card', '◐ Card, not studied', 'A note named this has an active card you have not reviewed yet.'],
  'suspended': ['suspended', '● Suspended', 'A note is named this, but all its cards are suspended.'],
  'on-note': ['on-note', '◑ On its note', "Written on the answer's own note (back information), not a card of its own."],
  'on-note-suspended': ['suspended', '◑ On its note (suspended)', "Written on the answer's own note, whose cards are all suspended."],
  'text': ['elsewhere', '○ Only in another note', "Appears in some other note's text. Not coverage."],
  '': ['missing', '○ Missing', 'Nowhere in your collection.']
};
const dotMap = {
  1: 'MS', 2: 'easy HS', 3: 'HS', 4: 'hard HS', 5: 'HS nats',
  6: '●', 7: '●●', 8: '●●●', 9: '●●●●', 10: 'open'
};
const dotDifficulty = diff => {
  const d = Math.round(Number(diff));
  return d ? (dotMap[d] || String(d)) : '';
};
const positionLabel = clue => {
  if (clue.where === 'bonus') return 'Bonus only';
  if (clue.where === 'giveaway') return 'Giveaway';
  if ((clue.power || 0) >= 0.5) return 'In power';
  return clue.where ? clue.where.charAt(0).toUpperCase() + clue.where.slice(1) : '';
};
const stripTag = answer => (answer || '').replace(/\s*<[^<>]{0,60}>\s*$/, '');

function node(tag, className = '', text = '') {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== '') element.textContent = String(text);
  return element;
}
function clear(element) {
  element.replaceChildren();
}
function announce(message) {
  $('live-status').textContent = message;
}
function showError(message) {
  $('error').textContent = message;
  $('error').hidden = !message;
}

async function api(action, data) {
  const options = { headers: { 'X-StockFisher-Token': token } };
  if (data !== undefined) {
    options.method = 'POST';
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(data);
  }
  let response;
  try {
    response = await fetch('/api/' + action, options);
  } catch (_) {
    throw new Error('StockFisher is not connected. Reopen the app with your shortcut.');
  }
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || 'The request could not be completed.');
  return result;
}

function inputs() {
  return {
    query: $('query').value.trim(),
    category: $('category').value.trim(),
    difficulty: $('difficulty').value.trim(),
    year: $('year').value.trim(),
    ranking: $('ranking').value,
    limit: Number($('limit').value),
    exclude: $('exclude').value.trim(),
    exact: $('exact').checked,
    anki: $('anki').checked
  };
}

function dirty() {
  return state.context && JSON.stringify(inputs()) !== JSON.stringify(state.context);
}

function updateSelection() {
  const total = state.result?.things?.length || 0;
  $('selection-count').textContent = state.selected.size ? (state.selected.size + ' selected') : 'Select clues';
  $('select-all').checked = total > 0 && state.selected.size === total;
  $('select-all').indeterminate = state.selected.size > 0 && state.selected.size < total;
  $('export-button').disabled = !state.selected.size || dirty() || state.busy;
}

function inputsChanged() {
  $('dirty-notice').hidden = !dirty();
  updateSelection();
}

function busy(value) {
  state.busy = value;
  $('search-controls').disabled = value || !state.connected;
  $('loading').hidden = !value;
  $('results').setAttribute('aria-busy', String(value));
  updateSelection();
}

async function search() {
  if (state.busy || !state.connected) return;
  const context = inputs();
  if (!context.query) {
    $('query').focus();
    return;
  }
  closeMenus();
  closeSource();
  showError('');
  state.result = null;
  state.context = null;
  state.selected.clear();
  $('result-content').hidden = true;
  $('dirty-notice').hidden = true;
  busy(true);
  announce('Searching your question index.');
  try {
    state.result = await api('profile', context);
    state.context = context;
    renderResults();
    announce('Profile ready for ' + context.query + '.');
  } catch (error) {
    showError(error.message);
    announce(error.message);
  } finally {
    busy(false);
    inputsChanged();
  }
}

function clueRow(clue, index) {
  const row = node('article', 'result-row');
  const checkbox = node('input', 'row-select');
  checkbox.type = 'checkbox';
  checkbox.dataset.index = index;
  checkbox.setAttribute('aria-label', 'Select ' + clue.thing);
  checkbox.addEventListener('change', () => {
    if (checkbox.checked) state.selected.add(index); else state.selected.delete(index);
    updateSelection();
  });
  const body = node('div', 'row-body');
  const top = node('div', 'row-top');
  const titleEl = node('h3', 'row-title');
  if (clue.kind === 'title') titleEl.append(node('em', '', clue.thing)); else titleEl.textContent = clue.thing;
  top.append(titleEl);

  const rightMeta = node('div', 'row-meta-right');
  const dot = dotDifficulty(clue.dmed ?? clue.davg);
  if (dot) {
    const badge = node('span', 'clue-diff-badge', dot);
    const range = clue.dmin && clue.dmax && clue.dmin !== clue.dmax
      ? ' (from ' + dotDifficulty(clue.dmin) + ' to ' + dotDifficulty(clue.dmax) + ')' : '';
    badge.title = 'Questions using this clue are usually ' + dot + range + '.';
    rightMeta.append(badge);
  }
  const metrics = node('span', 'row-metrics');
  metrics.append(node('span', 'stat-num', count(clue.n)), document.createTextNode(' questions · '),
    node('span', 'stat-num', Math.round(100 * (clue.tied || 0)) + '%'), document.createTextNode(' unique'));
  metrics.title = 'Questions on this answer that use it, and the share of all questions holding these words that are about this answer.';
  rightMeta.append(metrics);
  top.append(rightMeta);
  body.append(top);

  if (clue.example) body.append(node('p', 'row-excerpt', clue.example));
  if (clue.variants?.length) {
    const shown = clue.variants.slice(0, 4).join('; ');
    body.append(node('p', 'row-variants', 'Also worded: ' + shown + (clue.variants.length > 4 ? '; +' + (clue.variants.length - 4) + ' more' : '')));
  }

  const bottom = node('div', 'row-bottom');
  const source = node('span', 'row-source');
  const where = positionLabel(clue);
  if (where) {
    const tag = node('span', 'row-position', where);
    if (clue.where !== 'bonus') tag.title = 'Before the power mark in ' + Math.round(100 * (clue.power || 0)) + '% of its tossups.';
    source.append(tag, node('span', 'row-source-sep', ' · '));
  }
  if (clue.set_name) source.append(node('span', 'row-source-set', clue.set_name));
  const normAns = s => (s || '').replace(/^(the|a|an)\s+/i, '').trim().toLowerCase();
  if (clue.answer && normAns(clue.answer) !== normAns(state.result?.name)) {
    source.append(node('span', 'row-source-sep', ' · '), node('span', 'row-source-ans', clue.answer));
  }
  bottom.append(source);
  if (state.context?.anki && clue.anki !== undefined) {
    const [cls, label, help] = ankiStates[clue.anki || ''] || ankiStates[''];
    const status = node('span', 'anki-status ' + cls, label);
    status.title = help;
    bottom.append(status);
  }
  body.append(bottom);
  row.append(checkbox, body);

  row.addEventListener('click', event => {
    if (event.target === checkbox) return;
    if (row.classList.contains('selected-source') && $('source-reader').open) {
      closeSource();
      return;
    }
    if (clue.example_uid != null) openSource(clue.example_uid, clue.thing, clue.example, row);
  });
  return row;
}

function renderResults() {
  const result = state.result, context = state.context;
  $('result-content').hidden = false;
  const title = result.name || context.query;
  $('result-title').textContent = /^[a-z][A-Z]/.test(title) ? title : title.charAt(0).toUpperCase() + title.slice(1);
  $('draft-open').hidden = !result.found;
  $('selection-bar').hidden = !result.things?.length;
  $('result-warning').hidden = true;
  clear($('result-list'));
  clear($('result-summary'));
  if (!result.found) {
    $('result-summary').textContent = 'No matching answer in the selected scope';
  } else {
    [[result.tossups, 'tossups'], [result.bonuses, 'bonus parts'], [result.sets, 'sets']].forEach(([n, label], i) => {
      if (i > 0) $('result-summary').append(node('span', 'stat-sep', ' · '));
      const item = node('span', 'stat-pill');
      item.append(node('span', 'stat-num', count(n)), document.createTextNode(' ' + label));
      $('result-summary').append(item);
    });
  }
  const things = result.things || [];
  if (!result.found || !things.length) {
    const empty = node('div', 'empty-result');
    empty.append(node('h3', '', result.found ? 'No recurring clues found in this scope.' : 'Try another spelling or fewer filters.'));
    if (result.suggest?.length) empty.append(node('p', '', 'Nearby answerlines: ' + result.suggest.map(item => item[0]).join(', ')));
    $('result-list').append(empty);
  } else if (context.ranking === 'pyramid') {
    // In pyramidal order, group by where the clue itself falls; "Power" means usually before the (*).
    const groups = [
      { name: 'Power', match: c => c.where !== 'bonus' && c.where !== 'giveaway' && (c.power || 0) >= 0.5 },
      { name: 'After power', match: c => c.where !== 'bonus' && c.where !== 'giveaway' },
      { name: 'Giveaway', match: c => c.where === 'giveaway' },
      { name: 'Bonuses only', match: () => true }
    ].map(g => ({ ...g, items: [] }));
    things.forEach((clue, index) => groups.find(g => g.match(clue)).items.push({ clue, index }));
    groups.forEach(group => {
      if (!group.items.length) return;
      const section = node('div', 'clue-group');
      const header = node('div', 'group-header');
      header.append(node('span', 'group-title', group.name), node('span', 'group-count', count(group.items.length)));
      section.append(header);
      group.items.forEach(({ clue, index }) => section.append(clueRow(clue, index)));
      $('result-list').append(section);
    });
  } else {
    things.forEach((clue, index) => $('result-list').append(clueRow(clue, index)));
  }
  const linesBox = $('answerlines');
  const linesList = linesBox.querySelector('.answerlines-list');
  clear(linesList);
  const norm = s => (s || '').replace(/^(the|a|an)\s+/i, '').trim().toLowerCase();
  const otherLines = (result.lines || []).filter(([line]) => norm(line) !== norm(title));
  otherLines.forEach(([line, n]) => {
    const chip = node('button', 'answerline-chip');
    chip.type = 'button';
    chip.title = 'Profile "' + line + '"';
    chip.append(document.createTextNode(line), node('span', 'chip-count', ' (' + count(n) + ')'));
    chip.addEventListener('click', () => {
      $('query').value = line;
      search();
    });
    linesList.append(chip);
  });
  linesBox.hidden = !otherLines.length;
  const warnings = [result.anki_stale, result.mentioned_truncated ? 'Some questions that name this answer were left out (search limit); "also asked" clues may be incomplete.' : ''].filter(Boolean);
  if (warnings.length) {
    $('result-warning').textContent = warnings.join(' ');
    $('result-warning').hidden = false;
  }
  updateSelection();
}

function highlightSentenceInPassage(text, cluePhrase, excerpt) {
  const p = node('p', 'passage');
  if (!text) return p;
  const sentenceRegex = /[^.!?]+[.!?]+(?:["'”’]?\s*)/g;
  const sentenceList = [];
  let m;
  let lastIdx = 0;
  while ((m = sentenceRegex.exec(text)) !== null) {
    sentenceList.push({ start: m.index, end: m.index + m[0].length, text: m[0] });
    lastIdx = m.index + m[0].length;
  }
  if (lastIdx < text.length) sentenceList.push({ start: lastIdx, end: text.length, text: text.slice(lastIdx) });

  const cleanClue = (cluePhrase || '').toLowerCase().replace(/^["'“”]+|["'“”]+$/g, '').trim();
  const cleanExcerpt = (excerpt || '').toLowerCase().trim();
  let targetIndex = cleanClue ? sentenceList.findIndex(s => s.text.toLowerCase().includes(cleanClue)) : -1;
  if (targetIndex === -1 && cleanExcerpt) {
    targetIndex = sentenceList.findIndex(s => {
      const sLower = s.text.toLowerCase().trim();
      return cleanExcerpt.includes(sLower) || sLower.includes(cleanExcerpt) ||
        (cleanExcerpt.length > 25 && sLower.includes(cleanExcerpt.slice(0, 25)));
    });
  }
  if (targetIndex === -1) {
    p.textContent = text;
    return p;
  }
  const target = sentenceList[targetIndex];
  const rawSent = text.slice(target.start, target.end);
  const sentText = rawSent.trimEnd();
  const beforeText = text.slice(0, target.start);
  const afterText = rawSent.slice(sentText.length) + text.slice(target.end);
  if (beforeText) p.append(document.createTextNode(beforeText));
  const mark = node('mark', 'clue-sentence-highlight');
  const kwPos = cleanClue ? sentText.toLowerCase().indexOf(cleanClue) : -1;
  if (kwPos >= 0) {
    mark.append(
      document.createTextNode(sentText.slice(0, kwPos)),
      node('strong', 'clue-highlight-word', sentText.slice(kwPos, kwPos + cleanClue.length)),
      document.createTextNode(sentText.slice(kwPos + cleanClue.length))
    );
  } else {
    mark.textContent = sentText;
  }
  p.append(mark);
  if (afterText) p.append(document.createTextNode(afterText));
  return p;
}

async function openSource(uid, title, excerpt, row) {
  const request = ++state.sourceRequest;
  document.querySelectorAll('.selected-source').forEach(element => element.classList.remove('selected-source'));
  if (row) row.classList.add('selected-source');
  clear($('source-content'));
  $('source-content').append(node('p', '', 'Opening source question…'));
  $('workspace').classList.add('reading');
  const reader = $('source-reader');
  if (!reader.open) {
    if (matchMedia('(max-width:1000px)').matches) reader.showModal(); else reader.show();
    $('source-content').focus({ preventScroll: true });
  }
  try {
    const source = await api('question?uid=' + encodeURIComponent(uid));
    if (request !== state.sourceRequest || !reader.open) return;
    const question = source.question;
    clear($('source-content'));
    const dot = dotDifficulty(question.difficulty);
    const metaParts = [
      question.packet ? ('Packet ' + question.packet) : '',
      (question.kind === 'B' ? 'Bonus' : 'Tossup') + (question.number ? (' ' + question.number) : ''),
      question.subcategory || question.category || '',
      dot ? ('Difficulty ' + question.difficulty + ' (' + dot + ')') : (question.difficulty ? ('Difficulty ' + question.difficulty) : '')
    ].filter(Boolean);
    $('source-content').append(node('h2', '', question.set_name));
    if (metaParts.length) $('source-content').append(node('p', 'source-meta', metaParts.join(' · ')));
    let leadShown = false;
    for (const unit of source.units) {
      if (unit.lead && !leadShown) {
        $('source-content').append(highlightSentenceInPassage(unit.lead, title, excerpt));
        leadShown = true;
      }
      if (unit.part) $('source-content').append(node('p', 'bonus-label', 'PART ' + unit.part + ' · 10 PTS'));
      $('source-content').append(highlightSentenceInPassage(unit.text || '', title, excerpt));
      const answerBox = node('div', 'answer-box');
      answerBox.append(node('div', 'answer-label', 'Answerline'),
        node('div', 'answer-text', stripTag(unit.answer || unit.main) || 'No answerline recorded'));
      $('source-content').append(answerBox);
    }
    $('source-content').scrollTop = 0;
    announce('Source question opened from ' + question.set_name + '.');
  } catch (error) {
    if (request === state.sourceRequest) $('source-content').replaceChildren(node('p', 'error-text', error.message));
  }
}

function closeSource() {
  ++state.sourceRequest;
  $('workspace').classList.remove('reading');
  document.querySelectorAll('.selected-source').forEach(row => row.classList.remove('selected-source'));
  if ($('source-reader').open) $('source-reader').close();
}

function closeMenus() {
  document.querySelectorAll('.filter-menu').forEach(m => m.hidden = true);
  document.querySelectorAll('.filter-dropdown-btn').forEach(b => b.setAttribute('aria-expanded', 'false'));
}

function csvCell(value) {
  let text = String(value ?? '');
  if (/^[=+@\-\t\r]/.test(text)) text = "'" + text;
  return '"' + text.replaceAll('"', '""') + '"';
}

function exportSelected() {
  if (!state.selected.size || dirty() || !state.result) return;
  const fields = ['answer', 'clue', 'also_worded', 'questions', 'unique', 'position', 'before_power', 'level', 'example',
    'source', 'example_uid', 'anki', 'category', 'difficulty', 'years'];
  const lines = [fields.map(csvCell).join(',')];
  for (const index of [...state.selected].sort((a, b) => a - b)) {
    const clue = state.result.things[index], context = state.context;
    lines.push([state.result.name, clue.thing, (clue.variants || []).join('; '), clue.n, Math.round(100 * (clue.tied || 0)) + '%',
      positionLabel(clue), Math.round(100 * (clue.power || 0)) + '%', dotDifficulty(clue.dmed ?? clue.davg), clue.example, clue.source,
      clue.example_uid, (ankiStates[clue.anki || ''] || [])[1] || '', context.category, context.difficulty, context.year]
      .map(csvCell).join(','));
  }
  const url = URL.createObjectURL(new Blob(['﻿' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' }));
  const link = node('a');
  link.href = url;
  link.download = (state.result.name || 'stockfisher').replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '').slice(0, 80) + '-clues.csv';
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  announce('Exported ' + state.selected.size + ' selected clues.');
}

function setDatabase(info) {
  state.connected = !!info.connected;
  $('database-path').value = info.path || '';
  $('database-info').textContent = info.connected
    ? count(info.units) + ' answerable units from ' + count(info.sets) + ' sets.'
    : (info.error || 'Select your existing question index to start.');
  busy(false);
}

function setupFilterDropdown(dropdownId, btnId, valId, menuId, inputId, defaultLabel) {
  const btn = $(btnId), valSpan = $(valId), menu = $(menuId), input = $(inputId);
  const selectedMap = new Map();

  function update() {
    input.value = Array.from(selectedMap.keys()).join(', ');
    btn.classList.toggle('has-value', selectedMap.size > 0);
    menu.querySelectorAll('.filter-menu-item').forEach(item => {
      item.classList.toggle('selected', selectedMap.size ? selectedMap.has(item.dataset.value) : item.dataset.value === '');
    });
    const labels = Array.from(selectedMap.values());
    btn.title = labels.join(', ');
    valSpan.textContent = !labels.length ? defaultLabel : labels.length <= 2 ? labels.join(', ') : labels.length + ' selected';
    inputsChanged();
  }

  btn.addEventListener('click', event => {
    event.stopPropagation();
    const willOpen = menu.hidden;
    closeMenus();
    menu.hidden = !willOpen;
    btn.setAttribute('aria-expanded', String(willOpen));
  });
  menu.querySelectorAll('.filter-menu-item').forEach(item => {
    item.addEventListener('click', event => {
      event.stopPropagation();
      const val = item.dataset.value || '';
      if (!val) selectedMap.clear();
      else if (selectedMap.has(val)) selectedMap.delete(val);
      else selectedMap.set(val, item.dataset.label || defaultLabel);
      update();
    });
  });
}

$('search-form').addEventListener('submit', event => {
  event.preventDefault();
  search();
});
setupFilterDropdown('category-dropdown', 'category-btn', 'category-val', 'category-menu', 'category', 'All');
setupFilterDropdown('difficulty-dropdown', 'difficulty-btn', 'difficulty-val', 'difficulty-menu', 'difficulty', 'All');
document.addEventListener('click', event => {
  if (!event.target.closest('.filter-dropdown')) closeMenus();
});
document.querySelectorAll('#search-form input, #search-form select').forEach(input => input.addEventListener('input', inputsChanged));
$('options-toggle').addEventListener('click', () => {
  const hidden = !$('options').hidden;
  $('options').hidden = hidden;
  $('options-toggle').setAttribute('aria-expanded', String(!hidden));
  $('options-toggle').querySelector('.options-icon').textContent = hidden ? '+' : '−';
});
$('select-all').addEventListener('change', event => {
  state.selected.clear();
  document.querySelectorAll('.row-select').forEach(checkbox => {
    checkbox.checked = event.target.checked;
    if (checkbox.checked) state.selected.add(Number(checkbox.dataset.index));
  });
  updateSelection();
});
$('export-button').addEventListener('click', exportSelected);
$('source-close').addEventListener('click', () => closeSource());
$('source-reader').addEventListener('cancel', event => {
  event.preventDefault();
  closeSource();
});
$('database-open').addEventListener('click', () => $('database-dialog').showModal());
document.querySelectorAll('[data-close]').forEach(button => button.addEventListener('click', () => $(button.dataset.close).close()));
document.addEventListener('keydown', event => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault();
    if (!document.querySelector('dialog:modal')) {
      $('query').focus();
      $('query').select();
    }
  }
  if (event.key === 'Escape') {
    if (document.querySelector('.filter-menu:not([hidden])')) {
      closeMenus();
      return;
    }
    if ($('source-reader').open && !document.querySelector('dialog:modal')) closeSource();
  }
});
$('database-form').addEventListener('submit', async event => {
  event.preventDefault();
  const button = event.submitter;
  button.disabled = true;
  $('database-error').textContent = '';
  try {
    const info = await api('database', { path: $('database-path').value });
    closeMenus();
    closeSource();
    state.result = null;
    state.context = null;
    state.selected.clear();
    $('result-content').hidden = true;
    $('dirty-notice').hidden = true;
    showError('');
    setDatabase(info);
    $('database-dialog').close();
  } catch (error) {
    $('database-error').textContent = error.message;
  } finally {
    button.disabled = false;
  }
});
$('quit-button').addEventListener('click', async () => {
  try {
    await api('shutdown', {});
    $('database-dialog').close();
    closeMenus();
    closeSource();
    state.connected = false;
    busy(false);
    showError('StockFisher is closed. You can close this window and reopen it from your shortcut.');
  } catch (error) {
    $('database-error').textContent = error.message;
  }
});
$('draft-open').addEventListener('click', () => {
  if (!state.context) return;
  $('draft-context').textContent = 'For ' + state.result.name + ', using the filters from this profile.';
  clear($('draft-result'));
  $('draft-dialog').showModal();
  $('draft-text').focus();
});
$('draft-form').addEventListener('submit', async event => {
  event.preventDefault();
  $('draft-button').disabled = true;
  $('draft-result').replaceChildren(node('p', '', 'Checking the evidence…'));
  try {
    const result = await api('check', { ...state.context, answer: state.result.name, clue: $('draft-text').value });
    clear($('draft-result'));
    $('draft-result').append(
      node('h3', '', result.ok ? 'No automatic flags' : 'Review needed'),
      node('p', '', result.length + ' characters · Answer words found: ' + (result.leaks.join(', ') || 'none'))
    );
    for (const passage of result.similar || []) {
      const block = node('div', 'draft-passage');
      const dot = dotDifficulty(passage[5]);
      block.append(node('p', '', passage[4]), node('p', 'hint', passage[1] + (dot ? ' [' + dot + ']' : '') + ' · ' + passage[3]));
      $('draft-result').append(block);
    }
    $('draft-result').append(node('p', 'hint', 'This checks corpus support and wording. Verify factual accuracy separately.'));
  } catch (error) {
    $('draft-result').replaceChildren(node('p', 'error-text', error.message));
  } finally {
    $('draft-button').disabled = false;
  }
});

(async () => {
  busy(true);
  try {
    const info = await api('status');
    setDatabase(info);
    if (!info.connected) $('database-dialog').showModal(); else $('query').focus();
  } catch (error) {
    busy(false);
    showError(error.message);
  }
})();
