import os
from typing import Any, Dict, Optional

import requests

API_URL = os.getenv('VITE_API_URL', 'http://localhost:8000')


class AuthService:
    def __init__(self, base_url: str = API_URL) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

export const authService = {
  // 1. Updated Signup to direct to the specific donor/facility routes
  signup: async (userData, role = 'donor') => {
    try {
      // Constructs '/api/auth/signup/donor' or '/api/auth/signup/hospital'
      const endpoint = `/api/auth/signup/${role}`;
      const response = await api.post(endpoint, userData);
      return response.data;
    } catch (error) {
      throw (
        error.response?.data?.detail ||
        error.response?.data?.message ||
        'Registration failed.'
      );
    }
  },

  // 2. Cleaned Login path utilizing unified JSON payloads and storage
  login: async (email, password) => {
    try {
      // Directs to the correct JSON token path matching backend expectations
      const response = await api.post('/api/auth/token', {
        email: email,
        password: password
      });

      // Safely resolves whether backend returned a raw string token or standard JSON object
      const token = typeof response.data === 'string' ? response.data : response.data.access_token;

      if (token) {
        localStorage.setItem('token', token);
        
        if (response.data.role) {
          localStorage.setItem('role', response.data.role);
        }
        if (response.data.user_id) {
          localStorage.setItem('user_id', response.data.user_id);
        }
      }

      return response.data;
    } catch (error) {
      // Handle FastAPI Pydantic structural validation errors elegantly
      if (error.response?.status === 422 && error.response?.data?.detail) {
        const validationErrors = error.response.data.detail;
        console.error("Backend validation error details:", validationErrors);
        throw `Validation Error: ${validationErrors[0]?.msg || 'Invalid data layout'}`;
      }
      
      throw (
        error.response?.data?.detail ||
        'Invalid email or password.'
      );
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('user_id');
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },

  getToken: () => {
    return localStorage.getItem('token');
  },

  getRole: () => {
    return localStorage.getItem('role');
  },

  getUserId: () => {
    return localStorage.getItem('user_id');
  },
};

export default authService;