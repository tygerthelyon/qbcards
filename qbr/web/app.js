'use strict';

const $ = id => document.getElementById(id);
const token = document.querySelector('meta[name="stockfisher-token"]').content;
const state = {
  mode: 'profile',
  result: null,
  context: null,
  selected: new Set(),
  busy: false,
  connected: false,
  sourceRequest: 0,
  sourceButton: null,
  offset: 0
};
const count = value => Number(value || 0).toLocaleString();
const ankiLabels = {
  'card': 'In deck',
  'suspended': 'Suspended',
  'text': 'In deck',
  'on-note': 'In deck',
  '': 'Missing'
};
const dotMap = {
  1: 'MS', 2: 'easy HS', 3: 'HS', 4: 'hard HS', 5: 'HS nats',
  6: '●', 7: '●●', 8: '●●●', 9: '●●●●', 10: 'open'
};
const dotDifficulty = diff => {
  const d = Number(diff);
  return d ? (dotMap[d] || String(d)) : '';
};

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
    mode: state.mode,
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
  if (state.context?.mode === 'search') {
    $('previous-page').disabled = !!dirty() || state.offset === 0;
    $('next-page').disabled = !!dirty() || state.offset + 20 >= (state.result?.units || 0);
  }
}

function setMode(mode) {
  state.mode = mode;
  document.querySelectorAll('[data-mode]').forEach(button => {
    button.setAttribute('aria-pressed', String(button.dataset.mode === mode));
  });
  const profile = mode === 'profile';
  $('search-button').textContent = 'Search';
  $('query').placeholder = 'Search';
  document.querySelector('label[for=query]').textContent = profile ? 'Answer to research' : 'Question text to find';
  $('profile-options').hidden = !profile;
  $('mode-hint').textContent = profile ? 'Start broad. You can narrow the results with filters.' : 'Search passages across answers. Use ans:hirst butterflies to narrow by answerline.';
  inputsChanged();
}

function busy(value) {
  state.busy = value;
  $('search-controls').disabled = value || !state.connected;
  document.querySelectorAll('[data-example]').forEach(button => {
    button.disabled = value || !state.connected;
  });
  $('loading').hidden = !value;
  $('results').setAttribute('aria-busy', String(value));
  updateSelection();
}

async function search(offset = 0, savedContext = null) {
  if (state.busy || !state.connected) return;
  const context = savedContext || inputs();
  if (!context.query) {
    $('query').focus();
    return;
  }
  document.querySelectorAll('.filter-menu').forEach(m => m.hidden = true);
  document.querySelectorAll('.filter-dropdown-btn').forEach(b => b.setAttribute('aria-expanded', 'false'));
  closeSource(false);
  showError('');
  state.result = null;
  state.context = null;
  state.selected.clear();
  $('result-content').hidden = true;
  $('welcome').hidden = true;
  $('dirty-notice').hidden = true;
  busy(true);
  announce('Searching your question index.');
  try {
    state.result = await api(context.mode, { ...context, offset });
    state.context = context;
    state.offset = offset;
    renderResults();
    announce((context.mode === 'profile' ? 'Profile' : 'Search') + ' ready for ' + context.query + '.');
  } catch (error) {
    showError(error.message);
    announce(error.message);
  } finally {
    busy(false);
    inputsChanged();
  }
}

function readButton(uid, title, excerpt, row) {
  const button = node('button', 'source-button', 'Read question');
  button.append(node('span', '', '↗'));
  button.lastChild.setAttribute('aria-hidden', 'true');
  button.setAttribute('aria-label', 'Read source question for ' + title);
  button.setAttribute('aria-controls', 'source-reader');
  button.addEventListener('click', () => openSource(uid, title, excerpt, button, row));
  return button;
}

