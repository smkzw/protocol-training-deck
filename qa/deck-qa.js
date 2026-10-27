/* In-page QA for decks built by engine/build.py. Inject this file into the opened deck/index.html with ANY browser
   automation (ego-browser page.evaluate via scripts/qa.py, or paste into the devtools console), then:
     await DeckQA.all()          → { slides, steps, problems: [...], summary }   (walks every slide × every step)
     await DeckQA.slide(n)       → same checks for one slide (use in a loop if your tool limits one call's duration)
     await DeckQA.show(n, k)     → put slide n (1-based) at step k (-1 = last step), animations off, for screenshots
     await DeckQA.flash(n)       → enter slide n from slide n-1 with a key press and report ENTRY_FLASH if any later-step
                                   element is visible during the first frames (slide n is pre-set to its last step first)
   Problem codes (the summary must end up empty):
     LAYOUT_OUTSIDE   element sticks out of the 1168×564 canvas
     LAYOUT_OVERFLOW  text does not fit its box (scroll size > box size)
     TEXT_COLLISION   visible text of two different boxes overlaps (a later box with class "cover" — alert / case_card — is a
                      deliberate cover and is skipped; any other overlap is reported, opaque or not)
     NARR_OVERFLOW    a narration caption does not fit its card
     TITLE_LOGO       page title runs into the logo
     IMG_BROKEN       image failed to load
     NOTES_MISMATCH   speaker script paragraphs ≠ page steps
     NO_NOTES         page has no speaker script
     ENTRY_FLASH      entering a slide briefly shows a later step (the "上一状态闪现" bug)
     LOGO             not exactly one logo on the page, or it failed to load / is distorted (Kangzhe CORE-02)
     FOOTER           footer is not exactly two slots, or the page number is not "n / total" (Kangzhe CORE-04)
     LEAD_OVERFLOW    the one-line lead sentence is cut off (no ellipsis allowed, Kangzhe TYPE-03)
     FONT_FLOOR       visible text below 12 logical px (this skill's floor; computed size ÷ --kz-un)
     DRILL            方案原文 drill-down does not open / is empty / does not close / lets keys move the slide  — DeckQA.drill(n)
     PRESENTER_SYNC   the S presenter window contract fails on the BroadcastChannel (hello, step, page turn) — DeckQA.presenter()
   Decision diamonds (.dia) are measured against their inscribed square, so their rotated box raises no false alarm. */
