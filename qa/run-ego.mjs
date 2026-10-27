// QA runner for ego-browser (ego lite). Normally started by `python3 -I scripts/qa.py [--shots 0|1|2]`, which prepends the
// project path (ego-browser forwards neither cwd nor environment variables). By hand on macOS/Linux shells:
//   { echo "const ROOT='/abs/path/to/project', SHOTS=1;"; cat qa/run-ego.mjs; } | ego-browser nodejs
// Writes <project>/qa/report.json. SHOTS=1: one final-state PNG per slide in <project>/qa/shots/NN.png;
// SHOTS=2: additionally every step as NN-k.png (k = 0..steps) for checking the animation step by step.
const fs = await import("node:fs/promises");
const { pathToFileURL } = await import("node:url");
const root = typeof ROOT !== "undefined" ? ROOT : process.env.DECK; if (!root) throw new Error("define ROOT (see header)");
const shots = typeof SHOTS !== "undefined" ? SHOTS : process.env.SHOTS;
const deckDir = typeof DECK !== "undefined" && DECK ? DECK : root + "/deck";   // DECK = an unzipped delivery folder (offline retest)
const qa = await fs.readFile(root + "/qa/deck-qa.js", "utf8");
const task = await taskSpace("deck QA " + root);  // one space per project: two QA runs must not drive the same page
const page = task.page("p1");  // a new task space starts with one managed page labelled p1
await page.cdp("Network.enable", {}); await page.cdp("Network.setCacheDisabled", { cacheDisabled: true });
// VIEWPORTS: the first one gets the full check (every step, entry flash, drill-downs, presenter sync) and the screenshots;
// the others (Kangzhe acceptance sizes, scripts/qa.py --all-viewports) re-run the per-step layout checks only.
const vps = typeof VIEWPORTS !== "undefined" && VIEWPORTS ? VIEWPORTS : [[1920, 1080]];
const probs = []; let N = 0, steps = 0;
for (const [vi, [w, h]] of vps.entries()) {
  await page.cdp("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: false });
  await page.goto(pathToFileURL(deckDir + "/index.html").href + "?v=" + Date.now() + "#/1");  // file URL also right for C:/… paths
  await page.waitForFunction(() => document.documentElement.dataset.kzDeckReady === "true", undefined, { timeout: 20000 });
  await page.waitForTimeout(800);
  await page.evaluate(qa);
  N = await page.evaluate(() => window.DeckQA.count());
  const tag = list => vps.length > 1 ? list.map(p => ({ ...p, viewport: `${w}x${h}` })) : list;
  if (vi === 0) probs.push(...(await page.evaluate(() => window.DeckQA.images())));
  for (let n = 1; n <= N; n++) {
    const r = await page.evaluate((n) => window.DeckQA.slide(n), n); probs.push(...tag(r.problems));
    if (vi > 0) continue;
    steps += r.steps;
    probs.push(...(await page.evaluate((n) => window.DeckQA.flash(n), n)));
    probs.push(...(await page.evaluate((n) => window.DeckQA.drill(n), n)));
  }
  if (vi > 0) continue;
  probs.push(...(await page.evaluate(() => window.DeckQA.presenter())));
  if (shots) {
    await fs.mkdir(root + "/qa/shots", { recursive: true });
    for (let n = 1; n <= N; n++) {
      const nn = String(n).padStart(2, "0");
      const info = await page.evaluate((n) => window.DeckQA.show(n, -1), n);
      await page.screenshot({ path: `${root}/qa/shots/${nn}.png` });
      if (+shots > 1) for (let k = 0; k <= info.steps; k++) {
        await page.evaluate(([n, k]) => window.DeckQA.show(n, k), [n, k]);
        await page.screenshot({ path: `${root}/qa/shots/${nn}-${k}.png` });
      }
    }
  }
}
const rep = await page.evaluate(([p, n, s]) => window.DeckQA.summarize(p, n, s), [probs, N, steps]);
await fs.mkdir(root + "/qa", { recursive: true });
await fs.writeFile(root + "/qa/report.json", JSON.stringify(rep, null, 1));
console.log(JSON.stringify({ slides: rep.slides, steps: rep.steps, summary: rep.summary }));
