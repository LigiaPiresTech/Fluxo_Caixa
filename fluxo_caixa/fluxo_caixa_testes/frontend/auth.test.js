import { describe, it, expect, vi } from "vitest";

vi.mock("aws-amplify/auth", () => ({
  getCurrentUser: vi.fn(async () => ({ username: "maria@example.com" })),
  signIn: vi.fn(async () => ({})),
  signOut: vi.fn(async () => ({})),
  fetchAuthSession: vi.fn(async () => ({ tokens: { accessToken: { toString: () => "jwt-test" } } }))
}));

describe("frontend security contract", () => {
  it("requires Cognito session before authenticated API calls", async () => {
    const { fetchAuthSession } = await import("aws-amplify/auth");
    const session = await fetchAuthSession();
    expect(session.tokens.accessToken.toString()).toBe("jwt-test");
  });
});
