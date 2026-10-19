/* Progressive enhancement for Decipher compat 144 radio matrices.
 * Native inputs are the sole answer model. Completion uses the native Continue button. */
(function () {
  'use strict';
  document.querySelectorAll('.question.qswipe').forEach(function (root) {
    if (root.dataset.swipeReady) return;
    var native = root.querySelector('.answers');
    var groups = new Map();
    var form = root.closest('form');
    var continueButton = form && form.querySelector('#btn_continue');
    // Auto-completion is supported only on a single-question page.
    if (!native || !continueButton || continueButton.disabled || form.querySelectorAll('.question').length !== 1) return;
    native.querySelectorAll('input[type="radio"]').forEach(function (input) {
      if (!groups.has(input.name)) groups.set(input.name, []);
      groups.get(input.name).push(input);
    });
    var rows = Array.from(groups.values()).map(function (inputs) {
      var tr = inputs[0].closest('tr');
      var legend = tr && tr.querySelector('.row-legend');
      var byCode = {};
      inputs.forEach(function (input) {
        var cell = input.closest('td');
        var headers = cell && cell.getAttribute('headers');
        ['c1', 'c2', 'c3'].forEach(function (code) {
          if (headers && headers.split(/\s+/).some(function (h) { return h.endsWith('_' + code); })) byCode[code] = input;
        });
      });
      return { inputs: inputs, byCode: byCode, title: legend && legend.textContent.trim() };
    });
    // Unsupported native markup leaves the matrix fully usable.
    if (!rows.length || rows.some(function (r) { return !r.title || r.inputs.length !== 3 || !r.byCode.c1 || !r.byCode.c2 || !r.byCode.c3; })) return;
    var ui = document.createElement('section');
    ui.className = 'qsw-ui';
    ui.setAttribute('aria-label', 'Swipe cards');
    var helpId = root.id + '-swipe-help';
    ui.innerHTML = '<p class="qsw-sr qsw-status" role="status" aria-live="polite" aria-atomic="true"></p>' +
      '<p class="qsw-sr qsw-help">Swipe left for Dislike or right for Like. On the focused card, press Left Arrow for Dislike, S for Skip, or Right Arrow for Like. Skip is an explicit answer.</p>' +
      '<div class="qsw-stack"><article class="qsw-card" tabindex="0" aria-roledescription="swipe card"><div class="qsw-art" aria-hidden="true"><span></span><i></i><b></b></div>' +
      '<div class="qsw-card-copy"><h2 class="qsw-title"></h2></div><span class="qsw-cue" aria-hidden="true"></span></article></div>' +
      '<div class="qsw-actions" role="group" aria-label="Choose an answer"><button type="button" data-answer="c1"><span aria-hidden="true">−</span>Dislike</button><button type="button" data-answer="c2"><span aria-hidden="true">→</span>Skip</button><button type="button" data-answer="c3"><span aria-hidden="true">+</span>Like</button></div>';
    var completion = document.createElement('p');
    completion.className = 'qsw-completion';
    completion.setAttribute('role', 'status');
    completion.setAttribute('tabindex', '-1');
    completion.hidden = true;
    ui.appendChild(completion);
    var stack = ui.querySelector('.qsw-stack');
    var actions = ui.querySelector('.qsw-actions');
    var card = ui.querySelector('.qsw-card');
    var status = ui.querySelector('.qsw-status');
    var behind = card.cloneNode(true);
    behind.classList.add('qsw-behind');
    behind.removeAttribute('tabindex');
    behind.removeAttribute('aria-roledescription');
    behind.setAttribute('aria-hidden', 'true');
    card.before(behind);
    var cue = card.querySelector('.qsw-cue');
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    var busy = false, timer = null, pointer = null;
    var phase = 'answering', autoAttempted = false;
    var requestPending = false, submitSeen = false, recoveryTimer = null;
    function leaveDeck(message) {
      lock(true); pointer = null;
      stack.hidden = true; actions.hidden = true;
      ui.querySelector('.qsw-help').hidden = true;
      status.textContent = '';
      completion.textContent = message; completion.hidden = false;
      completion.focus();
    }
    function recover(message) {
      window.clearTimeout(timer); window.clearTimeout(recoveryTimer);
      phase = 'recovery'; requestPending = false; submitSeen = false;
      leaveDeck(message || 'Your answers are still selected. Please use Continue to try again.');
      // Return the original controls so validation or a stalled request cannot trap the respondent.
      native.hidden = false;
      continueButton.classList.remove('qsw-continue-hidden');
      continueButton.disabled = false;
    }
    function beginRequest() {
      phase = 'submitting'; requestPending = true; submitSeen = false;
      leaveDeck('Saving your answers…');
      recoveryTimer = window.setTimeout(function () {
        recover('This is taking longer than expected. Your answers are still selected. Use Continue to try again.');
      }, 12000);
    }
    function completeDeck() {
      if (phase !== 'answering' || autoAttempted) return;
      if (!rows.every(function (row) { return selected(row); })) return;
      autoAttempted = true;
      leaveDeck('Saving your answers…');
      if (continueButton.disabled || !continueButton.isConnected) { recover(); return; }
      // Retain Decipher's click, validation and submit handlers; never call form.submit().
      try { continueButton.click(); } catch (error) { recover(); }
    }
    function lock(value) {
      busy = value;
      ui.querySelectorAll('[data-answer]').forEach(function (b) { b.setAttribute('aria-disabled', String(value)); });
    }
    function resetMotion() {
      card.style.transition = 'none';
      card.style.transform = '';
      card.style.opacity = '';
      cue.style.opacity = '0';
      behind.style.transform = '';
    }
    function threshold() { return Math.max(65, Math.min(120, card.clientWidth * 0.27)); }
    function move(dx, dy) {
      var fraction = Math.min(1, Math.abs(dx) / threshold());
      card.style.transition = 'none';
      card.style.transform = 'translate(' + dx + 'px,' + (dy * 0.12) + 'px) rotate(' + Math.max(-14, Math.min(14, dx / 18)) + 'deg)';
      card.style.opacity = String(1 - Math.min(0.78, Math.abs(dx) / (card.clientWidth * 0.85)));
      cue.textContent = dx < 0 ? 'Dislike' : 'Like';
      cue.dataset.direction = dx < 0 ? 'c1' : 'c3';
      cue.style.opacity = String(fraction);
      behind.style.transform = 'translateY(' + (9 * (1 - fraction)) + 'px) scale(' + (0.96 + 0.04 * fraction) + ')';
    }
    function snapBack() {
      lock(true);
      card.style.transition = reduced.matches ? 'none' : 'transform 280ms cubic-bezier(.2,1.4,.4,1), opacity 220ms ease';
      card.style.transform = ''; card.style.opacity = '';
      cue.style.opacity = '0'; behind.style.transform = '';
      timer = window.setTimeout(function () { resetMotion(); lock(false); }, reduced.matches ? 0 : 280);
    }
    ui.querySelector('.qsw-help').id = helpId;
    card.setAttribute('aria-describedby', helpId);
    var labels = { c1: 'Dislike', c2: 'Skip', c3: 'Like' };
    var current = rows.findIndex(function (r) { return !selected(r); });
    if (current < 0) current = 0;
    function selected(row) { return Object.keys(row.byCode).find(function (code) { return row.byCode[code].checked; }) || null; }
    function show(message) {
      var row = rows[current];
      var chosen = selected(row);
      var count = rows.filter(function (r) { return selected(r); }).length;
      card.querySelector('.qsw-title').textContent = row.title;
      card.setAttribute('aria-label', row.title + '. ' + (chosen ? 'Current answer: ' + labels[chosen] : 'Not yet answered'));
      card.dataset.tone = String(current % 4);
      behind.hidden = current >= rows.length - 1;
      if (!behind.hidden) {
        behind.querySelector('.qsw-title').textContent = rows[current + 1].title;
        behind.dataset.tone = String((current + 1) % 4);
      }
      ui.querySelectorAll('[data-answer]').forEach(function (button) { button.setAttribute('aria-pressed', String(button.dataset.answer === chosen)); });
      status.textContent = (message ? message + ' ' : '') + 'Card ' + (current + 1) + ' of ' + rows.length + ': ' + row.title + '. ' + count + ' of ' + rows.length + ' answered.';
    }
    function choose(code) {
      if (busy || phase !== 'answering') return;
      var row = rows[current];
      if (row.byCode[code].disabled) return;
      lock(true); // Direction and row are fixed until this one transition finishes.
      pointer = null;
      if (!row.byCode[code].checked) row.byCode[code].click();
      if (!row.byCode[code].checked) { lock(false); snapBack(); return; }
      var message = row.title + ': ' + labels[code] + '.';
      var direction = code === 'c1' ? -1 : 1;
      cue.textContent = labels[code]; cue.dataset.direction = code; cue.style.opacity = '1';
      card.style.transition = reduced.matches ? 'none' : 'transform 300ms cubic-bezier(.25,.65,.4,1), opacity 260ms ease';
      card.style.transform = code === 'c2' ? 'translateY(-35px) scale(.96)' : 'translateX(' + (direction * (card.clientWidth + 120)) + 'px) rotate(' + (direction * 18) + 'deg)';
      card.style.opacity = '0';
      behind.style.transform = 'translateY(0) scale(1)';
      timer = window.setTimeout(function () {
        if (phase !== 'answering') return;
        if (rows.every(function (row) { return selected(row); })) { completeDeck(); return; }
        current = rows.findIndex(function (row) { return !selected(row); });
        resetMotion(); show(message); lock(false);
      }, reduced.matches ? 0 : 310);
    }
    ui.querySelectorAll('[data-answer]').forEach(function (button) { button.addEventListener('click', function () { choose(button.dataset.answer); }); });
    card.addEventListener('keydown', function (event) {
      if (event.repeat || event.altKey || event.ctrlKey || event.metaKey) return;
      var code = { ArrowLeft: 'c1', ArrowRight: 'c3', s: 'c2', S: 'c2' }[event.key];
      if (code) { event.preventDefault(); choose(code); }
    });
    card.addEventListener('pointerdown', function (event) {
      if (busy || !event.isPrimary || event.button !== 0) return;
      pointer = { id: event.pointerId, x: event.clientX, y: event.clientY, axis: null };
      card.setPointerCapture(event.pointerId);
    });
    card.addEventListener('pointermove', function (event) {
      if (!pointer || pointer.id !== event.pointerId || busy) return;
      var dx = event.clientX - pointer.x, dy = event.clientY - pointer.y;
      if (!pointer.axis && Math.max(Math.abs(dx), Math.abs(dy)) > 8) pointer.axis = Math.abs(dx) > Math.abs(dy) * 1.2 ? 'x' : 'y';
      if (pointer.axis === 'x') move(dx, dy);
    });
    function endGesture(event) {
      if (!pointer || pointer.id !== event.pointerId || busy) return;
      var dx = event.clientX - pointer.x, axis = pointer.axis;
      pointer = null;
      if (event.type === 'pointerup' && axis === 'x' && Math.abs(dx) >= threshold()) choose(dx < 0 ? 'c1' : 'c3');
      else snapBack();
    }
    card.addEventListener('pointerup', endGesture);
    card.addEventListener('pointercancel', endGesture);
    card.addEventListener('lostpointercapture', function () { if (pointer && !busy) { pointer = null; snapBack(); } });
    native.addEventListener('change', function () { if (!busy && phase === 'answering') show(); });
    continueButton.addEventListener('click', function (event) {
      if (requestPending) { event.preventDefault(); event.stopImmediatePropagation(); return; }
      beginRequest();
    }, true);
    form.addEventListener('submit', function (event) {
      if (submitSeen) { event.preventDefault(); event.stopImmediatePropagation(); return; }
      if (!requestPending) beginRequest();
      submitSeen = true;
    }, true);
    form.addEventListener('invalid', function () {
      recover('Please check the highlighted answers, then use Continue.');
    }, true);
    window.addEventListener('pageshow', function (event) {
      // BFCache re-entry never automatically resends an earlier submission.
      if (event.persisted) recover('Please review your selected answers, then use Continue.');
    });
    // Commit the enhancement only after successful discovery and setup.
    show(); native.before(ui); native.hidden = true; root.dataset.swipeReady = 'true';
    form.classList.add('qsw-form');
    continueButton.classList.add('qsw-continue-hidden');
    // A server validation redisplay with all values restored must not loop-submit.
    if (rows.every(function (row) { return selected(row); })) {
      autoAttempted = true;
      recover('Please review your selected answers, then use Continue.');
    }
    // Remove only observed test-only notices, never validation or other warnings.
    var page = root.closest('.survey-body');
    if (page) {
      page.classList.add('qsw-page');
      page.querySelectorAll('.survey-info, .survey-warning').forEach(function (notice) {
        var text = notice.textContent.replace(/\s+/g, ' ').trim();
        if (text === 'Please login to see additional testing features' ||
            text === "I've detected that your browser has already completed this survey but I'll let you in anyway for testing") {
          notice.classList.add('qsw-test-notice');
          notice.hidden = true;
        }
      });
    }
  });
}());
