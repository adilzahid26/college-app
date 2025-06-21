import React, { useState } from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuth } from './_layout';

export default function RegisterScreen() {
  const router = useRouter();
  const { login } = useAuth();

  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const handleRegister = async () => {
    if (!firstName || !lastName || !email || !password) {
      setErrorMsg("All fields are required!");
      return;
    }

    try {
      const registerResponse = await fetch('http://localhost:5000/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ firstName, lastName, email, password }),
      });

      const registerData = await registerResponse.json();

      if (!registerResponse.ok) {
        setErrorMsg(registerData.message || 'Registration failed');
        return;
      }

      const loginResponse = await fetch('http://localhost:5000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
        credentials: 'include',
      });

      const loginData = await loginResponse.json();

      if (loginResponse.ok) {
        login(loginData.user);
        router.replace('/BioScreen');
      } else {
        setErrorMsg(loginData.message || 'Login after registration failed');
      }
    } catch (err) {
      setErrorMsg('Something went wrong');
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <TextInput
        placeholder="First Name"
        value={firstName}
        onChangeText={setFirstName}
        style={{ marginBottom: 10, borderWidth: 1, padding: 8 }}
      />
      <TextInput
        placeholder="Last Name"
        value={lastName}
        onChangeText={setLastName}
        style={{ marginBottom: 10, borderWidth: 1, padding: 8 }}
      />
      <TextInput
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
        style={{ marginBottom: 10, borderWidth: 1, padding: 8 }}
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        autoCapitalize="none"
        style={{ marginBottom: 10, borderWidth: 1, padding: 8 }}
      />

      <Button title="Register" onPress={handleRegister} />

      {errorMsg ? <Text style={{ color: 'red', marginTop: 10 }}>{errorMsg}</Text> : null}

      <View style={{ marginTop: 20 }}>
        <Button title="Go back to Login" onPress={() => router.back()} />
      </View>
    </View>
  );
}