import "@testing-library/jest-dom";
import { afterEach, vi } from "vitest";

// Add type for CustomEventInit if not available
interface CustomEventInit {
  bubbles?: boolean;
  cancelable?: boolean;
  composed?: boolean;
  detail?: any;
}

// Mock Chart.js
vi.mock("chart.js", () => ({
  Chart: {
    register: vi.fn(),
  },
  CategoryScale: vi.fn(),
  LinearScale: vi.fn(),
  PointElement: vi.fn(),
  LineElement: vi.fn(),
  Title: vi.fn(),
  Tooltip: vi.fn(),
  Legend: vi.fn(),
}));

// Mock vue-chartjs
vi.mock("vue-chartjs", () => ({
  Line: {
    name: "Line",
    render: () => null, // Return empty render
  },
}));

// Mock chartjs-plugin-annotation
vi.mock("chartjs-plugin-annotation", () => ({
  default: vi.fn(),
}));

// Mock fetch globally
global.fetch = vi.fn();

// Mock CustomEvent if not available in test environment
if (typeof CustomEvent === "undefined") {
  global.CustomEvent = class CustomEvent extends Event {
    constructor(type: string, options?: CustomEventInit) {
      super(type, options);
    }
  } as typeof CustomEvent;
}

// Clean up after each test
afterEach(() => {
  vi.clearAllMocks();
});
