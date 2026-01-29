import { getAuth } from 'firebase/auth';

const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

// Helper to get auth token
async function getAuthToken(): Promise<string | null> {
  try {
    const auth = getAuth();
    if (!auth) return null;
    
    const user = auth.currentUser;
    if (user) {
      return await user.getIdToken();
    }
    return null;
  } catch (error) {
    // Firebase not initialized or configured - this is expected before setup
    return null;
  }
}

// Base API request function
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getAuthToken();
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

// Receipt API
export const receiptAPI = {
  upload: async (imageBase64: string, purchaseDate?: string) => {
    return apiRequest('/api/receipts/upload', {
      method: 'POST',
      body: JSON.stringify({
        image_base64: imageBase64,
        purchase_date: purchaseDate,
      }),
    });
  },

  list: async () => {
    return apiRequest('/api/receipts/');
  },

  get: async (receiptId: string) => {
    return apiRequest(`/api/receipts/${receiptId}`);
  },

  update: async (receiptId: string, data: any) => {
    return apiRequest(`/api/receipts/${receiptId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  delete: async (receiptId: string) => {
    return apiRequest(`/api/receipts/${receiptId}`, {
      method: 'DELETE',
    });
  },
};

// Pantry API
export const pantryAPI = {
  list: async (category?: string) => {
    const params = category ? `?category=${category}` : '';
    return apiRequest(`/api/pantry/${params}`);
  },

  expiring: async (days: number = 3) => {
    return apiRequest(`/api/pantry/expiring?days=${days}`);
  },

  add: async (item: any) => {
    return apiRequest('/api/pantry/', {
      method: 'POST',
      body: JSON.stringify(item),
    });
  },

  update: async (itemId: string, data: any) => {
    return apiRequest(`/api/pantry/${itemId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  consume: async (itemId: string) => {
    return apiRequest(`/api/pantry/${itemId}/consume`, {
      method: 'POST',
    });
  },

  delete: async (itemId: string) => {
    return apiRequest(`/api/pantry/${itemId}`, {
      method: 'DELETE',
    });
  },
};

// Comparison API
export const comparisonAPI = {
  analyze: async (deliveryItem: any, imageBase64?: string) => {
    return apiRequest('/api/compare/analyze', {
      method: 'POST',
      body: JSON.stringify({
        delivery_item: deliveryItem,
        image_base64: imageBase64,
      }),
    });
  },

  history: async () => {
    return apiRequest('/api/compare/history');
  },

  get: async (comparisonId: string) => {
    return apiRequest(`/api/compare/${comparisonId}`);
  },
};

// Analytics API
export const analyticsAPI = {
  spending: async (days: number = 14) => {
    return apiRequest(`/api/analytics/spending?days=${days}`);
  },

  calories: async (days: number = 14) => {
    return apiRequest(`/api/analytics/calories?days=${days}`);
  },

  waste: async () => {
    return apiRequest('/api/analytics/waste');
  },

  savings: async () => {
    return apiRequest('/api/analytics/savings');
  },

  today: async () => {
    return apiRequest('/api/analytics/today');
  },
};

// Notifications API
export const notificationsAPI = {
  list: async (unreadOnly: boolean = false) => {
    const params = unreadOnly ? '?unread_only=true' : '';
    return apiRequest(`/api/notifications/${params}`);
  },

  markRead: async (notificationId: string) => {
    return apiRequest(`/api/notifications/${notificationId}/read`, {
      method: 'PUT',
    });
  },

  registerToken: async (expoPushToken: string) => {
    return apiRequest('/api/notifications/register-token', {
      method: 'POST',
      body: JSON.stringify({ expo_push_token: expoPushToken }),
    });
  },

  sendTest: async () => {
    return apiRequest('/api/notifications/test', {
      method: 'POST',
    });
  },
};

// Auth API
export const authAPI = {
  setupProfile: async (preferences: any) => {
    return apiRequest('/api/auth/setup-profile', {
      method: 'POST',
      body: JSON.stringify(preferences),
    });
  },

  me: async () => {
    return apiRequest('/api/auth/me');
  },

  updateProfile: async (data: any) => {
    return apiRequest('/api/auth/profile', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },
};
