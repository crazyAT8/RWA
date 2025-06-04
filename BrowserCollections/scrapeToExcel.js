const { chromium } = require('playwright');
const XLSX = require('xlsx');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    storageState: 'auth.json', // Assumes you're already logged in and this file exists
  });
  const page = await context.newPage();
  
  await page.goto('https://www.bing.com/collections');

  await page.waitForSelector('.collectionItemTitle');

  const collections = await page.$$eval('.collectionItemTitle', elements =>
    elements.map(el => el.textContent.trim())
  );

  console.log('Found collections:', collections);

  // Format data for Excel
  const worksheetData = collections.map((name, index) => ({
    Index: index + 1,
    Name: name,
  }));

  // Create a new workbook
  const workbook = XLSX.utils.book_new();
  const worksheet = XLSX.utils.json_to_sheet(worksheetData);
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Collections');

  // Write to file
  XLSX.writeFile(workbook, 'collections.xlsx');

  console.log('✅ collections.xlsx has been created');

  await browser.close();
})();