function clueRow(clue, index) {
  const row = node('article', 'result-row');
  const checkbox = node('input', 'row-select');
  checkbox.type = 'checkbox';
  checkbox.setAttribute('aria-label', 'Select ' + clue.thing);
  checkbox.addEventListener('change', () => {
    if (checkbox.checked) state.selected.add(index); else state.selected.delete(index);
    updateSelection();
  });
  const body = node('div', 'row-body');
  const top = node('div', 'row-top');
  const titleEl = node('h3', 'row-title');
  if (clue.kind === 'title' || clue.kind === 'work') {
    titleEl.append(node('em', '', clue.thing));
  } else {
    titleEl.textContent = clue.thing;
  }
  top.append(titleEl);

  const rightMeta = node('div', 'row-meta-right');
  const diffVal = Number(clue.difficulty) || 0;
  const dot = dotDifficulty(diffVal);
  if (dot) {
    const diffBadge = node('span', 'clue-diff-badge', dot);
    diffBadge.title = 'Difficulty: ' + diffVal + ' (' + dot + ')';
    rightMeta.append(diffBadge);
  }
  const metrics = node('span', 'row-metrics');
  metrics.textContent = count(clue.n) + ' questions · ' + Math.round(100 * (clue.tied || 0)) + '% unique';
  metrics.title = 'Question frequency on this answer and exclusivity across the index.';
  rightMeta.append(metrics);
  top.append(rightMeta);
  body.append(top);

  if (clue.example) body.append(node('p', 'row-excerpt', clue.example));

  const bottom = node('div', 'row-bottom');
  const sourceContainer = node('span', 'row-source');
  let setName = clue.set_name || '';
  let ansName = clue.answer || '';
  if (!setName && !ansName && clue.source) {
    const commaIdx = clue.source.lastIndexOf(', ');
    if (commaIdx !== -1) {
      setName = clue.source.slice(0, commaIdx);
      ansName = clue.source.slice(commaIdx + 2);
    } else {
      setName = clue.source;
    }
  }
  if (setName) {
    sourceContainer.append(node('span', 'row-source-set', setName));
  }
  if (ansName) {
    if (setName) sourceContainer.append(node('span', 'row-source-sep', ' · '));
    sourceContainer.append(node('span', 'row-source-ans', ansName));
  }
  if (!setName && !ansName) {
    sourceContainer.textContent = 'No example source available';
  }
  bottom.append(sourceContainer);

  if (state.context?.anki || clue.anki !== undefined) {
    let ankiClass = 'missing';
    let ankiText = '○ Missing';
    if (clue.anki === 'card' || clue.anki === 'text' || clue.anki === 'on-note') {
      ankiClass = 'in-deck';
      ankiText = '● In deck';
    } else if (clue.anki === 'suspended') {
      ankiClass = 'suspended';
      ankiText = '● In deck (suspended)';
    }
    const ankiTag = node('span', 'anki-status ' + ankiClass, ankiText);
    bottom.append(ankiTag);
  }
  body.append(bottom);
  row.append(checkbox, body);

  row.addEventListener('click', (event) => {
    if (event.target === checkbox) return;
    if (row.classList.contains('selected-source') && $('source-reader').open) {
      closeSource();
      return;
    }
    if (clue.example_uid != null) {
      openSource(clue.example_uid, clue.thing, clue.example, null, row);
    }
  });

  return row;
}

function searchRow(hit) {
  const row = node('article', 'result-row');
  row.append(node('span'));
  const body = node('div', 'row-body');
  const top = node('div', 'row-top');
  const dot = dotDifficulty(hit.difficulty);
  const dotPart = dot ? (' [' + dot + ']') : '';
  top.append(
    node('h3', 'row-title', hit.main),
    node('span', 'row-metrics', hit.difficulty ? ('Difficulty ' + hit.difficulty + dotPart) : '')
  );
  const excerpt = hit.sentences?.[0]?.s || hit.text || '';
  body.append(top, node('p', 'row-excerpt', excerpt));
  const bottom = node('div', 'row-bottom');
  const location = hit.set_name + dotPart;
  bottom.append(node('span', 'row-source', location), readButton(hit.uid, hit.main, excerpt, row));
  body.append(bottom);
  row.append(body);
  return row;
}