(function () {
  'use strict';
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const slides = () => [...document.querySelectorAll('.deck > .slide')];
  const vis = (el, stop) => { let o = 1; for (let e = el; e && e !== stop; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return 0; o *= +cs.opacity; } return o; };
  const label = el => (el.textContent || el.getAttribute('class') || '').trim().replace(/\s+/g, ' ').slice(0, 24);
  const FLOOR = 12;   // smallest logical px allowed by this skill (typography.md); Kangzhe's own floor is 16, see brand-compliance.md
  const kzun = el => parseFloat(getComputedStyle(el).getPropertyValue('--kz-un')) || 1;

  async function show(n, k) {
    const s = slides()[n - 1]; if (!s) throw new Error('no slide ' + n);
    document.body.classList.add('no-anim');
    location.hash = '#/' + n; await wait(150);
    const steps = +s.dataset.steps || 0;
    if (window.SOP2) window.SOP2.apply(s, k < 0 ? steps : Math.min(k, steps), false);
    await wait(60);
    return { n, steps, title: s.dataset.title, scene: s.dataset.scene || 'hero' };
  }

  function checkStep(s, n, k, out, seen) {
    const cv = s.querySelector('.cv'); if (!cv) return;
    const box = cv.getBoundingClientRect();
    const add = (code, msg) => { const key = code + msg.replace(/\d+px/g, ''); if (!seen.has(key)) { seen.add(key); out.push({ slide: n, step: k, scene: s.dataset.scene, code, msg }); } };
    for (const el of cv.querySelectorAll('.ab')) {
      if (vis(el, s) < 0.05) continue;
      const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
      if (r.left < box.left - 6 || r.right > box.right + 6 || r.top < box.top - 30 || r.bottom > box.bottom + 6) add('LAYOUT_OUTSIDE', `[${label(el)}]`);
      if (el.matches('svg,.wires,.narr')) continue;
      if (el.matches('.dia')) {   // rotated square: the label must fit the inscribed square (≈70% of the box)
        const sp = el.querySelector('span');
        if (sp && (sp.offsetHeight > el.clientHeight * 0.72 + 2 || sp.scrollWidth > el.clientWidth * 0.86 + 2)) add('LAYOUT_OVERFLOW', `[${label(el)}] diamond label too big`);
        continue;
      }
      if (el.scrollHeight > el.clientHeight + 3 && el.clientHeight > 0) add('LAYOUT_OVERFLOW', `[${label(el)}] y+${el.scrollHeight - el.clientHeight}px`);
      if (el.scrollWidth > el.clientWidth + 3 && el.clientWidth > 0) add('LAYOUT_OVERFLOW', `[${label(el)}] x+${el.scrollWidth - el.clientWidth}px`);
    }
    // text collisions between different boxes
    const runs = [], w = document.createTreeWalker(cv, NodeFilter.SHOW_TEXT);
    for (let t = w.nextNode(); t; t = w.nextNode()) {
      if (!t.textContent.trim()) continue;
      const el = t.parentElement, own = el.closest('.ab');
      if (!own || vis(el, s) < 0.5) continue;
      if (!el.closest('svg')) { const px = parseFloat(getComputedStyle(el).fontSize) / kzun(s); if (px < FLOOR - 0.5) add('FONT_FLOOR', `[${t.textContent.trim().slice(0, 16)}] ${px.toFixed(1)} < ${FLOOR}`); }
      const rg = document.createRange(); rg.selectNodeContents(t);
      for (const b of rg.getClientRects()) if (b.width > 4 && b.height > 4) runs.push({ own, b, t: t.textContent.trim().slice(0, 16) });
    }
    for (let i = 0; i < runs.length; i++) for (let j = i + 1; j < runs.length; j++) {
      const a = runs[i], c = runs[j];
      if (a.own === c.own || a.own.contains(c.own) || c.own.contains(a.own) || c.own.closest('.cover')) continue;
      const ix = Math.min(a.b.right, c.b.right) - Math.max(a.b.left, c.b.left), iy = Math.min(a.b.bottom, c.b.bottom) - Math.max(a.b.top, c.b.top);
      if (ix > 0 && iy > 0 && ix * iy / Math.min(a.b.width * a.b.height, c.b.width * c.b.height) > 0.25) add('TEXT_COLLISION', `「${a.t}」×「${c.t}」`);
    }
  }

  function images() {
    return [...document.images].filter(img => !img.complete || !img.naturalWidth).map(img => ({ slide: 0, step: 0, code: 'IMG_BROKEN', msg: img.getAttribute('src') }));
  }

  // One slide, every step. Runners with a per-call time limit loop over slide() instead of calling all().
  async function slide(n) {
    const out = [], s = slides()[n - 1], info = await show(n, 0), seen = new Set();
    const body = s.querySelector('.kz-body-title');
    if (body) {
      const t = body.getBoundingClientRect(), lg = s.querySelector('.kz-logo').getBoundingClientRect();
      if (t.right > lg.left - 4) out.push({ slide: n, step: 0, scene: s.dataset.scene, code: 'TITLE_LOGO', msg: `${Math.round(t.right - lg.left + 4)}px` });
      const notes = s.querySelectorAll('aside.notes p[data-k]');
      const paras = [...notes].filter(p => p.dataset.k !== '0').length;
      if (!notes.length) out.push({ slide: n, step: 0, scene: s.dataset.scene, code: 'NO_NOTES', msg: '' });
      else if (paras !== info.steps) out.push({ slide: n, step: 0, scene: s.dataset.scene, code: 'NOTES_MISMATCH', msg: `${paras} paragraphs / ${info.steps} steps` });
    }
    const put = (code, msg) => out.push({ slide: n, step: 0, scene: s.dataset.scene || 'hero', code, msg });
    const logos = [...s.querySelectorAll('img')].filter(i => /logo/i.test(i.getAttribute('src') || '') && vis(i, s) > 0.05);
    if (logos.length !== 1) put('LOGO', `${logos.length} logos on the page (exactly one)`);
    for (const i of logos) { const r = i.getBoundingClientRect(), want = i.naturalWidth / i.naturalHeight;
      if (!i.naturalWidth) put('LOGO', 'logo image did not load');
      else if (!/contain|scale-down/.test(getComputedStyle(i).objectFit) && Math.abs(r.width / r.height - want) / want > 0.03) put('LOGO', `logo distorted (${(r.width / r.height).toFixed(2)} vs ${want.toFixed(2)})`); }
    const foot = s.querySelector('.kz-foot');
    if (body) {
      const slots = foot ? [...foot.children] : [], num = s.querySelector('.kz-page-number');
      if (slots.length !== 2 || !slots[0].textContent.trim()) put('FOOTER', `footer must have exactly two slots (found ${slots.length})`);
      if (!num || num.textContent.trim() !== `${n} / ${slides().length}`) put('FOOTER', `page number「${num ? num.textContent.trim() : ''}」≠「${n} / ${slides().length}」`);
      const lead = s.querySelector('.lead-tx');
      if (lead && lead.scrollWidth > lead.clientWidth + 1) put('LEAD_OVERFLOW', `lead is cut off by ${lead.scrollWidth - lead.clientWidth}px — shorten it`);
    }
    for (let k = 0; k <= info.steps; k++) {
      window.SOP2.apply(s, k, false); await wait(30);
      checkStep(s, n, k, out, seen);
    }
    [...s.querySelectorAll('.narr > .ne')].forEach((e, i) => {
      const tx = e.querySelector('.tx'), cs = getComputedStyle(e);
      const room = e.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
      if (tx.scrollHeight > room + 1) out.push({ slide: n, step: i + 1, scene: s.dataset.scene, code: 'NARR_OVERFLOW', msg: `${tx.scrollHeight} > ${Math.round(room)}` });
    });
    window.SOP2.apply(s, info.steps, false);
    return { steps: info.steps + 1, problems: out };
  }

  // A real flash reproduces every time; a one-off (busy machine, another tab of the same deck) does not. Report only repeats.
  async function flash(n) {
    const first = await flashOnce(n);
    return first.length ? await flashOnce(n) : first;
  }

  async function flashOnce(n) {
    const ss = slides(), s = ss[n - 1], prev = ss[n - 2];
    if (!s || !prev || !(+s.dataset.steps)) return [];
    document.body.classList.remove('no-anim');
    // wait for the runtime to really switch (a fixed delay is too short on big decks and makes the check flaky)
    const goto = async (el, h) => { location.hash = h; for (let t = 0; t < 60 && !el.classList.contains('is-active'); t++) await wait(50); await wait(120); };
    await goto(s, '#/' + n);
    window.SOP2.apply(s, +s.dataset.steps, false);                       // as if the slide had been played before
    await goto(prev, '#/' + (n - 1));
    window.SOP2.apply(prev, +prev.dataset.steps || 0, false); await wait(50);
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
    let worst = 0;
    for (let i = 0; i < 8; i++) {
      await new Promise(r => requestAnimationFrame(r));
      const later = [...s.querySelectorAll('[data-s]')].filter(e => +e.dataset.s > 0 && e.dataset.fx !== 'wipe' && !e.closest('svg') && vis(e, s) > 0.05)  // wipe = clip-path reveal (opacity stays 1);
      worst = Math.max(worst, later.length);
    }
    document.body.classList.add('no-anim');
    return worst ? [{ slide: n, step: 0, scene: s.dataset.scene, code: 'ENTRY_FLASH', msg: `${worst} later-step elements visible on entry` }] : [];
  }

  function summarize(problems, nSlides, nSteps) {
    const summary = {};
    for (const p of problems) summary[p.code] = (summary[p.code] || 0) + 1;
    return { slides: nSlides, steps: nSteps, problems, summary };
  }

  // 方案原文 drill-down: opens, keeps keys away from the slide, closes.
  async function drill(n) {
    const s = slides()[n - 1], btn = s && s.querySelector('.src-btn'); if (!btn) return [];
    const bad = msg => [{ slide: n, step: -1, scene: s.dataset.scene, code: 'DRILL', msg }];
    await show(n, 0); btn.click(); await wait(400);
    const dlg = document.querySelector('dialog[open]'); if (!dlg) return bad('方案原文 button did not open the drill-down');
    if (!dlg.textContent.trim()) return bad('drill-down is empty');
    const before = s.dataset.step;
    dlg.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true })); await wait(100);
    const leaked = s.dataset.step !== before;
    const close = [...dlg.querySelectorAll('button')].find(b => /关闭|close/i.test(b.textContent)); if (close) close.click(); else dlg.close();
    await wait(400);
    if (document.querySelector('dialog[open]')) return bad('drill-down did not close');
    return leaked ? bad('a key pressed inside the drill-down moved the slide') : [];
  }

  // Presenter window contract (S key): impersonate it on the shared BroadcastChannel and check hello / step / page turn.
  async function presenter() {
    const ss = slides(), n = ss.findIndex(s => (+s.dataset.steps || 0) >= 2 && s.querySelector('.kz-body-title')) + 1;
    if (!n || n >= ss.length) return [];
    const fail = msg => [{ slide: n, step: 0, scene: ss[n - 1].dataset.scene, code: 'PRESENTER_SYNC', msg }];
    let bc; try { bc = new BroadcastChannel('html-ppt-presenter-' + location.pathname); } catch (e) { return fail('BroadcastChannel unavailable'); }
    const got = []; bc.onmessage = e => got.push(e.data || {});
    const last = type => got.filter(m => m.type === type).pop();
    try {
      document.body.classList.add('no-anim'); location.hash = '#/' + n; await wait(300); window.SOP2.apply(ss[n - 1], 0, false);
      got.length = 0; bc.postMessage({ type: 'hello' }); await wait(250);
      const h = last('stepstate'); if (!h || h.k !== 0 || h.n !== +ss[n - 1].dataset.steps) return fail(`hello → stepstate ${JSON.stringify(h)}`);
      got.length = 0; bc.postMessage({ type: 'step', dir: 1 }); await wait(250);
      const st = last('stepstate'); if (!st || st.k !== 1) return fail(`step → stepstate ${JSON.stringify(st)}`);
      window.SOP2.apply(ss[n - 1], +ss[n - 1].dataset.steps, false);
      got.length = 0; bc.postMessage({ type: 'step', dir: 1 }); await wait(400);
      const go = last('go'); if (!go || go.idx !== n) return fail(`step past the last step → go ${JSON.stringify(go)} (expected idx ${n})`);
      if (!ss[n].classList.contains('is-active')) return fail('page did not turn after the last step');
      return [];
    } finally { bc.close(); }
  }

  async function all() {
    const out = images(); let steps = 0;
    for (let n = 1; n <= slides().length; n++) { const r = await slide(n); steps += r.steps; out.push(...r.problems, ...(await flash(n)), ...(await drill(n))); }
    out.push(...(await presenter()));
    return summarize(out, slides().length, steps);
  }

  window.DeckQA = { all, show, slide, flash, drill, presenter, images, summarize, count: () => slides().length };
})();
