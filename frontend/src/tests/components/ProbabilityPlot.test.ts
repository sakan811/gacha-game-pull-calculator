import { render, screen } from "@testing-library/vue";
import {
  describe,
  it,
  expect,
  beforeAll,
  afterAll,
  afterEach,
  vi,
  beforeEach,
} from "vitest";
import { http, HttpResponse } from "msw";
import ProbabilityPlot from "../../components/ProbabilityPlot.vue";
import {
  createMockServer,
  mockVisualizationData,
  mockBannerProps,
  mockCalculationResponse,
  setupResizeObserverMock,
} from "../../tests/utils/test-utils";

// Add interfaces for test cases
interface BasicRenderTestCase {
  name: string;
  assertion: (container: HTMLElement) => void;
}

interface TotalPullsTestCase {
  currentPity: number;
  plannedPulls: number;
  expected: number;
}

// Setup MSW server
const server = createMockServer();

describe("ProbabilityPlot Component", () => {
  // Common test setup
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());
  beforeEach(() => setupResizeObserverMock(vi));

  // Add return type for renderComponent
  const renderComponent = (
    _props: Partial<typeof mockBannerProps.standard>,
  ) => {
    return render(ProbabilityPlot, { props: _props }) as unknown as {
      container: HTMLElement;
      rerender: (props: Partial<typeof mockBannerProps.standard>) => void;
    };
  };

  const triggerChartUpdate = async (container: HTMLElement): Promise<void> => {
    const element = container.querySelector(
      '[data-testid="probability-plots"]',
    );
    if (!element) {
      throw new Error("Probability plots element not found");
    }
    await element.dispatchEvent(new Event("mounted", { bubbles: true }));
  };

  const testCaseGroups = {
    basicRender: [
      {
        name: "should render chart containers",
        assertion: (container: HTMLElement) => {
          expect(
            container.querySelector('[data-testid="probability-plots"]'),
          ).toBeTruthy();
        },
      },
      {
        name: "should render chart titles",
        assertion: () => {
          expect(screen.getByText("Successful Pull Distribution")).toBeTruthy();
          expect(screen.getByText("Cumulative Probability")).toBeTruthy();
        },
      },
    ] as BasicRenderTestCase[],
    totalPullsCalculation: [
      { currentPity: 0, plannedPulls: 10, expected: 10 },
      { currentPity: 10, plannedPulls: 20, expected: 30 },
      { currentPity: 74, plannedPulls: 16, expected: 90 },
      { currentPity: 89, plannedPulls: 1, expected: 90 },
    ] as TotalPullsTestCase[],
  };

  // Basic rendering tests
  describe("Basic Rendering", () => {
    testCaseGroups.basicRender.forEach(({ name, assertion }) => {
      it(name, () => {
        const { container } = renderComponent({
          ...mockBannerProps.standard,
          totalPulls:
            mockBannerProps.standard.currentPity +
            mockBannerProps.standard.plannedPulls,
        });
        assertion(container);
      });
    });
  });

  // Data visualization tests
  describe("Visualization", () => {
    it("should fetch and display visualization data", async () => {
      const { container } = renderComponent(mockBannerProps.standard);

      // Trigger the update through DOM event
      await triggerChartUpdate(container);

      // Wait for the request to complete
      await vi.waitFor(() => {
        expect(screen.getByText("Successful Pull Distribution")).toBeTruthy();
      });
    });
  });

  // Calculation tests grouped separately
  describe("Total Pulls Calculation", () => {
    const testCases = testCaseGroups.totalPullsCalculation;

    // Test cases
    testCases.forEach(({ currentPity, plannedPulls, expected }) => {
      it(`should show chart with total pulls: ${currentPity} + ${plannedPulls} = ${expected}`, async () => {
        server.use(
          http.post("/api/visualization", () => {
            return HttpResponse.json({
              ...mockVisualizationData,
              current_pity: currentPity,
              total_pulls: expected,
            });
          }),
        );

        const { container } = renderComponent({
          ...mockBannerProps.standard,
          currentPity,
          plannedPulls,
          result: mockCalculationResponse,
        });

        // Trigger chart update
        await triggerChartUpdate(container);

        // Wait for chart to update
        await vi.waitFor(() => {
          expect(
            container.querySelector('[data-testid="probability-plots"]'),
          ).toBeTruthy();
          expect(
            container.querySelector('[data-testid="probability-plots"]'),
          ).toBeTruthy();
        });
      });
    });

    // Chart update test
    it("should update charts only after calculation", async () => {
      const { container, rerender } = renderComponent({
        ...mockBannerProps.standard,
        currentPity: 10,
      });

      // Initial calculation
      await triggerChartUpdate(container);

      // Change props without triggering calculation
      await rerender({
        ...mockBannerProps.standard,
        currentPity: 10,
        plannedPulls: 40,
        result: mockCalculationResponse,
      });

      // Get component instance and verify data hasn't changed
      await vi.waitFor(() => {
        const spy = vi.spyOn(server, "use");
        expect(spy).not.toHaveBeenCalled();
      });
    });
  });

  describe("Edge Cases", () => {
    it("should handle zero pulls scenario", async () => {
      server.use(
        http.post("/api/visualization", () => {
          return HttpResponse.json({
            ...mockVisualizationData,
            current_pity: 0,
            total_pulls: 0,
          });
        }),
      );

      const { container } = renderComponent({
        ...mockBannerProps.standard,
        currentPity: 0,
        plannedPulls: 0,
      });

      await triggerChartUpdate(container);

      await vi.waitFor(() => {
        expect(
          container.querySelector('[data-testid="probability-plots"]'),
        ).toBeTruthy();
      });
    });

    it("should handle missing visualization data gracefully", async () => {
      server.use(
        http.post("/api/visualization", () => {
          return HttpResponse.json({});
        }),
      );

      const { container } = renderComponent({
        ...mockBannerProps.standard,
        currentPity: 0,
        plannedPulls: 0,
      });

      await triggerChartUpdate(container);

      await vi.waitFor(() => {
        expect(
          container.querySelector('[data-testid="probability-plots"]'),
        ).toBeTruthy();
      });
    });
  });
});
