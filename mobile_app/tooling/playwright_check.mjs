import { chromium } from 'playwright';

const url = process.env.APP_URL || 'http://127.0.0.1:9000';

const main = async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'load' });
  // Дадим Flutter Web время дорисовать первый кадр
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2500);
  await page.screenshot({ path: 'tooling/screenshot.png', fullPage: true });
  await browser.close();
  console.log('Screenshot saved to tooling/screenshot.png');
};

main().catch((e) => {
  console.error(e);
  process.exit(1);
});

