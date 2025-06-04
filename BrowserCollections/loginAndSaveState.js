const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await chromium.newContext();
  const page = await context.newPage();
  
  await page.goto('https://www.bing.com/collections');
  console.log('👉 Please log in manually...');
  await page.waitForTimeout(30000); // give yourself 30 seconds

  await context.storageState({ path: 'auth.json' });
  await browser.close();
})();
