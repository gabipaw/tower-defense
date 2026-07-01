// Testy e2e gry Tower Defense. Korzystamy z hooka window.TD wystawionego
// przez grę, aby deterministycznie testować logikę (bez klikania po canvasie).
const { test, expect } = require("@playwright/test");

const state = (page) => page.evaluate(() => window.TD.state());

test.beforeEach(async ({ page }) => {
  await page.goto("/");
  await page.waitForFunction(() => !!window.TD);
});

test("HUD startowy: 120 złota, 15 żyć, fala 0", async ({ page }) => {
  await expect(page.getByTestId("money")).toHaveText("120");
  await expect(page.getByTestId("lives")).toHaveText("15");
  await expect(page.getByTestId("wave")).toHaveText("0");
});

test("Start fali zwiększa numer fali i aktywuje grę", async ({ page }) => {
  await page.getByTestId("start").click();
  const s = await state(page);
  expect(s.wave).toBe(1);
  expect(s.phase).toBe("active");
  await expect(page.getByTestId("start")).toBeDisabled();
});

test("wrogowie pojawiają się po starcie fali", async ({ page }) => {
  await page.evaluate(() => window.TD.startWave());
  await expect.poll(async () => (await state(page)).enemies, { timeout: 5000 }).toBeGreaterThan(0);
});

test("postawienie wieży na trawie kosztuje 50 złota", async ({ page }) => {
  const ok = await page.evaluate(() => window.TD.tryPlace(0, 0)); // pole trawy
  expect(ok).toBe(true);
  const s = await state(page);
  expect(s.towers).toBe(1);
  expect(s.money).toBe(70);
  await expect(page.getByTestId("money")).toHaveText("70");
});

test("nie można budować na ścieżce", async ({ page }) => {
  const ok = await page.evaluate(() => window.TD.tryPlace(2, 1)); // kafel ścieżki
  expect(ok).toBe(false);
  const s = await state(page);
  expect(s.towers).toBe(0);
  expect(s.money).toBe(120);
});

test("brak złota blokuje budowę", async ({ page }) => {
  await page.evaluate(() => { window.TD.tryPlace(0, 0); window.TD.tryPlace(0, 2); }); // 120 -> 20
  const ok = await page.evaluate(() => window.TD.tryPlace(4, 0)); // koszt 50 > 20
  expect(ok).toBe(false);
  expect((await state(page)).money).toBe(20);
});

test("Nowa gra przywraca stan początkowy", async ({ page }) => {
  await page.evaluate(() => { window.TD.tryPlace(0, 0); window.TD.startWave(); });
  await page.evaluate(() => window.TD.reset());
  const s = await state(page);
  expect(s).toMatchObject({ money: 120, lives: 15, wave: 0, phase: "idle", towers: 0 });
});