function renderResults() {
  const result = state.result, context = state.context;
  const profile = context.mode === 'profile';
  $('result-content').hidden = false;
  $('result-kicker').textContent = profile ? 'Answer profile' : 'Question text';
  $('result-title').textContent = profile ? (result.name || context.query) : context.query;
  $('draft-open').hidden = !profile || !result.found;
  $('selection-bar').hidden = !profile || !result.things?.length;
  $('pagination').hidden = profile || result.units <= 20;
  $('answerlines').hidden = !profile || !result.lines?.length;
  $('result-warning').hidden = true;
  clear($('result-list'));
  if (profile) {
    clear($('result-summary'));
    if (!result.found) {
      $('result-summary').textContent = 'No matching answer in the selected scope';
    } else {
      const stats = [
        [count(result.questions), 'questions'],
        [count(result.tossups), 'tossups'],
        [count(result.bonuses), 'bonuses'],
        [count(result.sets), 'sets']
      ];
      stats.forEach(([n, label], i) => {
        if (i > 0) $('result-summary').append(node('span', 'stat-sep', ' · '));
        const item = node('span', 'stat-pill');
        item.append(node('span', 'stat-num', n), document.createTextNode(' ' + label));
        $('result-summary').append(item);
      });
    }
    const things = result.things || [];
    if (!result.found || !things.length) {
      const empty = node('div', 'empty-result');
      empty.append(node('h3', '', result.found ? 'No recurring clues found in this scope.' : 'Try another spelling or fewer filters.'));
      if (result.suggest?.length) empty.append(node('p', '', 'Nearby answerlines: ' + result.suggest.map(item => item[0]).join(', ')));
      empty.append(node('p', '', 'Try searching with fewer filters or broadening categories.'));
      $('result-list').append(empty);
    } else {
      const groups = [
        { name: 'Power', items: [], match: w => w === 'lead-in' || w === 'early' },
        { name: 'Middle', items: [], match: w => w === 'middle' || w === 'late' },
        { name: 'Giveaways', items: [], match: w => w === 'giveaway' },
        { name: 'Bonuses', items: [], match: w => w === 'bonus' }
      ];

      things.forEach((clue, index) => {
        const where = clue.where || '';
        let targetGroup = groups.find(g => g.match(where));
        if (!targetGroup) targetGroup = groups[1];
        targetGroup.items.push({ clue, index });
      });

      groups.forEach(group => {
        if (!group.items.length) return;
        const section = node('div', 'clue-group');
        const header = node('div', 'group-header');
        header.append(node('span', 'group-title', group.name));
        section.append(header);
        group.items.forEach(({ clue, index }) => section.append(clueRow(clue, index)));
        $('result-list').append(section);
      });
    }
    const linesBox = $('answerlines');
    const linesList = linesBox.querySelector('.answerlines-list');
    clear(linesList);
    const primaryName = (result.name || context.query || '').trim().toLowerCase();
    const rawLines = result.lines || [];
    let displayLines = rawLines.filter(([line]) => line.trim().toLowerCase() !== primaryName);
    if (!displayLines.length && rawLines.length > 1) displayLines = rawLines;
    if (displayLines.length) {
      const label = linesBox.querySelector('.answerlines-label');
      if (label) label.textContent = 'Alternates:';
      displayLines.forEach(([line, n]) => {
        const chip = node('button', 'answerline-chip');
        chip.type = 'button';
        chip.title = 'Search "' + line + '"';
        chip.append(
          document.createTextNode(line),
          node('span', 'chip-count', ' (' + count(n) + ')')
        );
        chip.addEventListener('click', e => {
          e.preventDefault();
          $('query').value = line;
          search();
        });
        linesList.append(chip);
      });
      linesBox.hidden = false;
    } else {
      linesBox.hidden = true;
    }
    const warnings = [result.anki_stale, result.mentioned_truncated ? 'Related-answer mentions reached the search limit; some counts may be incomplete.' : ''].filter(Boolean);
    if (warnings.length) { $('result-warning').textContent = warnings.join(' '); $('result-warning').hidden = false; }
  } else {
    clear($('result-summary'));
    const stats = [
      [count(result.questions), 'questions'],
      [count(result.units), 'matching units']
    ];
    stats.forEach(([n, label], i) => {
      if (i > 0) $('result-summary').append(node('span', 'stat-sep', ' · '));
      const item = node('span', 'stat-pill');
      item.append(node('span', 'stat-num', n), document.createTextNode(' ' + label));
      $('result-summary').append(item);
    });
    result.hits.forEach(hit => $('result-list').append(searchRow(hit)));
    if (!result.hits.length) $('result-list').append(node('p', 'empty-result', 'No matching passages. Try different wording or fewer filters.'));
    $('page-label').textContent = count(state.offset + 1) + '–' + count(Math.min(result.units, state.offset + 20)) + ' of ' + count(result.units);
    $('previous-page').disabled = state.offset === 0;
    $('next-page').disabled = state.offset + 20 >= result.units;
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
  if (lastIdx < text.length) {
    sentenceList.push({ start: lastIdx, end: text.length, text: text.slice(lastIdx) });
  }

  const cleanClue = (cluePhrase || '').toLowerCase().replace(/^["'“”]+|["'“”]+$/g, '').trim();
  const cleanExcerpt = (excerpt || '').toLowerCase().trim();

  let targetIndex = -1;
  if (cleanClue) {
    targetIndex = sentenceList.findIndex(s => s.text.toLowerCase().includes(cleanClue));
  }
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

  const targetSentence = sentenceList[targetIndex];
  const rawSent = text.slice(targetSentence.start, targetSentence.end);
  const trimmedLen = rawSent.trimEnd().length;
  const sentText = rawSent.slice(0, trimmedLen);
  const trailingSpace = rawSent.slice(trimmedLen);
  const beforeText = text.slice(0, targetSentence.start);
  const afterText = trailingSpace + text.slice(targetSentence.end);

  if (beforeText) p.append(document.createTextNode(beforeText));

  const mark = node('mark', 'clue-sentence-highlight');
  if (cleanClue) {
    const kwPos = sentText.toLowerCase().indexOf(cleanClue);
    if (kwPos >= 0) {
      mark.append(
        document.createTextNode(sentText.slice(0, kwPos)),
        node('strong', 'clue-highlight-word', sentText.slice(kwPos, kwPos + cleanClue.length)),
        document.createTextNode(sentText.slice(kwPos + cleanClue.length))
      );
    } else {
      mark.textContent = sentText;
    }
  } else {
    mark.textContent = sentText;
  }
  p.append(mark);

  if (afterText) p.append(document.createTextNode(afterText));

  return p;
}

async function openSource(uid, title, excerpt, button, row) {
  const request = ++state.sourceRequest;
  state.sourceButton = button;
  document.querySelectorAll('.selected-source').forEach(element => element.classList.remove('selected-source'));
  if (row) row.classList.add('selected-source');
  clear($('source-content'));
  $('source-content').append(node('p', '', 'Opening source question…'));
  $('workspace').classList.add('reading');
  const reader = $('source-reader');
  if (!reader.open) {
    if (matchMedia('(max-width:1000px)').matches) reader.showModal(); else reader.show();
  }
  try {
    const source = await api('question?uid=' + encodeURIComponent(uid));
    if (request !== state.sourceRequest || !reader.open) return;
    const question = source.question;
    clear($('source-content'));
    const dot = dotDifficulty(question.difficulty);
    const heading = node('h2', '', question.set_name + (dot ? (' [' + dot + ']') : ''));
    heading.id = 'source-title';
    $('source-content').append(heading);
    for (const unit of source.units) {
      if (unit.lead) $('source-content').append(highlightSentenceInPassage(unit.lead, title, excerpt));
      if (unit.part) $('source-content').append(node('p', 'bonus-label', 'PART ' + unit.part));
      const text = unit.text || '';
      $('source-content').append(highlightSentenceInPassage(text, title, excerpt));

      const answerBox = node('div', 'answer-box');
      answerBox.append(
        node('div', 'answer-label', 'Answerline'),
        node('div', 'answer-text', unit.answer || unit.main || 'No answerline recorded')
      );
      $('source-content').append(answerBox);
    }
    $('source-content').scrollTop = 0;
    announce('Source question opened from ' + question.set_name + '.');
  } catch (error) {
    if (request === state.sourceRequest) $('source-content').replaceChildren(node('p', 'error-text', error.message));
  }
}

function closeSource(restoreFocus = true) {
  ++state.sourceRequest;
  $('workspace').classList.remove('reading');
  document.querySelectorAll('.selected-source').forEach(row => row.classList.remove('selected-source'));
  if ($('source-reader').open) $('source-reader').close();
  if (restoreFocus && state.sourceButton?.isConnected) state.sourceButton.focus({ preventScroll: true });
}

function csvCell(value) {
  let text = String(value ?? '');
  if (/^[=+@\-\t\r]/.test(text)) text = "'" + text;
  return '"' + text.replaceAll('"', '""') + '"';
}

function exportSelected() {
  if (!state.selected.size || dirty() || !state.result) return;
  const fields = ['answer', 'clue', 'questions', 'tied', 'position', 'example', 'source', 'example_uid', 'anki', 'category', 'difficulty', 'years'];
  const lines = [fields.map(csvCell).join(',')];
  for (const index of [...state.selected].sort((a, b) => a - b)) {
    const clue = state.result.things[index], context = state.context;
    lines.push([state.result.name, clue.thing, clue.n, clue.tied, clue.where, clue.example, clue.source,
      clue.example_uid, clue.anki, context.category, context.difficulty, context.year].map(csvCell).join(','));
  }
  const url = URL.createObjectURL(new Blob(['\ufeff' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' }));
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
  $('category-list')?.replaceChildren(...(info.categories || []).map(category => {
    const option = node('option');
    option.value = category;
    return option;
  }));
  if (info.connected) {
    $('index-status').textContent = count(info.sets) + ' sets';
    $('index-status').title = count(info.units) + ' answerable units from ' + count(info.sets) + ' sets.';
    $('database-info').textContent = count(info.units) + ' answerable units from ' + count(info.sets) + ' sets.';
  } else {
    $('index-status').textContent = 'Connect a question index';
    $('database-info').textContent = info.error || 'Select your existing question index to start.';
  }
  busy(false);
}

$('search-form').addEventListener('submit', event => {
  event.preventDefault();
  search();
});
document.querySelectorAll('[data-mode]').forEach(button => button.addEventListener('click', () => setMode(button.dataset.mode)));
document.querySelectorAll('[data-example]').forEach(button => button.addEventListener('click', () => {
  setMode('profile');
  $('query').value = button.dataset.example;
  search();
}));
function setupFilterDropdown(dropdownId, btnId, valId, menuId, inputId, defaultLabel) {
  const dropdown = $(dropdownId);
  const btn = $(btnId);
  const valSpan = $(valId);
  const menu = $(menuId);
  const input = $(inputId);
  if (!dropdown || !btn || !menu || !input) return;

  const selectedMap = new Map();

  function update() {
    if (selectedMap.size === 0) {
      input.value = '';
      valSpan.textContent = defaultLabel;
      btn.title = '';
      btn.classList.remove('has-value');
      menu.querySelectorAll('.filter-menu-item').forEach(item => {
        item.classList.toggle('selected', item.dataset.value === '');
      });
    } else {
      input.value = Array.from(selectedMap.keys()).join(', ');
      btn.classList.add('has-value');
      menu.querySelectorAll('.filter-menu-item').forEach(item => {
        item.classList.toggle('selected', selectedMap.has(item.dataset.value));
      });
      const labels = Array.from(selectedMap.values());
      btn.title = labels.join(', ');
      if (labels.length <= 2) {
        valSpan.textContent = labels.join(', ');
      } else {
        valSpan.textContent = labels.length + ' selected';
      }
    }
    inputsChanged();
  }

  btn.addEventListener('click', event => {
    event.stopPropagation();
    const willOpen = menu.hidden;
    document.querySelectorAll('.filter-menu').forEach(m => {
      if (m !== menu) m.hidden = true;
    });
    document.querySelectorAll('.filter-dropdown-btn').forEach(b => {
      if (b !== btn) b.setAttribute('aria-expanded', 'false');
    });
    menu.hidden = !willOpen;
    btn.setAttribute('aria-expanded', String(willOpen));
  });

  menu.querySelectorAll('.filter-menu-item').forEach(item => {
    item.addEventListener('click', event => {
      event.stopPropagation();
      const val = item.dataset.value || '';
      const label = item.dataset.label || defaultLabel;

      if (!val) {
        selectedMap.clear();
        update();
        return;
      }

      if (selectedMap.has(val)) {
        selectedMap.delete(val);
      } else {
        selectedMap.set(val, label);
      }
      update();
    });
  });
}

setupFilterDropdown('category-dropdown', 'category-btn', 'category-val', 'category-menu', 'category', 'All');
setupFilterDropdown('difficulty-dropdown', 'difficulty-btn', 'difficulty-val', 'difficulty-menu', 'difficulty', 'All');

document.addEventListener('click', event => {
  if (!event.target.closest('.filter-dropdown')) {
    document.querySelectorAll('.filter-menu').forEach(m => m.hidden = true);
    document.querySelectorAll('.filter-dropdown-btn').forEach(b => b.setAttribute('aria-expanded', 'false'));
  }
});

document.querySelectorAll('#search-form input, #search-form select').forEach(input => input.addEventListener('input', inputsChanged));
$('options-toggle').addEventListener('click', () => {
  const hidden = !$('options').hidden;
  $('options').hidden = hidden;
  $('options-toggle').setAttribute('aria-expanded', String(!hidden));
  const icon = $('options-toggle').querySelector('.options-icon');
  if (icon) icon.textContent = hidden ? '+' : '−';
});
$('select-all').addEventListener('change', event => {
  state.selected.clear();
  document.querySelectorAll('.row-select').forEach((checkbox, index) => {
    checkbox.checked = event.target.checked;
    if (checkbox.checked) state.selected.add(index);
  });
  updateSelection();
});
$('export-button').addEventListener('click', exportSelected);
$('previous-page').addEventListener('click', () => search(Math.max(0, state.offset - 20), state.context));
$('next-page').addEventListener('click', () => search(state.offset + 20, state.context));
$('source-close').addEventListener('click', () => closeSource());
$('source-reader').addEventListener('cancel', event => {
  event.preventDefault();
  closeSource();
});
$('database-open')?.addEventListener('click', () => $('database-dialog').showModal());
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
    const openMenu = document.querySelector('.filter-menu:not([hidden])');
    if (openMenu) {
      document.querySelectorAll('.filter-menu').forEach(m => m.hidden = true);
      document.querySelectorAll('.filter-dropdown-btn').forEach(b => b.setAttribute('aria-expanded', 'false'));
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
    document.querySelectorAll('.filter-menu').forEach(m => m.hidden = true);
  document.querySelectorAll('.filter-dropdown-btn').forEach(b => b.setAttribute('aria-expanded', 'false'));
  closeSource(false);
    state.result = null;
    state.context = null;
    state.selected.clear();
    $('result-content').hidden = true;
    $('welcome').hidden = false;
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
$('quit-button')?.addEventListener('click', async () => {
  try {
    await api('shutdown', {});
    $('database-dialog').close();
    document.querySelectorAll('.filter-menu').forEach(m => m.hidden = true);
  document.querySelectorAll('.filter-dropdown-btn').forEach(b => b.setAttribute('aria-expanded', 'false'));
  closeSource(false);
    state.connected = false;
    busy(false);
    showError('StockFisher is closed. You can close this window and reopen it from your shortcut.');
  } catch (error) {
    $('database-error').textContent = error.message;
  }
});
$('draft-open').addEventListener('click', () => {
  if (!state.context || state.context.mode !== 'profile') return;
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
      const dotPart = dot ? (' [' + dot + ']') : '';
      block.append(
        node('p', '', passage[4]),
        node('p', 'hint', passage[1] + dotPart + ' · ' + passage[3])
      );
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
