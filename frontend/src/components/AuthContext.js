import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const user_id = localStorage.getItem('user_id');
    const username = localStorage.getItem('username');
    const is_patron = localStorage.getItem('is_patron') === 'true';
    const is_collaborateur = localStorage.getItem('is_collaborateur') === 'true';
    
    if (token && user_id && username) {
      setUser({ 
        token, 
        user_id, 
        username,
        is_patron, 
        is_collaborateur 
      });
    }
  }, []);

  const logout = () => {
    localStorage.clear();
    setUser(null);
    window.location.href = '/login';
  };

  const login = (token, userData) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user_id', userData.user_id);
    localStorage.setItem('username', userData.username);
    localStorage.setItem('is_patron', userData.is_patron);
    localStorage.setItem('is_collaborateur', userData.is_collaborateur);
    setUser({ token, ...userData });
  };

  const updateUser = (userData) => {
    setUser(userData);
  };

  return (
    <AuthContext.Provider value={{ user, setUser, logout, login, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
