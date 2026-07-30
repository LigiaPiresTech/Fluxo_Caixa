import { test, expect } from "@playwright/test";

test("frontend responds", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/Fluxo de Caixa/i);
});
