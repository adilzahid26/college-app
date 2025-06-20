import React from 'react';
import { View, Text, Button } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuth } from '../_layout';

export default function BioScreen() {
  const { logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.replace('/');
  };

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ marginBottom: 20 }}>Welcome to your Bio Screen!</Text>
      <Button title="Logout" onPress={handleLogout} />
    </View>
  );
}