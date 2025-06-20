import { Stack, useRouter, useSegments } from 'expo-router';
import { useEffect, useState, createContext, useContext } from 'react';
import { ActivityIndicator } from 'react-native';

const AuthContext = createContext({ isAuthenticated: false, login: () => {}, logout: () => {} });

export function useAuth() {
  return useContext(AuthContext);
}

function AuthProvider({ children }: any) {
  const [isAuthenticated, setAuthenticated] = useState(false);
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    const [segment] = segments;
    const inTabs = segment === '(tabs)' as string;

    if (!isAuthenticated && inTabs) {
      router.replace('/');
    }
  }, [isAuthenticated]);

  const login = () => setAuthenticated(true);
  const logout = () => setAuthenticated(false);

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export default function RootLayout() {
  return (
    <AuthProvider>
      <Stack screenOptions={{ headerShown: false }} />
    </AuthProvider>
  );
}