import { render } from "@testing-library/vue";
import { describe, it } from "vitest";
import App from "../../App.vue";
import {
  setupBannerTest,
  updateBannerInputs,
  assertProbabilityResults,
} from "../utils/test-utils";

describe("Zenless Zone Zero Banner Calculations", () => {
  setupBannerTest();

  beforeEach(() => {
    render(App);
  });

  it("should calculate standard banner probabilities", async () => {
    await updateBannerInputs("zenless", "standard", "10");
    await assertProbabilityResults({
      total: "15.50%",
      character: "7.75%",
      equipment: "7.75%",
    });
  });

  it("should calculate limited banner probabilities", async () => {
    await updateBannerInputs("zenless", "limited", "10");
    await assertProbabilityResults({
      total: "15.50%",
      character: "10.00%",
    });
  });

  it("should calculate W-Engine banner probabilities", async () => {
    await updateBannerInputs("zenless", "w_engine", "10");
    await assertProbabilityResults({
      total: "15.50%",
      character: "10.00%",
    });
  });

  it("should calculate Bangboo banner probabilities", async () => {
    await updateBannerInputs("zenless", "bangboo", "10");
    await assertProbabilityResults({
      total: "15.50%",
      character: "10.00%",
    });
  });

  it("should handle invalid banner type gracefully", async () => {
    await updateBannerInputs("zenless", "invalid_banner", "10");
    await assertProbabilityResults({
      total: "0.00%",
      character: "0.00%",
      equipment: "0.00%",
    });
  });
});
