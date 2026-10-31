const { chromium } = require('playwright');
const url = process.env.SITE_URL || 'http://127.0.0.1:8765/index.html';
const os = require('os'); const path = require('path');
const shotDir = process.env.SHOT_DIR || path.join(os.tmpdir(), 'uat-shots'); require('fs').mkdirSync(shotDir, {recursive:true});
const sizes = [[1440,900],[390,844],[320,568]];
(async () => {
  const browser = await chromium.launch();
  let fails = 0; const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m); if(!c) fails++;};
  for (const [w,h] of sizes) {
    console.log(`\n--- ${w}x${h}`);
    const ctx = await browser.newContext({viewport:{width:w,height:h}});
    const page = await ctx.newPage();
    const errs=[]; page.on('console',m=>{ if(m.type()==='error') errs.push(m.text()); }); page.on('pageerror',e=>errs.push(e.message));
    page.on('dialog', d=>d.accept());
    await page.goto(url);
    const overflow = async()=> page.evaluate(()=>document.documentElement.scrollWidth > window.innerWidth+1);
    ok(!(await overflow()), 'intro: no horizontal overflow');
    ok(await page.locator('#beginBtn').isDisabled(), 'begin disabled until matter entered');
    await page.fill('#matter','I keep starting projects and abandoning them halfway.');
    await page.click('#beginBtn');
    const names=['Calcination','Dissolution','Separation','Conjunction','Fermentation'];
    let seen=0;
    for (const n of names) {
      const h2 = await page.locator('h2').textContent(); if (h2===n) seen++;
      ok(await page.locator('#layer-reality').count()===0 && await page.locator('#layer-structure').count()===0, `${n}: layers hidden by default`);
      ok(!(await overflow()), `${n}: no horizontal overflow`);
      if (n==='Calcination'){
        await page.click('[data-layer="reality"]'); ok(await page.locator('#layer-reality').isVisible(), 'Reality opens on request');
        await page.click('[data-layer="structure"]'); ok((await page.locator('#layer-structure').textContent()).includes('Lead'), 'Structure shows correspondences');
        await page.click('[data-layer="reality"]'); ok(await page.locator('#layer-reality').count()===0, 'Reality closes again');
        await page.screenshot({path:`${shotDir}/calc_${w}.png`, fullPage:true});
      }
      await page.fill('#answer', `${n} response text for the work.`);
      await page.click('#nextBtn');
    }
    ok((await page.locator('h2').textContent())==='Distillation', 'reached Distillation'); seen++;
    await page.fill('#answer','Finishing matters more than starting something new each week.');
    await page.click('#distillAgain');
    ok((await page.locator('#cycleCount').textContent()).startsWith('Pass 2'), 'recursion: pass 2');
    await page.fill('#answer','Finish before starting.');
    await page.click('#distillAgain');
    ok((await page.locator('#cycleCount').textContent()).startsWith('Pass 3'), 'recursion: pass 3');
    await page.reload();
    ok((await page.locator('h2').textContent())==='Distillation' && (await page.locator('#cycleCount').textContent()).startsWith('Pass 3'), 'persistence: reload resumes at Distillation pass 3');
    await page.screenshot({path:`${shotDir}/distill_${w}.png`, fullPage:true});
    await page.fill('#answer','Finish.');
    await page.click('#distillDone');
    ok((await page.locator('h2').textContent())==='Coagulation', 'distillation exits to Coagulation'); seen++;
    await page.fill('#answer','Ship the half-done journal app this Sunday.');
    await page.click('#nextBtn');
    ok(seen===7, `7/7 stages traversed (${seen})`);
    ok((await page.locator('h2').textContent())==='Apply', 'Apply reached');
    ok((await page.locator('.vessel').textContent()).includes('Finish.'), 'Apply shows final distillate');
    await page.fill('#applyWhen','Sunday 10am'); await page.fill('#applyFirst','Open the repo and list what is left');
    ok(!(await overflow()), 'Apply: no horizontal overflow');
    await page.screenshot({path:`${shotDir}/apply_${w}.png`, fullPage:true});
    const [dl] = await Promise.all([page.waitForEvent('download'), page.click('text=Save as text')]);
    const p = await dl.path(); const txt = require('fs').readFileSync(p,'utf8');
    ok(txt.includes('Distillation (3 passes)') && txt.includes('Sunday 10am'), 'Save as text contains journey + apply');
    await page.click('nav.rail .dot >> nth=0'); ok((await page.locator('h2').textContent())==='Calcination', 'rail navigates to completed stage');
    ok((await page.locator('#soundBtn').getAttribute('aria-pressed'))==='false', 'sound off by default');
    await page.click('#soundBtn'); ok((await page.locator('#soundBtn').getAttribute('aria-pressed'))==='true', 'sound toggles on by user gesture');
    await page.click('#soundBtn');
    await page.click('#resetBtn'); ok(await page.locator('#matter').count()===1 && (await page.inputValue('#matter'))==='', 'Begin again clears state');
    await page.screenshot({path:`${shotDir}/intro_${w}.png`, fullPage:true});
    ok((await page.locator('footer').textContent()).includes('Symbolic and reflective'), 'scope notice visible');
    ok(await page.locator('link[rel=icon]').count()===1 && await page.locator('meta[property="og:image"]').count()===1, 'favicon + social metadata present');
    ok(errs.length===0, 'no console errors / CSP violations '+(errs.length?JSON.stringify(errs):''));
    await ctx.close();
  }
  const ctx = await browser.newContext({reducedMotion:'reduce'}); const page = await ctx.newPage(); await page.goto(url);
  const anim = await page.evaluate(()=>getComputedStyle(document.querySelector('.sigil .spin')).animationName);
  ok(anim==='none','reduced motion disables animation');
  await page.keyboard.press('Tab'); const f = await page.evaluate(()=>document.activeElement.className); ok(f==='skip','first Tab reaches skip link');
  await browser.close();
  console.log(`\nUAT RESULT: ${fails? 'FAIL ('+fails+')':'PASS'}`); process.exit(fails?1:0);
})();
