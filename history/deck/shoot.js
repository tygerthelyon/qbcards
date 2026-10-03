// shoot.js -- screenshot previews/html/*.html at phone width (390px) into previews/png/
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, 'previews', 'html'), out = path.join(__dirname, 'previews', 'png');
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort()) {
    await p.goto('file://' + path.join(dir, f));
    await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(out, f.replace('.html', '.png')), fullPage: true });
  }
  await b.close();
})();
