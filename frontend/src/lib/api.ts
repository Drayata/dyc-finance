/**
 * MarketPulse AI — API Client
 * Centralized API client with error handling and auth token management.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiOptions {
  method?: string;
  body?: any;
  headers?: Record<string, string>;
  token?: string;
}

class ApiError extends Error {
  status: number;
  requestId?: string;

  constructor(message: string, status: number, requestId?: string) {
    super(message);
    this.status = status;
    this.requestId = requestId;
  }
}

async function apiRequest<T>(endpoint: string, options: ApiOptions = {}): Promise<T> {
  const { method = 'GET', body, headers = {}, token } = options;

  const requestHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
    ...headers,
  };

  if (token) {
    requestHeaders['Authorization'] = `Bearer ${token}`;
  } else if (typeof window !== 'undefined') {
    const savedToken = localStorage.getItem('mp_access_token');
    if (savedToken) {
      requestHeaders['Authorization'] = `Bearer ${savedToken}`;
    }
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    method,
    headers: requestHeaders,
    body: body ? JSON.stringify(body) : undefined,
  });

  const requestId = response.headers.get('X-Request-ID') || undefined;

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new ApiError(errorData.detail || 'Request failed', response.status, requestId);
  }

  return response.json();
}

// --- Auth Endpoints ---
export const auth = {
  register: (data: { email: string; username: string; password: string; full_name?: string }) =>
    apiRequest('/auth/register', { method: 'POST', body: data }),
  login: (data: { email: string; password: string }) =>
    apiRequest('/auth/login', { method: 'POST', body: data }),
  refresh: (refreshToken: string) =>
    apiRequest('/auth/refresh', { method: 'POST', body: { refresh_token: refreshToken } }),
  me: () => apiRequest('/auth/me'),
  updateProfile: (data: any) => apiRequest('/auth/me', { method: 'PATCH', body: data }),
};

// --- Market Endpoints ---
export const markets = {
  overview: () => apiRequest('/api/markets/overview'),
  movers: (assetType?: string) =>
    apiRequest(`/api/markets/movers${assetType ? `?asset_type=${assetType}` : ''}`),
  listAssets: (params: Record<string, any> = {}) => {
    const query = new URLSearchParams(params).toString();
    return apiRequest(`/api/assets?${query}`);
  },
  getAsset: (symbol: string) => apiRequest(`/api/assets/${symbol}`),
  getCandles: (symbol: string, interval = '1d', limit = 90) =>
    apiRequest(`/api/assets/${symbol}/candles?interval=${interval}&limit=${limit}`),
  getIndicators: (symbol: string, interval = '1d') =>
    apiRequest(`/api/assets/${symbol}/indicators?interval=${interval}`),
  getFundamentals: (symbol: string) => apiRequest(`/api/assets/${symbol}/fundamentals`),
  getOnchain: (symbol: string) => apiRequest(`/api/assets/${symbol}/onchain`),
};

// --- News Endpoints ---
export const news = {
  list: (params: Record<string, any> = {}) => {
    const query = new URLSearchParams(params).toString();
    return apiRequest(`/api/news?${query}`);
  },
  highImpact: (limit = 10) => apiRequest(`/api/news/high-impact?limit=${limit}`),
  forAsset: (symbol: string, limit = 20) => apiRequest(`/api/news/asset/${symbol}?limit=${limit}`),
  categories: () => apiRequest('/api/news/categories'),
};

// --- Signal Endpoints ---
export const signals = {
  list: (params: Record<string, any> = {}) => {
    const query = new URLSearchParams(params).toString();
    return apiRequest(`/api/signals?${query}`);
  },
  forAsset: (symbol: string) => apiRequest(`/api/signals/asset/${symbol}`),
  strongestBullish: (limit = 5) => apiRequest(`/api/signals/strongest-bullish?limit=${limit}`),
  strongestBearish: (limit = 5) => apiRequest(`/api/signals/strongest-bearish?limit=${limit}`),
};

// --- Watchlist Endpoints ---
export const watchlists = {
  list: () => apiRequest('/api/watchlists'),
  create: (data: { name: string; description?: string }) =>
    apiRequest('/api/watchlists', { method: 'POST', body: data }),
  addItem: (watchlistId: string, data: { asset_id: string }) =>
    apiRequest(`/api/watchlists/${watchlistId}/items`, { method: 'POST', body: data }),
  removeItem: (watchlistId: string, itemId: string) =>
    apiRequest(`/api/watchlists/${watchlistId}/items/${itemId}`, { method: 'DELETE' }),
  delete: (watchlistId: string) =>
    apiRequest(`/api/watchlists/${watchlistId}`, { method: 'DELETE' }),
};

// --- Health ---
export const system = {
  health: () => apiRequest('/health'),
};

export { ApiError };
export default { auth, markets, news, signals, watchlists, system };
