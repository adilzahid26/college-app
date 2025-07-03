import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  ActivityIndicator,
  Alert,
  TouchableOpacity,
} from 'react-native';
import { useAuth } from '../_layout';
import styles from '../styles';

export default function SearchScreen() {
  const { user, loading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [users, setUsers] = useState<any[]>([]);

  useEffect(() => {
    if (authLoading) return;

    const fetchUsers = async () => {
      try {
        const res = await fetch('http://localhost:5000/search', {
          credentials: 'include',
        });
        if (!res.ok) throw new Error('Failed to load users');
        const data = await res.json();
        setUsers(data);
      } catch (err) {
        Alert.alert('Error', err instanceof Error ? err.message : 'Unexpected error loading users');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [authLoading]);

  if (loading || authLoading) {
    return (
      <View style={styles.outerContainer}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={{ padding: 20 }}>
      <Text style={styles.screenTitle}>Search Users</Text>

      {users.map((u, idx) => (
        <View key={idx} style={styles.searchCard}>
          <Text style={styles.searchUserText} numberOfLines={2} ellipsizeMode="tail">
            {u.first_name} {u.last_name} | {u.graduation_year || '-'} | {u.major || '-'} |{' '}
            {(u.interests || []).join(', ') || '-'} | {(u.hobbies || []).join(', ') || '-'}
          </Text>

          <TouchableOpacity style={styles.searchMessageButton} onPress={() => {}}>
            <Text style={styles.searchMessageButtonText}>Message</Text>
          </TouchableOpacity>
        </View>
      ))}
    </ScrollView>
  );
}
