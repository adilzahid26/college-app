import React from 'react';
import { View, Text, Button } from 'react-native';
import { useRouter } from 'expo-router';

export default function RegisterScreen() {
  const router = useRouter();

  return (
    <View style={{ padding: 20 }}>
      <Text>Register Screen</Text>
      <Button title="Go back to Login" onPress={() => router.back()} />
    </View>
  );
}