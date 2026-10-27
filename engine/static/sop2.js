/* SOP step engine (v2). Nothing plays by itself: → ↓ Space PageDown Enter, a left/up swipe or a trackpad swipe
   advance one motion step; ← ↑ PageUp Backspace go back. Only when a slide's steps are exhausted does the
   upstream html-ppt runtime turn the page; entering a slide backwards lands on its last step.
   Element contract (written by build/v2/kit.py):
     data-s="k"            appears at step k        data-o="k"   disappears at step k
     data-d="ms"           entrance delay within its step
     data-k='{"k":{...}}'  keyframes: x y w h (canvas units) · c (classes) · t (text) · h (html)
     data-count='{"k":[from,to,decimals]}'   data-move='{"k":"pathId"}' (SVG <g class="tok">)
   State is a pure function of the step number, so going back is exact and print shows the final step. */
(function () {
  'use strict';
  const deck = document.querySelector('.deck');
  const nav = document.querySelector('.sop-nav');
  let navCh = null;
  const mq = matchMedia('(prefers-reduced-motion: reduce)');
  const STEP = new WeakMap(), CACHE = new WeakMap();
  const slides = () => [...deck.querySelectorAll(':scope > .slide')];
  const active = () => deck.querySelector(':scope > .slide.is-active');
  const total = s => +s.dataset.steps || 0;
  const json = (el, key) => { let c = CACHE.get(el); if (!c) CACHE.set(el, c = {}); if (!(key in c)) c[key] = JSON.parse(el.getAttribute(key)); return c[key]; };
  const latest = (map, k) => { let best = null; for (const s of Object.keys(map)) if (+s <= k && (best === null || +s > +best)) best = s; return best; };
  const fmt = (v, d) => Number(v).toLocaleString('zh-CN', { minimumFractionDigits: d, maximumFractionDigits: d, useGrouping: false });
  const ease = t => 1 - Math.pow(1 - t, 3);
  const tweens = new WeakMap();
  function tween(el, ms, fn) {
    cancelAnimationFrame(tweens.get(el)); const t0 = performance.now();
    const tick = now => { const p = Math.min(1, (now - t0) / ms); fn(ease(p)); if (p < 1) tweens.set(el, requestAnimationFrame(tick)); };
    tweens.set(el, requestAnimationFrame(tick));
  }

  function apply(slide, k, animate) {
    const n = total(slide); k = Math.max(0, Math.min(n, k));
    const prev = STEP.get(slide) ?? -1; STEP.set(slide, k);
    const fwd = animate && k > prev;
    slide.dataset.step = String(k);
    for (const el of slide.querySelectorAll('[data-s],[data-o]')) {
      const s = el.dataset.s === undefined ? 0 : +el.dataset.s, o = el.dataset.o === undefined ? Infinity : +el.dataset.o;
      const was = el.classList.contains('is-in');
      const on = s <= k && k < o;
      el.style.transitionDelay = fwd && on && !was && el.dataset.d ? el.dataset.d + 'ms' : '';
      el.classList.toggle('is-in', on);
      el.classList.toggle('is-gone', k >= o);
    }
    for (const el of slide.querySelectorAll('[data-k]:not(.notes [data-k])')) {   // notes paragraphs also carry data-k
      const map = json(el, 'data-k'); const keys = Object.keys(map).map(Number).sort((a, b) => a - b);
      if (!el.__base) el.__base = { h: el.innerHTML, text: keys.some(x => 't' in map[x] || 'html' in map[x]), cls: [...new Set(keys.flatMap(x => (map[x].c || '').split(/\s+/).filter(Boolean)))],
        pos: Object.fromEntries(['x', 'y', 'w', 'h'].map(p => [p, el.style.getPropertyValue('--' + p)])) };
      const props = {};
      for (const x of keys) if (x <= k) Object.assign(props, map[x]);
      for (const p of ['x', 'y', 'w', 'h']) { const v = props[p] !== undefined ? String(props[p]) : el.__base.pos[p]; if (v) el.style.setProperty('--' + p, v); else el.style.removeProperty('--' + p); }
      el.classList.remove(...el.__base.cls);
      if (props.c) el.classList.add(...props.c.split(/\s+/).filter(Boolean));
      if (props.html !== undefined) { if (el.innerHTML !== props.html) el.innerHTML = props.html; }
      else if (props.t !== undefined) { if (el.textContent !== props.t) el.textContent = props.t; }
      else if (el.__base.text && el.innerHTML !== el.__base.h) el.innerHTML = el.__base.h;
    }
    for (const el of slide.querySelectorAll('[data-count]')) {
      const map = json(el, 'data-count'), key = latest(map, k);
      if (!el.__base0) el.__base0 = el.textContent;
      if (key === null) { el.textContent = el.__base0; continue; }
      const [a, b, d = 0] = map[key];
      if (fwd && +key === k) tween(el, 900, p => { el.textContent = fmt(a + (b - a) * p, d); }); else el.textContent = fmt(b, d);
    }
    for (const g of slide.querySelectorAll('[data-move]')) {
      const map = json(g, 'data-move'), key = latest(map, k);
      const path = id => document.getElementById(id);
      const kyi = 1 / (parseFloat(getComputedStyle(slide.querySelector('.cv')).getPropertyValue('--ky')) || 1);
      const place = (p, at) => { const pt = p.getPointAtLength(at); g.setAttribute('transform', `translate(${pt.x.toFixed(1)} ${pt.y.toFixed(1)}) scale(1 ${kyi.toFixed(4)})`); };
      if (key === null) { const first = path(map[Object.keys(map).sort((a, b) => a - b)[0]]); place(first, 0); g.classList.remove('is-in'); continue; }
      const p = path(map[key]); const L = p.getTotalLength(); g.classList.add('is-in');
      if (fwd && +key === k) tween(g, 1100, t => place(p, L * t)); else place(p, L);
    }
    if (slide.classList.contains('is-active') && !slide.closest('.overview') && bc) bc.postMessage({ type: 'stepstate', k, n });
  }

  const PREVIEW = new URLSearchParams(location.search).has('preview');
  const frozen = () => mq.matches || PREVIEW || document.body.dataset.preview === '1' || window.__printing;
  // Presenter window (upstream S key) shares this channel: it sends {type:'step'} and shows the step we broadcast.
  let bc = null;
  try { if (!PREVIEW) bc = new BroadcastChannel('html-ppt-presenter-' + location.pathname); } catch (e) { bc = null; }
  const modalOpen = () => !!document.querySelector('dialog[open]');
  const inNav = t => !!(t && t.closest && t.closest('.sop-nav'));
  function finishAll() { for (const s of slides()) apply(s, total(s), false); }

  // Slide entry: forwards → step 0, backwards → last step.
  let lastIndex = -1;
  const bridge = KZHTMLPPT.bind(deck, slide => ({
    enter() {
      const i = slides().indexOf(slide);
      // Jump to the entry state with transitions off, so a slide that was played before does not fade its old
      // state out while the page fades in (seen as a flash of the previous state on revisits).
      slide.classList.add('sop-instant');
      if (frozen()) apply(slide, total(slide), false);
      else apply(slide, i < lastIndex && lastIndex - i === 1 ? total(slide) : 0, false);
      void slide.offsetWidth;
      requestAnimationFrame(() => requestAnimationFrame(() => slide.classList.remove('sop-instant')));
      lastIndex = i;
      navMark(i + 1);
    },
    leave() {}
  }));

  // Navigation: consume a step when possible, otherwise let the upstream runtime turn the page.
  let synthetic = false;
  function upstream(dir) { synthetic = true; document.dispatchEvent(new KeyboardEvent('keydown', { key: dir > 0 ? 'ArrowRight' : 'ArrowLeft', bubbles: true })); synthetic = false; }
  function overviewOpen() { const o = document.querySelector('.overview'); return o && getComputedStyle(o).display !== 'none' && o.classList.contains('open'); }
  function stepBy(dir) {
    const s = active(); if (!s) return false;
    const k = STEP.get(s) ?? 0, n = total(s);
    if (dir > 0 && k < n) { apply(s, k + 1, !frozen()); return true; }
    if (dir < 0 && k > 0) { apply(s, k - 1, !frozen()); return true; }
    return false;
  }
  // O overview: html-ppt clones the slides at load time (all at step 0); show each thumbnail in its final state instead.
  window.addEventListener('keydown', e => {
    if (e.key !== 'o' && e.key !== 'O') return;
    setTimeout(() => { for (const c of document.querySelectorAll('.overview .slide:not([data-final])')) { c.dataset.final = '1'; c.classList.add('sop-instant'); try { apply(c, total(c), false); } catch (err) {} } }, 0);
  });
  const NEXT = new Set(['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter']), PREV = new Set(['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace']);
  window.addEventListener('keydown', e => {
    if (synthetic || e.metaKey || e.ctrlKey || e.altKey || overviewOpen() || modalOpen()) return;
    if (e.target.closest && e.target.closest('input,textarea,select,[contenteditable=true],.sop-nav')) return;
    // html-ppt's T (cycle theme) and A (replay a slide animation) do not apply to this brand deck: swallow them
    if ('tTaA'.includes(e.key) && e.key.length === 1) { e.stopImmediatePropagation(); return; }
    const dir = NEXT.has(e.key) ? 1 : PREV.has(e.key) ? -1 : 0; if (!dir) return;
    if (stepBy(dir)) { e.preventDefault(); e.stopImmediatePropagation(); return; }
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); e.stopImmediatePropagation(); upstream(dir); }
  }, true);

  // Touch: swipe left/up = next, right/down = previous.
  let tx = 0, ty = 0, tt = 0, tracking = false;
  window.addEventListener('touchstart', e => { if (e.touches.length !== 1 || modalOpen() || inNav(e.target)) { tracking = false; return; } tx = e.touches[0].clientX; ty = e.touches[0].clientY; tt = Date.now(); tracking = true; }, { capture: true, passive: true });
  window.addEventListener('touchend', e => {
    if (!tracking) return; tracking = false; const t = e.changedTouches[0]; if (!t || Date.now() - tt > 800) return;
    const dx = t.clientX - tx, dy = t.clientY - ty; if (Math.max(Math.abs(dx), Math.abs(dy)) < 50) return;
    const horiz = Math.abs(dx) >= Math.abs(dy), dir = (horiz ? dx : dy) < 0 ? 1 : -1;
    if (stepBy(dir)) { e.stopImmediatePropagation(); return; }
    if (!horiz) { e.stopImmediatePropagation(); upstream(dir); }
  }, { capture: true, passive: true });

  // Trackpad / wheel swipe: one step per gesture (accumulate, then cool down).
  let acc = 0, cool = 0;
  window.addEventListener('wheel', e => {
    if (overviewOpen() || modalOpen() || inNav(e.target)) return;
    const now = Date.now(); if (now < cool) return;
    acc += Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
    if (Math.abs(acc) < 60) return;
    const dir = acc > 0 ? 1 : -1; acc = 0; cool = now + 650;
    if (!stepBy(dir)) upstream(dir);
  }, { passive: true });

  if (bc) bc.addEventListener('message', e => {
    const d = e.data || {};
    if (d.type === 'step' && (d.dir === 1 || d.dir === -1) && !modalOpen()) { if (!stepBy(d.dir)) upstream(d.dir); }
    else if (d.type === 'hello') { const s = active(); if (s) bc.postMessage({ type: 'stepstate', k: STEP.get(s) ?? 0, n: total(s) }); }
  });

  // "方案原文" drill-down: protocol text travels as JSON next to each slide and is rendered with textContent only.
  let drill = null;
  document.addEventListener('click', e => {
    const btn = e.target.closest && e.target.closest('.src-btn'); if (!btn || !window.KZDrilldown) return;
    const slide = btn.closest('.slide'), blob = slide && slide.querySelector('.src-data'); if (!blob) return;
    const data = JSON.parse(blob.textContent), el = KZDrilldown.element;
    if (!drill) drill = new KZDrilldown.Drilldown({ host: document.body });
    drill.push({ id: btn.dataset.src, title: data.title, render(section) {
      for (const sec of data.sections) {
        const box = el('div', 'src-sec'); box.append(el('h3', null, sec.h));
        for (const t of sec.p) box.append(el('p', t.startsWith('· ') ? 'sub' : null, t));
        section.append(box);
      }
      if (document.body.dataset.srcNote) section.append(el('p', 'src-note', document.body.dataset.srcNote));
    } }, btn);
  });

  // Hover page index (markup from build2.py). Links are plain #/n hashes, so the upstream runtime turns the page and
  // tells the presenter window; keys pressed inside the index never reach the step engine or the runtime.
  function navShow(ch) {
    if (!nav || ch === null) return;
    for (const el of nav.querySelectorAll('.sop-nav-ch')) el.classList.toggle('hot', el.dataset.ch === ch);
    for (const el of nav.querySelectorAll('.sop-nav-pages ol')) el.classList.toggle('hot', el.dataset.ch === ch);
  }
  function navMark(n) {
    if (!nav) return;
    let ch = null;
    for (const a of nav.querySelectorAll('a[data-n]')) {
      const on = +a.dataset.n === n; a.classList.toggle('cur', on);
      if (on) { const ol = a.closest('ol'); ch = a.dataset.ch ?? (ol ? ol.dataset.ch : null); if (ol) a.scrollIntoView({ block: 'nearest' }); }
    }
    for (const el of nav.querySelectorAll('.sop-nav-ch')) el.classList.toggle('in', el.dataset.ch === ch);
    navCh = ch; navShow(ch ?? '0');
  }
  if (nav && (PREVIEW || window.self !== window.top)) nav.remove();
  else if (nav) {
    const tab = nav.querySelector('.sop-nav-tab'), chs = nav.querySelector('.sop-nav-chs');
    let tOpen = 0, tClose = 0, tCh = 0, lastX = 0, rightward = false, openedAt = 0;
    const setOpen = o => { clearTimeout(tOpen); clearTimeout(tClose); if (o && !nav.classList.contains('open')) { navShow(navCh ?? '0'); openedAt = Date.now(); } nav.classList.toggle('open', o); tab.setAttribute('aria-expanded', String(o)); };
    // Hover intent: open after a short dwell, close after a grace period, so passing the edge or overshooting does nothing.
    nav.addEventListener('mouseenter', () => { clearTimeout(tClose); if (!nav.classList.contains('open')) tOpen = setTimeout(() => setOpen(true), 140); });
    nav.addEventListener('mouseleave', () => { clearTimeout(tOpen); clearTimeout(tCh); tClose = setTimeout(() => setOpen(false), 320); });
    tab.addEventListener('click', () => setOpen(!nav.classList.contains('open') || Date.now() - openedAt < 400));
    nav.addEventListener('focusin', () => setOpen(true));
    nav.addEventListener('focusout', e => { if (!inNav(e.relatedTarget)) setOpen(false); });
    // Chapter switch: wait while the pointer is heading right toward the page list, so a diagonal move does not
    // flip the list to whichever chapter it crosses.
    chs.addEventListener('mousemove', e => { rightward = e.clientX - lastX > 1; lastX = e.clientX; });
    for (const el of nav.querySelectorAll('.sop-nav-ch')) {
      el.addEventListener('mouseenter', () => { clearTimeout(tCh); tCh = setTimeout(() => navShow(el.dataset.ch), rightward ? 220 : 60); });
      el.addEventListener('mouseleave', () => clearTimeout(tCh));
      el.addEventListener('focus', () => navShow(el.dataset.ch));
    }
    nav.querySelector('.sop-nav-pages').addEventListener('mouseenter', () => clearTimeout(tCh));
    nav.addEventListener('click', e => { const a = e.target.closest('a[data-n]'); if (a) { a.blur(); setOpen(false); } });
    nav.addEventListener('keydown', e => { e.stopPropagation(); if (e.key === 'Escape') { document.activeElement.blur(); setOpen(false); } });
    document.addEventListener('click', e => { if (!inNav(e.target)) setOpen(false); });
  }

  addEventListener('beforeprint', () => { window.__printing = true; finishAll(); });
  addEventListener('afterprint', () => { window.__printing = false; });
  mq.addEventListener('change', () => { if (mq.matches) finishAll(); });

  // Initial state without transitions.
  document.body.classList.add('no-anim');
  for (const s of slides()) { if (!STEP.has(s)) apply(s, frozen() ? total(s) : 0, false); }
  requestAnimationFrame(() => requestAnimationFrame(() => document.body.classList.remove('no-anim')));
  window.SOP2 = { apply, step: s => STEP.get(s), stepBy, finishAll, bridge };
  document.documentElement.dataset.kzDeckReady = 'true';
})();
